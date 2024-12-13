import io
import os
from flask_mail import Mail, Message
from flask import session
import pandas as pd

from flask_mysqldb import MySQL

mail = Mail()
mysql = MySQL()


def send_email_route_by_user(row, recent_date):

    # row ={
    #         "ip": con_ip,
    #         "status": isValid,
    #         "result": {"providers","detected_on", "is_blacklisted"},
    #         "user_id": user_id,
    #         "email":email
    #     }

    emails = set()

    for ip in row:
        if ip["result"]["is_blacklisted"]:
            emails.add(ip["email"])

    for email in emails:
        # print(email)
        send_email_route_bymail(email, recent_date)


def send_email_route_bymail(email, recent_date):

    mycursor = mysql.connection.cursor()

    # Fetching blacklisted files and adding it into a .csv file
    ip_query = """
    SELECT tblips.ipaddress, tblips.status, tblips.rdns, tblips.comments, tblipgroups.group_name AS ipgroup_name
    FROM tblips
    LEFT JOIN tblipgroups ON tblips.ipgroup = tblipgroups.id
    JOIN tblusers ON tblips.ownerid = tblusers.id
    WHERE tblusers.email = %s
      AND tblips.updated_at >= %s
      AND tblips.status = 'Blacklisted'
    ORDER BY tblips.id
"""
    mycursor.execute(ip_query, (email, recent_date))

    ip_result = mycursor.fetchall()
    mycursor.connection.commit()
    print(ip_result)

    if ip_result.__len__() > 0:

        df = pd.DataFrame(ip_result, columns=[i[0] for i in mycursor.description])
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Get the CSV content as a string
        csv_content = csv_buffer.getvalue()

        mycursor.connection.commit()

        msg = Message(
            subject="Blacklisted IPs",
            recipients=[email],
        )
        msg.attach("dashboard_information.csv", "text/csv", csv_content)
        mail.send(msg)
