from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from functions.blacklist.blacklist_functions import ips_between
from functions.dashboard.dashboard_ip_functions import reverse_DNS

mysql = MySQL()


def ips_add_range_route():
    if request.method == "POST":
        # get owner id from session
        owner_id = session.get("user_id")

        # assign values from form and remove white spaces from both ends with strip()
        ip_first = request.form.get("ips1").strip()
        ip_last = request.form.get("ips2").strip()
        comments = request.form.get("comments")
        ipgroup = request.form.get("ipgroup")

        # get all ips in between of first and last ip including last ip
        inBetween = ips_between(ip_first, ip_last)

        # result = reverse_DNS(inBetween, type="range")

        # create connection
        mycursor = mysql.connection.cursor()

        # create a query string for execution
        insert_query = """INSERT INTO tblips(ipaddress,ownerid,rdns,comments,ipgroup) Values(%s,%s,%s,%s,%s) 
                        ON DUPLICATE KEY UPDATE ipaddress=Values(ipaddress)"""

        # as we adding ips in range so we have to add ips in batches to avoid any overflow
        # Define batch size
        batch_size = 500
        # prepare data for range/batch
        # order should be same as defined in insert_query

        prepared_data = [
            # (ip, owner_id, result[index], comments, ipgroup)
            (ip, owner_id, "", comments, ipgroup)
            # (ip, owner_id,"", comments,ip_group)
            for index, ip in enumerate(inBetween)
        ]
        # Insert rows in batches
        for i in range(0, len(prepared_data), batch_size):
            batch = prepared_data[i : i + batch_size]
            # executemany to add data to database based on batch_size
            mycursor.executemany(insert_query, batch)

        mycursor.connection.commit()  # Commit after each batch

        # after the batch execute, redirect to ip dashboard
        return redirect(url_for("dashboard_ip"))

    else:
        return render_template("dashboard/ip/dashboard_ip.html")
