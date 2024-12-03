import datetime
import json
import re
import time
import socket


from typing import Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Response, session, copy_current_request_context
from flask_mysqldb import MySQL

mysql = MySQL()


# from requests import Response
from functions.blacklist.blacklist_functions import (
    getTemplate,
    is_valid_ipv4,
    updateResult,
)


# check if it is blacklisted or not
def check_dnsbl_bulk(reversed_ip: str, provider: str) -> Tuple[bool]:
    query = f"{reversed_ip}.{provider}"  # create a query
    try:
        # check if it gives any error for following code or not
        response = socket.gethostbyname(query)
        # if everything is OK, return True as ip is blacklisted
        return True
    # if name or service is not known, it means IP is not blacklisted
    except socket.gaierror:
        return False


# check if ip is blacklisted for every providers
def check_dnsbl_providers_bulk(ip_address: str, providers: list) -> dict:
    start_time, reversed_ip, result = getTemplate(ip_address)

    # check for each provider in providers list
    for provider in providers:
        # call function chec_dnsbl_bulk with reversed_ip and provider["provider"]
        isBlacklisted = check_dnsbl_bulk(reversed_ip, provider["provider"])
        updateResult(isBlacklisted, result, provider["provider"])
    end_time = time.time()

    result["time_elapsed"] = int(end_time - start_time)
    return result


def process_ip(ip, row, providers_bulk):
    con_ip = re.sub(r"[\r\n]", "", ip)

    # Check if IP already exists in the row
    if not any(ip_obj["ip"] == con_ip for ip_obj in row):
        isValid = is_valid_ipv4(con_ip)

        if isValid:
            # call check_dnsbl_providers_bulk with converted ip(con_ip) and providers bulk (providers_bulk)
            result = check_dnsbl_providers_bulk(con_ip, providers_bulk)
            return {"ip": con_ip, "status": isValid, "result": result}
    return None


# entry point for bulk blacklist
def process_ips(ip_list, row, providers_bulk):

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit each IP processing to the executor
        # call the process_ip with ip, row, providers_bulk as a parameter
        futures = [
            executor.submit(process_ip, ip, row, providers_bulk) for ip in ip_list
        ]

        # Collect results as they complete
        for future in as_completed(futures):
            result = future.result()
            if result:
                row.append(result)  # appends every result to row


def process_ips_ajax(ip_list, row, providers_bulk, type):

    user_id = session.get("user_id")
    mycursor = mysql.connection.cursor()

    @copy_current_request_context
    def update_db(result):
        date = datetime.datetime.today()

        # user_id = session.get("user_id")
        # mycursor = mysql.connection.cursor()

        # convert that date to timestamp
        recent_date = date.strftime("%Y-%m-%d %H:%M:%S")
        # if to_update_ips is not None or empty array
        # if to_update_ips:
        mycursor.execute(
            f"""UPDATE tblips
                                SET status='{"Blacklisted" if result["result"]["is_blacklisted"] else "Clean"}',
                                updated_at='{recent_date}'
                                WHERE ownerid='{user_id}' AND ipaddress='{result["ip"]}'"""
        )

    count = {}

    # map over each provider in providers_bulk
    for provider in providers_bulk:
        provider = provider["provider"]
        # count[provider["provider"]] as provider is a object and has provider name in its "provider" property
        count[provider] = 0

    def get_results():
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit each IP processing to the executor
            # call the process_ip with ip, row, providers_bulk as a parameter
            futures = [
                executor.submit(process_ip, ip, row, providers_bulk) for ip in ip_list
            ]

            # Collect results as they complete
            for future in as_completed(futures):
                result = future.result()
                if result:
                    # time.sleep(1)
                    # print(count)
                    for provider in providers_bulk:
                        provider = provider["provider"]
                        if provider in result["result"]["detected_on"]:
                            count[provider] += 1
                    newdata = {
                        "data": result,
                        "count": count,
                    }
                    # if type == "fetching":
                    update_db(result)

                    yield f"data: {json.dumps(newdata)}\n\n"

    return Response(
        get_results(),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
