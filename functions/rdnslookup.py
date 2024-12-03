import socket

from flask import render_template, request


def rdnslookup_route():

    result = ""  # Create variable to store rdns result
    ip = ""  # Create variable to store ip address
    try:
        # get ip data from form and remove spaces from both ends
        ip = request.form.get("ip").strip()

        # Resolve MX records
        result = socket.gethostbyaddr(ip)[0]

    # if dns records not found for given ip address
    except socket.herror:
        return render_template(
            "rdns.html", result={"error": "No DNS record found", "ip": ip}
        )

    # if error in execution
    except Exception as e:
        # if ip is given, and error occured for that ip
        if ip:
            return render_template(
                "rdns.html", result={"error": "Given IP is not valid", "ip": ip}
            )
        else:
            return render_template("rdns.html", result={"ip": ip})
    # if everythin is OK
    # return result and ip
    return render_template("rdns.html", result={"result": result, "ip": ip})
