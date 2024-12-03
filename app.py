# imported ips
import os  # to fetch environment variables in application
from flask import Flask, redirect, render_template, request, url_for, session
from dotenv import load_dotenv  # to use environment variables in application
from flask_mail import Mail  # to use mail in application
from flask_mysqldb import MySQL  # to use MySQL in application
from flask_session import Session  # to use sessions in application

# import routes and functions in application
from functions.blacklist.blacklist_functions import ips_between
from functions.bulkblacklist.bulkblacklist_functions import process_ips_ajax
from functions.dashboard.dashboard_ip_group import dashboard_ipgroup_route
from functions.delete_group import delete_ipgroup_route
from functions.email_verification import (
    resend_email_verification_route,
    verify_email_route,
)
from functions.logout import logout_route
from functions.mail.send_email import send_email_route
from functions.mxlookup import mxlookup_route
from functions.dnslookup import dnslookup_route
from functions.blacklist.blacklist import blacklist_route
from functions.pricing import pricing_route
from functions.recaptcha import validate_recaptcha_route
from functions.auth.login import login_route
from functions.rdnslookup import rdnslookup_route
from functions.update_group import update_ipgroup_route
from functions.whoisfetch import whoisfetch_route
from functions.whatismyip import whatis_myip_route, whatismyipdata_route
from functions.sslchecker import getsslchecker_route
from functions.bulkblacklist.bulkblacklist import bulkblacklist_route
from functions.auth.registration import registration_route
from functions.dashboard.edit_ip import edit_ip_route
from functions.dashboard.ips_add_csv import ips_add_csv_route
from functions.dashboard.dashboard_ip import dashboard_ip_list_route, dashboard_ip_route
from functions.dashboard.ips_add_range import ips_add_range_route
from functions.dashboard.ips_add_custom import ips_add_custom_route
from functions.dashboard.dashboard_profile import dashboard_profile_route
from functions.dashboard.dashboard_ip_functions import fetch_ips_route, fetch_ips_stream_route, fetch_rdns_route

from functions.providers_data import providers_bulk


load_dotenv()  # configure dotenv


app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
MySQL(app)

app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")  # sender email
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")  # app password
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")  # sender email
Mail(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# dnslookup -MX information
@app.route("/mx-lookup", methods=["POST", "GET"])
def mxlookup():
    return mxlookup_route()


@app.route("/dns-lookup", methods=["POST", "GET"])
def dnslookup():
    return dnslookup_route()


@app.route("/rdns-lookup", methods=["POST", "GET"])
def rdnslookup():
    return rdnslookup_route()


@app.route("/ip-blacklist", methods=["POST", "GET"])
def blacklist():
    return blacklist_route()


# @app.route("/bulk-blacklist", methods=["GET", "POST"])
# def bulkblacklist():
#    


@app.route("/whois-lookup", methods=["POST", "GET"])
def whoisfetch():
    return whoisfetch_route()


@app.route("/whatis-my-ip-data", methods=["POST", "GET"])
def whatismyipdata():
    return whatismyipdata_route()


@app.route("/whatis-my-ip", methods=["POST", "GET"])
def whatis_myip():
    return whatis_myip_route()


@app.route("/ssl-checker", methods=["POST", "GET"])
def getsslchecker():
    return getsslchecker_route()


@app.route("/validate-recaptcha", methods=["POST"])
def validate_recaptcha():
    return validate_recaptcha_route()


@app.route("/login", methods=["POST", "GET"])
def login():
    return login_route()


@app.route("/registration", methods=["POST", "GET"])
def registration():
    return registration_route()


@app.route("/logout", methods=["GET"])
def logout():
    return logout_route()


@app.route("/dashboard-profile", methods=["GET"])
def dashboard_profile():
    return dashboard_profile_route()


@app.route("/dashboard-ip", methods=["POST", "GET"])
def dashboard_ip():
    return dashboard_ip_route()


@app.route("/dashboard-ipgroup", methods=["POST", "GET"])
def dashboard_ipgroup():
    return dashboard_ipgroup_route()


@app.route("/ips-add-range", methods=["POST", "GET"])
def ips_add_range():
    return ips_add_range_route()


@app.route("/ips-add-custom", methods=["POST", "GET"])
def ips_add_custom():
    return ips_add_custom_route()


@app.route("/ips-add-csv", methods=["POST", "GET"])
def ips_add_csv():
    return ips_add_csv_route()


@app.route("/fetch-ips", methods=["GET", "POST"])
def fetch_ips():
    return fetch_ips_route()
    # return redirect(url_for("dashboard_ip"))

# @app.route("/fetch-ips-stream", methods=["GET"])
# def fetch_ips_stream():
#     return fetch_ips_stream_route()


@app.route("/fetch-rdns", methods=["POST", "GET"])
def fetch_rdns():
    return fetch_rdns_route()
    # return redirect(url_for("dashboard_ip"))


@app.route("/edit-ip", methods=["POST", "GET"])
def edit_ip():
    return edit_ip_route()


@app.route("/send-email", methods=["GET"])
def send_email():
    return send_email_route()


@app.route("/update-ipgroup", methods=["POST", "GET"])
def update_ipgroup():
    return update_ipgroup_route()


@app.route("/delete-ipgroup", methods=["POST"])
def delete_ipgroup():
    return delete_ipgroup_route()


@app.route("/verify-email", methods=["POST", "GET"])
def verify_email():
    return verify_email_route()


@app.route("/resend-email-verification", methods=["POST", "GET"])
def resend_email_verification():
    return resend_email_verification_route()


@app.route("/pricing", methods=["POST", "GET"])
def pricing():
    return pricing_route()


@app.route("/get-ips", methods=["GET", "POST"])
def get_ips():
    type_form = request.form.get("type_form")
    ips = []
    if type_form == "bulk":
        ip_first = request.form.get("ips1").strip()
        ip_last = request.form.get("ips2").strip()
        inbetweenips = ips_between(ip_first, ip_last)
        ips = inbetweenips
        session["ips"] = inbetweenips
    else:
        ips = request.form.get("ips")
        # strip ips, and create new array of ips defined per line
        converted_ips = ips.strip().replace("\r", "").split("\n")

        new_ips = []  # initialize new_ips with empty array

        # remove repeated ips
        for ip in converted_ips:
            if not ip in new_ips:
                new_ips.append(ip)
        session["ips"] = new_ips

        ips = new_ips

    return {"ips": ips}


@app.route("/bulk-blacklist", methods=["GET", "POST"])
def bulkblacklist():
    return render_template("bulkblacklist.html")


@app.route("/bulk-blacklist-stream", methods=["GET", "POST"])
def bulkblacklist_ajax_stream():
    # get ips in between of given two ips with first and last included
    ips = session.get("ips")
    row = []

    return process_ips_ajax(ips, row, providers_bulk)


@app.route("/get-bulkblacklist-table-template", methods=["POST"])
def bulkblacklist_ajax_table_template():
    ips = request.json.get("ips", [])  # Get the ips list from the POST data
    return render_template("table-templates/table-bulkblacklist.html", ips=ips)


if __name__ == "__main__":
    app.run(debug=True)
