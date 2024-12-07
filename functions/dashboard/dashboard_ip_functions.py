from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import json
import socket

from flask import (
    session,
    Response,
    request,
    copy_current_request_context,
)
from flask_mysqldb import MySQL
from functions.providers_data import providers_bulk
from functions.bulkblacklist.bulkblacklist_functions import (
    process_ips_ajax,
)

mysql = MySQL()


def get_ips_for_fetch_route():
    mycursor = mysql.connection.cursor()

    mycursor.execute(
        """SELECT * FROM tblips
            WHERE ownerid = {user_id}
            ORDER BY time(ip_updated_at)
            LIMIT 100"""
    )

    mycursor.connection.commit()

    ips = []
    ipslist = mycursor.fetchall()
    for ip in ipslist:
        ips.append(ip[1])

    session["ips"] = ips

    return {"ips": ips}


def fetch_ips_stream_route():
    user_id = session.get("user_id")
    # initialize the cursor
    mycursor = mysql.connection.cursor()
    # execute the query, get ips of respected user, order by ip_Updated_at as ascending and get first 100 results
    mycursor.execute(
        f"""SELECT * FROM tblips WHERE ownerid = {user_id} ORDER BY time(ip_updated_at) LIMIT 100"""
    )

    # store them as non-updated ips
    non_updated_ips = mycursor.fetchall()
    # as non_updated_ips is list of each row as a structure of list, we have to get ip from list
    # create new variable to store the ips
    to_update_ips = []
    # loop on each row, add ip to to_update_ips
    for ip in non_updated_ips:
        to_update_ips.append(ip[1])

    # create a new variable to store result
    row = []
    # call the process_ips function, send ips list, row, and providers_bulk
    return process_ips_ajax(to_update_ips, row, providers_bulk, "fetching")


def fetch_ips_route():
    # get user_id from session
    user_id = session.get("user_id")
    # initialize the cursor
    mycursor = mysql.connection.cursor()
    # execute the query, get ips of respected user, order by ip_Updated_at as ascending and get first 100 results
    mycursor.execute(
        f"""SELECT * FROM tblips WHERE ownerid = {user_id} ORDER BY time(ip_updated_at) LIMIT 100"""
    )

    if request.method == "POST":
        ips = []
        ipslist = mycursor.fetchall()
        mycursor.connection.commit()

        for ip in ipslist:
            ips.append(ip[1])

        return {"ips": ips}


# FETCH RDNS FUNCTIONS ###########

def reverse_DNS(ip, type):
    try:
        if type == "custom":
            return socket.gethostbyaddr(ip[0])[0]
        else:
            return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None


def lookup(ip):
    return {"ip": ip, "rdns": reverse_DNS(ip, type="csv")}


def process_rdns_ajax(ip_list):

    user_id = session.get("user_id")

    @copy_current_request_context
    def update_db(result):

        date = datetime.datetime.today()
        recent_date = date.strftime("%Y-%m-%d %H:%M:%S")

        try:
            with mysql.connection.cursor() as cursor:
                query = """
                    UPDATE tblips
                    SET rdns=%s,updated_at=%s,rdns_updated_at=%s
                    WHERE ownerid=%s AND ipaddress=%s
                """
                cursor.execute(
                    query,
                    (result["rdns"], recent_date, recent_date, user_id, result["ip"]),
                )
                mysql.connection.commit()
        except mysql.OperationalError as e:
            print(f"Database operation failed: {e}")

    def get_results():
        with ThreadPoolExecutor() as executor:

            futures = [executor.submit(lookup, ip) for ip in ip_list]

            for future in as_completed(futures):
                result = future.result()
                if result:
                    update_db(result)
                    yield f"data: {json.dumps(result)}\n\n"

    return Response(
        get_results(),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


def fetch_rdns_stream_route():
    user_id = session.get("user_id")

    mycursor = mysql.connection.cursor()

    mycursor.execute(
        f"""SELECT * FROM tblips
            WHERE ownerid={user_id}
            ORDER BY time(rdns_updated_at)
            LIMIT 100"""
    )

    non_updated_ips = mycursor.fetchall()

    to_update_ips_rdns = []
    for ip in non_updated_ips:
        to_update_ips_rdns.append(ip[1])

    return process_rdns_ajax(to_update_ips_rdns)


def fetch_rdns_route():
    user_id = session.get("user_id")
    mycursor = mysql.connection.cursor()

    mycursor.execute(
        f"""SELECT * FROM tblips
            WHERE ownerid={user_id}
            ORDER BY time(rdns_updated_at)
            LIMIT 100"""
    )

    if request.method == "GET":
        rdns = []

        non_updated_rdns = mycursor.fetchall()
        mycursor.connection.commit()
        for ip in non_updated_rdns:
            rdns.append(ip[1])

        return {"ips": rdns}
