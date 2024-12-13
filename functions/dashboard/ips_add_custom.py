from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mysql = MySQL()


def ips_add_custom_route():
    if request.method == "POST":
        # get owner_id from session
        owner_id = session.get("user_id")
        # get ips array from form, strip it to remove spaces and splitlines to get ips per line
        ips = request.form.get("ips", "").strip().splitlines()
        ipgroup = request.form.get("ipgroup")

        # to get ip and its comments split the each ips string by "//",
        # as first should be ip and second should be comment for that particular ip
        ips = [ip.strip().split("//") for ip in ips]

        # initialize the cursor
        mycursor = mysql.connection.cursor()
        # create a insert query string
        insert_query = """INSERT INTO tblips(ipaddress,ownerid,comments,ipgroup) values(%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE ipaddress=Values(ipaddress)"""

        # we are adding ips in batch to database to avoid overflow issues
        batch_size = 500
        # we are creating a prepared_data for values in insert_query string
        # as each element in ips is a array so, first should be ip and second should be comment for that ip
        # ip[0]-> ip address, ip[1]-> comment for that ip address
        prepared_data = [
            (
                (ip[0], owner_id, ip[1], ipgroup)
                if ip.__len__() > 1
                else (ip[0], owner_id, None, ipgroup)
            )
            for ip in ips
        ]

        # Insert rows in batches
        for i in range(0, len(prepared_data), batch_size):
            batch = prepared_data[i : i + batch_size]

            # executemany to add data to database in batches
            mycursor.executemany(insert_query, batch)

        mycursor.connection.commit()

        # After completion redirect to ip dashboard
        return redirect(url_for("dashboard_ip"))
    else:
        return render_template("dashboard/ip/dashboard_ip.html")
