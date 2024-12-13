from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import os
import re
from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv  # to use environment variables in application


from bulkblacklist_functions import (
    check_dnsbl_providers_bulk,
)

from email_functions import  send_email_route_by_user
from bulk_providers import providers_bulk
from flask_mail import Mail  # to use mail in application


mysql = MySQL()

load_dotenv()  # configure dotenv
app = Flask(__name__)

app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
MySQL(app)

app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")  # sender email
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")  # app password
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")  # sender email
Mail(app)


with app.app_context():
        



    def is_valid_ipv4(ip):
        ipv4_regex = re.compile(
            r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        )
        return re.match(ipv4_regex, ip) is not None


    def process_ip(ip, row, providers_bulk, user_id, email):
        con_ip = re.sub(r"[\r\n]", "", ip)

        # Check if IP already exists in the row
        if not any(ip_obj["ip"] == con_ip for ip_obj in row):
            isValid = is_valid_ipv4(con_ip)

            if isValid:
                # call check_dnsbl_providers_bulk with converted ip(con_ip) and providers bulk (providers_bulk)
                result = check_dnsbl_providers_bulk(con_ip, providers_bulk)
                return {
                    "ip": con_ip,
                    "status": isValid,
                    "result": result,
                    "user_id": user_id,
                    "email": email,
                }
        return None


    def process_ips(ip_list, row, providers_bulk):  # iplist = ((ipaddrees, userid, email))

        def update_db(result):
            # result {
            #         "ip": con_ip,
            #         "status": isValid,
            #         "result": result,
            #         "user_id": user_id,
            #           "email": email
            #     }

            user_id = result["user_id"]
            date = datetime.datetime.today()
            recent_date = date.strftime("%Y-%m-%d %H:%M:%S")

            try:
                with mysql.connection.cursor() as cursor:
                    query = """
                        UPDATE tblips SET
                        status=last_status, status = %s, updated_at = %s, ip_updated_at=%s
                        WHERE ownerid = %s AND ipaddress = %s
                    """
                    status = (
                        "Blacklisted" if result["result"]["is_blacklisted"] else "Clean"
                    )
                    cursor.execute(
                        query, (status, recent_date, recent_date, user_id, result["ip"])
                    )
                    mysql.connection.commit()
            except mysql.OperationalError as e:
                print(f"Database operation failed: {e}")

        def get_results():
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Submit each IP processing to the executor
                # call the process_ip with ip, row, providers_bulk as a parameter
                futures = [
                    executor.submit(process_ip, ip[0], row, providers_bulk, ip[1], ip[2])
                    for ip in ip_list
                ]

                # Collect results as they complete
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        update_db(result)
                        row.append(result)

        get_results()


    def call_mysql():


        mycursor = mysql.connection.cursor()

        mycursor.connection.commit()
        # execute the query to get all ips of respected user,
        # adds ipgroup_name to the list as ipgroup name of that ip
        mycursor.execute(
            f"""SELECT tblips.ipaddress, tblips.ownerid, tblusers.email AS user_email
            FROM tblips
            LEFT JOIN tblusers ON tblips.ownerid = tblusers.id
            ORDER BY tblips.ip_updated_at LIMIT 1000"""
        )
        # get ips from database where ips are lastly updated

        ips = mycursor.fetchall()

        results = mycursor.fetchall()
        mycursor.connection.commit()
        row = []

        date = datetime.datetime.today()
        recent_date = date.strftime("%Y-%m-%d %H:%M:%S")
        recent_date_obj = datetime.datetime.strptime(recent_date, "%Y-%m-%d %H:%M:%S")

        process_ips(ips, row, providers_bulk)  # at this point ip and status is updated
        send_email_route_by_user(row, recent_date_obj)

        # print(row)
        
    call_mysql()


# if __name__ == "__main__":
#     app.run(debug=True)



