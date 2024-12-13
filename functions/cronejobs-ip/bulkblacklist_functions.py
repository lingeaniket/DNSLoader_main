import datetime
import socket
import time
from typing import Tuple


def updateResult(isBlacklisted, result, provider):
    if isBlacklisted:
        # add provider on top of all other providers, because it is blacklisted
        result["providers"].insert(0, provider)
        # add provider in detected_on array
        result["detected_on"].append(provider)
        result["is_blacklisted"] = True  # add is_blacklisted as True
    else:
        # add provider to providers array
        result["providers"].append(provider)


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


def getTemplate(ip_address: str) -> Tuple[str, str, dict]:
    # get start time of execution of code
    start_time = time.time()
    # reverse the given ip
    # requires to check blacklisted or not
    reversed_ip = ".".join(reversed(ip_address.split(".")))
    # create a format for end result
    result = {
        "detected_on": [],
        "providers": [],
        "is_blacklisted": False,
        "hostname": ip_address,
        # "date": str(datetime.now())[:19],
    }

    return start_time, reversed_ip, result


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
