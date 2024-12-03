import whois

from flask import render_template, request


# convert the row to array and make it object as below,
# [{"key": "domain", "value": "domain.com", "name": "Domain", "isList": False}, {...}]
def getDataInFormat(data):
    return [
        {
            "key": key,
            "value": value,
            # replace keys with "_" with " " and make every first letter of word capital
            "name": key.replace("_", " ").title(),
            "isList": type(value) == list,  # check if it is list or not
        }
        for key, value in data.items()
    ]


# function to convert date in user readable format, if it is list send only first date
def getProperDate(date):
    # if date is not not available, send Not Available message
    return (
        date[0].strftime("%Y-%m-%d")
        if isinstance(date, list)
        else (date.strftime("%Y-%m-%d") if date else "Not Available")
    )


def whoisfetch_route():
    if request.method == "GET":
        return render_template("whois.html", result={})

    whoisdata = ""
    rawData = ""
    domain = ""
    try:
        # get domain from form and remove spaces from
        domain = request.form.get("domain").strip()
        output_data = whois.whois(domain)  # get the output data
        rawData = output_data  # store raw data

        # Handled cases where dates might be lists, call getProperDate and send date as a parameter
        updated_date = getProperDate(output_data.updated_date)
        creation_date = getProperDate(output_data.creation_date)
        expiration_date = getProperDate(output_data.expiration_date)

        registrar = output_data.registrar  # domain registar details

        # All name servers
        all_name_servers = output_data.name_servers
        # convert them to lowercase
        all_name_servers = [name_server.lower() for name_server in all_name_servers]
        # extract unique name servers
        # get only 4 name server
        name_servers = list(set(all_name_servers))[:4]

        # add details to row
        row = {
            "domain": domain,
            "registrar": registrar,
            "creation_date": creation_date,
            "expiration_date": expiration_date,
            "updated_date": updated_date,
            "name_servers": name_servers,
        }
        # get whoisdata and raw data in format of {"key": "xyz", "value": "xyz", "name": "Xyz", "is_list": False}
        whoisdata = getDataInFormat(row)
        whoisRawdata = getDataInFormat(rawData)

    except Exception as e:
        # if error is raised during execution
        return render_template(
            "whois.html",
            result={
                "error": "Given domain is not valid",
                "domain": domain,
                "raw": "",
            },
        )
    # return result, row and raw data
    return render_template(
        "whois.html",
        result={"domain": domain, "row": whoisdata, "raw": whoisRawdata},
    )
