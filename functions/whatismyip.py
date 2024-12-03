import geocoder


from flask import jsonify, render_template, request


# main "/whatis-my-ip-data" route
# only get data not render template
def whatismyipdata_route():
    ipv4 = ""  # store public ip
    ip_geo = {}  # store new_ip
    ip = ""  # store ip
    try:
        # get ip from form and remove spaces from both ends
        ip = request.args.get("ip").strip()

        if ip:
            ipv4 = ip  # if ip available, store it in public_ip
            # get location from geocoder and store it in new ip
            ip_geo = geocoder.ip(ipv4)

    except Exception as e:
        print(f"Error: {e}")

    result = {
        "ipv4": ipv4,
        "address": {
            "latitude": ip_geo.lat,
            "longitude": ip_geo.lng,
            "city": ip_geo.city,
            "country": ip_geo.country,
            "state": ip_geo.state,
            "org": ip_geo.org,
            "postal": ip_geo.postal,
        },
    }
    return jsonify(result)


# main "/whatis-my-ip" route
def whatis_myip_route():
    return render_template("whatis-my-ip.html", result={})
