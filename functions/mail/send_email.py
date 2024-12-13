import io
import os
from flask_mail import Mail, Message
from flask import session
import pandas as pd

from flask_mysqldb import MySQL

mail = Mail()
mysql = MySQL()

parent = os.path.dirname(os.path.abspath(__file__))
os.chdir(parent)


def send_email_route():
    user_id = session.get("user_id")

    mycursor = mysql.connection.cursor()

    # Fetching blacklisted files and adding it into a .csv file
    ip_query = f"Select ipaddress, status, rdns, comments, last_status from tblips where ownerid={user_id} ORDER BY ip_updated_at LIMIT 1000"
    mycursor.execute(ip_query)

    ip_result = mycursor.fetchall()
    mycursor.connection.commit()

    mycursor.execute(f"Select ipaddress, status, rdns, comments from tblips LIMIT 1")
    mycursor.fetchall()
    mycursor.connection.commit()
    ip_result_main = []
    # ip_result=list(ip_result)

    for ip in ip_result:
        if ip[1] != ip[4]:
            ip = list(ip)
            ip.pop()
            ip_result_main.append(ip)
    if ip_result_main.__len__() > 0:

        df = pd.DataFrame(ip_result_main, columns=[i[0] for i in mycursor.description])
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Get the CSV content as a string
        csv_content = csv_buffer.getvalue()

        # email id and information
        query = f"SELECT *FROM tblusers WHERE id='{user_id}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        if result:
            email = result[0][3]
            mycursor.connection.commit()

            msg = Message(
                subject="Updated Status IPs",
                recipients=[email],
            )
            msg.attach("dashboard_information.csv", "text/csv", csv_content)
            mail.send(msg)

