import dns
import datetime
import dns.resolver


from flask import render_template, request
from functions.sslchecker_function import (
    get_cert,
    get_cert_info,
    get_tls_info,
    is_forcing_https,
    is_tls_version_outdated,
    parse_cert,
)


# function to get the certificate for given hostname with port = 443
def get_ssl_certificate(host):
    port = 443

    # call get_cert, pass hostname and port to get the certificate in binary
    cert_binary = get_cert(host, port)
    if cert_binary:
        result = {}  # create a object to store the end result

        cert = parse_cert(cert_binary)  # call get_cert and get certificate
        # call get_cert_info and get the certificate information
        cert_info = get_cert_info(cert, host)

        tls_info = {}  # create a object to store the tls information
        tls_error = ""  # create a variable to add an tls error

        # call get_tls_info and get the tls information
        # get_tls_info returns {data: {...}, error: {...}}
        tls_info_main = get_tls_info(host, port)

        # first check for any error in tls information
        # if any error while getting tls information
        if tls_info_main["error"] == "Hostname mismatch":
            result["domain_matching_error"] = True

        # elif tls_info_main["error"]=="Domain error":
        #     result["domain_error"] = True

        # if no error and has data in tls_info_main
        elif tls_info_main["data"]:
            tls_info = tls_info_main["data"]  # store tls information data in tls_info

        else:  # if there is any other error, store it also
            tls_error = tls_info_main["error"]
            result["tls_error"] = tls_error

        for key, value in cert_info.items():  # add every details in result object
            result[key] = value

        # add tls details to result object
        result["protocol"] = tls_info["tls_version"]
        result["cipher"] = tls_info["cipher"]
        # check if tls version is outdated or not
        result["outdated_tls"] = is_tls_version_outdated(tls_info["tls_version"])

        # call is_forcing_https with given hostname and get result
        result["https_forced"] = is_forcing_https(host)

        return result  # return result
    else:
        return None  # return None


# main "ssl-checker" route
def getsslchecker_route():
    # if method is "GET", render template
    if request.method == "GET":
        return render_template("sslchecker.html", result={"fetched": False})
    elif request.method == "POST":
        ssl_certificate = {}  # create a ssl_certificate object to store the data
        ssl_certificate["timeofcompletion"] = str(datetime.datetime.now())[:19]

        try:
            # remove the https or http from host
            domain_host = request.form.get("host")
            host_arr = domain_host.split("//")

            host = ""
            if host_arr.__len__() == 1:
                host = host_arr[0]
            elif host_arr.__len__() == 2:
                host = host_arr[1]

            # if host is empty string, return error as host is required
            if not host:
                return render_template(
                    "sslchecker.html",
                    result={"error": "Host field is required.", "fetched": True},
                )

            # check if dns resolve the host
            try:
                mx_records = dns.resolver.query(host, "A")

            except dns.resolver.NXDOMAIN:  # domain is not found
                ssl_certificate["domain_error"] = True  # set domain error as True
                return render_template(
                    "sslchecker.html",
                    result={
                        "certificate": ssl_certificate,
                        "query": domain_host,
                        "fetched": True,
                    },
                )

            # if any exception is raised during execution
            except Exception as e:
                ssl_certificate["domain_error"] = True  # set domain error as True
                return render_template(
                    "sslchecker.html",
                    result={
                        "certificate": ssl_certificate,
                        "query": domain_host,
                        "fetched": True,
                    },
                )

            # if everything is fine, call get_ssl_certificate and get the certificate
            ssl_certificate = get_ssl_certificate(host)

            # print(ssl_certificate)

            # if no ssl certificate found
            if not ssl_certificate:
                return render_template(
                    "sslchecker.html",
                    result={
                        "error": "Your SSL certificate does not match your domain name!",
                        "query": host,
                        "fetched": True,
                    },
                )

            # get time of completion
            ssl_certificate["timeofcompletion"] = str(datetime.datetime.now())[:19]

            # create a query based on https_forced
            query = f"http{'s' if ssl_certificate['https_forced'] else ''}://{host}"
            return render_template(
                "sslchecker.html",
                result={
                    "certificate": ssl_certificate,
                    "query": query,
                    "fetched": True,
                },
            )
        # If any error during execution
        except Exception as e:
            print(e)
            return render_template(
                "sslchecker.html",
                result={
                    "certificate": ssl_certificate,
                    "query": domain_host,
                    "fetched": True,
                },
            )
