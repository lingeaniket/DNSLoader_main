import dns
import dns.resolver


from flask import render_template, request


def dnslookup_route():
    if request.method == "GET":
        return render_template("dns-lookup.html", result={})
    elif request.method == "POST":
        # define the variables
        myresult = []  # variable for end result
        domain = ""  # variable for domain
        try:
            # Resolve MX records
            domain = request.form.get(
                "domain"
            ).strip()  # get domain from form and remove whitespaces from both ends with strip() function
            mx_records = dns.resolver.query(
                domain, "A"
            )  # resolve the query for given domain
            for record in mx_records:
                myresult.insert(1, record)  # insert every recor to the end result
        except dns.resolver.NoAnswer:  # means dns has no answer for given domain
            print(f"No MX records found for {domain}")
            # return error with error message
            return render_template(
                "dns-lookup.html",
                result={"error": f"No DNS records found for {domain}", "query": domain},
            )
        except dns.resolver.NXDOMAIN:  # means domain not exist
            print(f"Domain {domain} does not exist")
            if domain:  # means domain is not empty string
                # return error with error message
                return render_template(
                    "dns-lookup.html",
                    result={
                        "error": f"Domain {domain} does not exist",
                        "query": domain,
                    },
                )
            else:  # means domain is empty string
                return render_template(
                    "dns-lookup.html",
                    result={},
                )
        except Exception as e:  # exception while processing
            print(f"Error: {e}")
            if domain:  # means domain is not a empty string
                # return error message
                return render_template(
                    "dns-lookup.html",
                    result={"error": "Given domain is not valid", "query": domain},
                )
            else:  # means domain is empty string
                return render_template("dns-lookup.html", result={})
        # return template with results, domain and query
        return render_template(
            "dns-lookup.html",
            result={"results": myresult, "domain": domain, "query": domain},
        )
