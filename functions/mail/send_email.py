from flask import session
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

mail = Mail()
mysql = MySQL()


def send_email_route(row):
    user_id = session.get("user_id")
    blacklisted_ips = [
        ip_data for ip_data in row if ip_data["result"]["is_blacklisted"]
    ]
    ip_list = []
    if blacklisted_ips.__len__() > 0:
        for ip in blacklisted_ips:
            ip_list.append(ip["ip"])

        mycursor = mysql.connection.cursor()
        query = f"SELECT *FROM tblusers WHERE id='{user_id}'"
        mycursor.execute(query)
        result = mycursor.fetchone()
        if result:
            email = result[3]
            mycursor.connection.commit()

            msg = Message(
                subject="Blacklisted IPs",
                recipients=[email],
                body=f"The following IPs are blacklisted:'{sorted(
                    ip_list, key=lambda ip: [int(part) for part in ip.split(".")]
                )}'",
            )

            mail.send(msg)
