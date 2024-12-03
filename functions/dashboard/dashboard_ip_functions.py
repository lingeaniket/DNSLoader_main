from concurrent.futures import ThreadPoolExecutor
import datetime
import socket

from flask import session, request, redirect, url_for, copy_current_request_context
from flask_mysqldb import MySQL
from functions.providers_data import providers_bulk
from functions.mail.send_email import send_email_route
from functions.bulkblacklist.bulkblacklist_functions import (
    process_ips,
    process_ips_ajax,
)

mysql = MySQL()


def get_ips_for_fetch_route():
    mycursor = mysql.connection.cursor()

    mycursor.execute(
        "SELECT * FROM tblips WHERE ownerid = {user_id} ORDER BY time(updated_at) LIMIT 100"
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
    # execute the query, get ips of respected user, order by Updated_at as ascending and get first 100 results
    mycursor.execute(
        f"""SELECT * FROM tblips WHERE ownerid = {user_id} ORDER BY time(updated_at) LIMIT 100"""
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
    # execute the query, get ips of respected user, order by Updated_at as ascending and get first 100 results
    mycursor.execute(
        f"""SELECT * FROM tblips WHERE ownerid = {user_id} ORDER BY time(updated_at) LIMIT 100"""
    )

    if request.method == "GET":

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

        # order the row result as ascending order of ip address

        order_map = {ip: index for index, ip in enumerate(to_update_ips)}
        row = sorted(row, key=lambda ip: order_map.get(ip["ip"], len(to_update_ips)))

        # call the send_email to send email of blacklisted ips
        # send_email_route(row)

        for ip_data in row:
            # get time of updation
            date = datetime.datetime.today()
            # convert that date to timestamp
            recent_date = date.strftime("%Y-%m-%d %H:%M:%S")
            # if to_update_ips is not None or empty array
            if to_update_ips:
                # execute the query
                mycursor.execute(
                    f"""UPDATE tblips
                        SET status='{"Blacklisted" if ip_data["result"]["is_blacklisted"] else "Clean"}',
                        updated_at='{recent_date}'
                        WHERE ownerid='{user_id}' AND ipaddress='{ip_data["ip"]}'"""
                )
        mycursor.connection.commit()

        return redirect(url_for("dashboard_ip"))

    else:
        mycursor = mysql.connection.cursor()
        print(user_id)

        mycursor.execute(
            f"""SELECT * FROM tblips WHERE ownerid = {user_id} ORDER BY time(updated_at) LIMIT 100"""
        )

        mycursor.connection.commit()

        ips = []
        ipslist = mycursor.fetchall()
        for ip in ipslist:
            ips.append(ip[1])

        return {"ips": ips}

    # return SELECT * FROM tblips WHERE ownerid = {user_id} ORDER BY time(updated_at) LIMIT 100


def reverse_DNS(inBetween, type):
    result = []
    # inBetween = ips_between(ip_first, ip_last)
    for ip in inBetween:
        try:
            if type == "custom":
                reverse_DNS = socket.gethostbyaddr(ip[0])[0]
            else:
                reverse_DNS = socket.gethostbyaddr(ip)[0]
            result.append(reverse_DNS)

        except Exception as e:
            result.append(None)

    return result


def reverse_DNS(ip, type):
    """
    Perform a reverse DNS lookup for a single IP address.
    """
    try:
        if type == "custom":
            return socket.gethostbyaddr(ip[0])[0]
        else:
            return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None


def get_rdns(ip_list):
    """
    Perform reverse DNS lookups for a list of IPs using ThreadPoolExecutor.
    """

    def lookup(ip):
        return {"ip": ip, "rdns": reverse_DNS(ip, type="csv")}

    with ThreadPoolExecutor() as executor:
        # Submit tasks and collect results
        results = list(executor.map(lookup, ip_list))

    return results


# create a function of rdns_fetch
def fetch_rdns_route():
    mycursor = mysql.connection.cursor()
    user_id = session.get("user_id")

    mycursor.execute(
        f"""SELECT * FROM tblips WHERE ownerid={user_id} ORDER BY time(updated_at) LIMIT 100"""
    )

    non_updated_rdns = mycursor.fetchall()
    updated_rdns = []
    for ip in non_updated_rdns:
        updated_rdns.append(ip[1])
    row = []

    row = get_rdns(updated_rdns)

    for ip_data in row:
        date = datetime.datetime.today()
        recent_date = date.strftime("%Y-%m-%d %H:%M:%S")
        if updated_rdns:
            mycursor.execute(
                f"""UPDATE tblips SET rdns='{ip_data["rdns"]}',updated_at='{recent_date}' 
                    WHERE ownerid='{user_id}' AND ipaddress='{ip_data["ip"]}'"""
            )
    mycursor.connection.commit()


def fetch_rdns():
    mycursor = mysql.connection.cursor()
    user_id = session.get("user_id")
    mycursor.execute(
        f"""SELECT * FROM tblips WHERE ownerid={user_id} ORDER BY time(updated_at) LIMIT 100"""
    )

    ips = mycursor.fetchall()
