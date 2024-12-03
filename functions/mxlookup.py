import dns
import dns.resolver


from flask import render_template, request


def mxlookup_route():

    if request.method == "GET":
        return render_template("mxlookup.html", result={})
    elif request.method == "POST":

        # define the variables
        myresult = []  # end result
        domain = ""  # end domain
        try:
            # Get the domain from form input
            domain = request.form.get("domain").strip()
            # Fetch MX Records
            mx_records = dns.resolver.query(domain, "MX")
            for record in mx_records:
                recordsv4 = {"pref": "", "hostname": "", "ip": ""}
                recordsv6 = {"pref": "", "hostname": "", "ip": ""}

                mail_server = record.exchange.to_text()  # get the mail server/hostname

                recordsv4["pref"] = record.preference  # get the preference
                recordsv6["pref"] = record.preference  # get the preference

                recordsv4["hostname"] = f"{mail_server}"  # get the hostname
                recordsv6["hostname"] = f"{mail_server}"  # get the hostname

                # Resolve IPv4 (A record)
                try:
                    ipv4_records = dns.resolver.query(mail_server, "A")
                    for ipv4 in ipv4_records:
                        recordsv4["ip"] = f"{ipv4}"  # converted to string
                except dns.resolver.NoAnswer:  # if no answer
                    recordsv4["ip"] = "NA"
                myresult.insert(1, recordsv4)  # add IPv4 records to end result

                # Resolve IPv6 (AAAA record)
                try:
                    ipv6_records = dns.resolver.query(mail_server, "AAAA")
                    for ipv6 in ipv6_records:
                        recordsv6["ip"] = f"{ipv6}"  # converted to string
                except dns.resolver.NoAnswer:  # if no answer
                    recordsv6["ip"] = "NA"
                myresult.insert(1, recordsv6)  # add IPv6 records to end result

        except dns.resolver.NoAnswer:  # if no answer from server for given domain
            print(f"No MX records found for {domain}")
            # return results with given error
            return render_template(
                "mxlookup.html",
                result={
                    "results": myresult,
                    "query": domain,
                    "error": f"Sorry, we couldn't find any name servers for '{domain}'",
                },
            )
        except dns.resolver.NXDOMAIN:  # if domain not exist
            print(f"Domain {domain} does not exist")
            # return results with given error
            return render_template(
                "mxlookup.html",
                result={
                    "results": myresult,
                    "query": domain,
                    "error": f"Sorry, we couldn't find any name servers for '{domain}'",
                },
            )
        except Exception as e:  # if exception is raised in code
            print(f"Error: {e}")
            # if domain is there, send error message with template
            if domain:
                return render_template(
                    "mxlookup.html",
                    result={
                        "error": f"Sorry, we couldn't find any name servers for '{domain}'",
                        "query": domain,
                    },
                )
            # else return template with only query
            else:
                return render_template("mxlookup.html", result={"query": domain})
        # if everything is OK, return template with results, domain and query
        return render_template(
            "mxlookup.html",
            result={"results": myresult, "domain": domain, "query": domain},
        )
