import socket
import asyncio


from flask import render_template, request
from functions.providers_data import providers
from functions.blacklist.blacklist_functions import check_dnsbl_providers, is_valid_ipv4


def blacklist_route():
    if request.method == "GET":
        return render_template("blacklist.html", result={"data": False})
    elif request.method == "POST":
        # defined variables
        ip = ""  # ip/domain to check for blacklist
        try:
            # get the ip or domain from form, here ip can be a IP or domain name
            ip = request.form.get("ip").strip()

            if ip:
                new_ip = ip  # defined a new variable for ip to differentiate between form ip and ip for validation
                if not is_valid_ipv4(ip):  # if given ip is not valid
                    new_ip = socket.gethostbyname(ip)  # get domain by given ip
                # check for result
                result = asyncio.run(check_dnsbl_providers(new_ip, providers))
                # return result with result and given query
                return render_template(
                    "blacklist.html",
                    result={"result": result, "query": ip, "data": True},
                )
            # if ip is not available then return empty object
            else:
                return render_template("blacklist.html", result={"data": True})

        except Exception as e:
            print(e)
            # if there is error in execution return query and error message
            return render_template(
                "blacklist.html",
                result={"error": "Error in  blacklist", "query": ip, "data": True},
            )
