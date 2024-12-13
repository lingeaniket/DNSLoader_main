import pandas as pd

from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mysql = MySQL()


def ips_add_csv_route():
    if request.method == "POST":
        # get csv file form form data
        file = request.files.get("file")
        ipgroup = request.form.get("ipgroup")

        # get owner_id from session
        owner_id = session.get("user_id")

        print(file)

        # if file is there in form data
        if file:
            # convert file to object, as column name as key and rows data as a value
            df = pd.read_csv(file)

            # if at any point row is empty, so if data is there get that data or insert None for it
            ips = [None if pd.isna(ip) else ip for ip in df["IP"].to_list()]
            comments = []
            if "Comments" in df.columns:
                comments = [
                    None if pd.isna(comment) else comment
                    for comment in df["Comments"].to_list()
                ]
            else:
                comments = [None for _ip_ in df["IP"].to_list()]

            print(ips)
            # initialize the cursor
            mycursor = mysql.connection.cursor()

            # create the insert_query string
            insert_query = """INSERT INTO tblips(ipaddress,ownerid,comments,ipgroup) VALUES(%s,%s,%s,%s)
                            ON DUPLICATE KEY UPDATE ipaddress=Values(ipaddress)"""

            # we are adding each ips in batches
            # define batch size
            batch_size = 500
            # prepared data with values in insert_query, order should be same
            # ip as IP, owner_id as Owner_Id, Comments[index] as Comments
            prepared_data = [
                (ip, owner_id, comments[index], ipgroup) for index, ip in enumerate(ips)
            ]

            # Insert rows in batches
            for i in range(0, len(prepared_data), batch_size):
                batch = prepared_data[i : i + batch_size]
                # executemany to add data to database based on batch_size
                mycursor.executemany(insert_query, batch)
            mycursor.connection.commit()

        return redirect(url_for("dashboard_ip"))
    else:
        return render_template("dashboard/ip/dashboard_ip.html")
