from flask import render_template, request
from functions.providers_data import providers_bulk
from functions.blacklist.blacklist_functions import ips_between, is_valid_ipv4
from functions.bulkblacklist.bulkblacklist_functions import process_ips


def get_row_result(ips_list, sort_method):
    row = []  # initialize row with empty array

    # call process_ips function with unique IP addresses, row variable and providers_bulk (4 main providers)
    process_ips(ips_list, row, providers_bulk)

    # if row has to order by reference
    if sort_method == "reference":
        # create a new object for each ip as ip: index like {"1.1.1.1": 0, "2.2.2.2": 1,...}
        order_map = {ip: index for index, ip in enumerate(ips_list)}

        # Sort the data based on the index in the reference order
        # get ips index through order_map
        # if index not found default len(new_ips) will be added to ensure it will sorted in the end
        row = sorted(row, key=lambda ip: order_map.get(ip["ip"], len(ips_list)))
    elif sort_method == "ordered":
        # sort the row maintaining the order of ips
        row = sorted(row, key=lambda ip: [int(part) for part in ip["ip"].split(".")])
    # feature to get how many ips are blacklisted for given provider
    # created a variable for storing each provider
    count = {}

    try:
        # map over each provider in providers_bulk
        for provider in providers_bulk:
            provider = provider["provider"]
            # count[provider["provider"]] as provider is a object and has provider name in its "provider" property
            count[provider] = 0
            # map over each ips result
            for record in row:
                # if given provider is in detected_on, means it is blacklisted, so increase count by 1
                if provider in record["result"]["detected_on"]:
                    count[provider] += 1
    # if any exception is encountered
    except Exception as e:
        print(e)
    return row, count


def renderfor_invalid_ip(ip, first, last, type_form):
    # if ip is not valid, send error indicating that ip is invalid
    return render_template(
        "bulkblacklist.html",
        result={
            "error": f"{ip} is not valid IPv4 address.",
            "query": {"ips1": first, "ips2": last},
            "type_form": type_form,
        },
    )


def bulkblacklist_route():
    if request.method == "POST":
        print(request.method)
        # define variables
        ips = ""  # required for "custom" form type
        ip_first = ""  # required for "bulk" form type
        ip_last = ""  # required for "bulk" form type
        # get type of form to "custom" or "bulk"
        type_form = request.form.get("type_form").strip()
        print(type_form)
        try:
            if type_form == "custom":
                # for custom form type, it is a textarea for entering ips per line
                ips = request.form.get("ips")

                # strip ips, and create new array of ips defined per line
                converted_ips = ips.strip().replace("\r", "").split("\n")

                new_ips = []  # initialize new_ips with empty array

                # remove repeated ips
                for ip in converted_ips:
                    if not ip in new_ips:
                        new_ips.append(ip)

                if new_ips.__len__() > 256:  # return error as ips length is too large
                    return render_template(
                        "bulkblacklist.html",
                        result={
                            "error": "Too many IP addresses in the range.",
                            "query": ips,
                            "type_form": type_form,
                        },
                    )
                # call get_row_result with ip_list and sort_method as "ordered" to get row of results and count of ips
                row, count = get_row_result(new_ips, "reference")

                # return render template with query, row and type_form
                return render_template(
                    "bulkblacklist.html",
                    result={
                        "query": ips,
                        "row": row,
                        "type_form": type_form,
                        "providers": [
                            provider["provider"] for provider in providers_bulk
                        ],
                        "count": count,
                    },
                )
            # for ips in range
            elif type_form == "bulk":
                # get starting ip and remove whitespaces from both ends with strip()
                ip_first = request.form.get("ips1").strip()
                # get ending ip and remove whitespaces from both ends with strip()
                ip_last = request.form.get("ips2").strip()

                # check is ip_first is valid or not
                if not is_valid_ipv4(ip_first):
                    # if ip_first is not valid, send error indicating that first ip is invalid
                    return renderfor_invalid_ip(ip_first, ip_first, ip_last)

                # check is ip_last is valid or not
                if not is_valid_ipv4(ip_last):
                    return renderfor_invalid_ip(ip_last, ip_first, ip_last)

                # get ips in between of given two ips with first and last included
                inBetweenIps = ips_between(ip_first, ip_last)
                if inBetweenIps.__len__() > 256:
                    # return error if length is too long, more than 256
                    return render_template(
                        "bulkblacklist.html",
                        result={
                            "error": "Too many IP addresses in the range.",
                            "query": {"ips1": ip_first, "ips2": ip_last},
                            "type_form": type_form,
                        },
                    )
                # call get_row_result with ip_list and sort_method as "ordered" to get row of results and count of ips
                row, count = get_row_result(inBetweenIps, "ordered")
                # return the result with query, row and type_form
                return render_template(
                    "bulkblacklist.html",
                    result={
                        "query": {"ips1": ip_first, "ips2": ip_last},
                        "row": row,
                        "type_form": type_form,
                        "providers": [
                            provider["provider"] for provider in providers_bulk
                        ],
                        "count": count,
                    },
                )
            # if above conditions are not met
            else:
                return render_template("bulkblacklist.html", result={})
        # if error occured during execution/processing
        except Exception as e:
            # return template with error message
            return render_template(
                "bulkblacklist.html",
                result={"error": str(e), "query": ips, "type_form": type_form},
            )
    # if request is get then render only template with empty result object
    else:
        return render_template("bulkblacklist.html", result={})
