function changeType() {
    const type = this.type;
    const custom = document.getElementById("custom");
    const custom_btn = document.getElementById("custom_btn");
    const bulk = document.getElementById("bulk");
    const bulk_btn = document.getElementById("bulk_btn");
    if (type === "custom") {
        custom.style.display = "block";
        bulk.style.display = "none";
        custom_btn.setAttribute("disabled", "true");
        bulk_btn.removeAttribute("disabled");
    } else {
        custom.style.display = "none";
        bulk.style.display = "block";
        custom_btn.removeAttribute("disabled");
        bulk_btn.setAttribute("disabled", "true");
    }
}

function get_results() {
    const eventSource = new EventSource("/bulk-blacklist-stream");
    eventSource.onmessage = function (event) {
        const { data, count } = JSON.parse(event.data); // Parse JSON data

        ["zen.spamhaus.org", "b.barracudacentral.org", "bl.spamcop.net"].forEach((provider, idx) => {
            const intd = document.getElementById(`${data.ip}-${idx}`);
            intd.style.textAlign = "center";
            intd.innerHTML = " Ok ";
            intd.className = "tb-detected1";

            if (data.result.is_blacklisted && data.result.detected_on.indexOf(provider) > -1) {
                intd.innerHTML = " Listed ";
                intd.className = "tb-detected";
            }
        });

        ["zen.spamhaus.org", "b.barracudacentral.org", "bl.spamcop.net"].forEach((names, idx) => {
            const list = document.getElementById(`${idx + 1}-provider`);
            list.innerHTML = `Listed = ${count[names]}`;
        });
    };

    eventSource.onerror = function () {
        console.error("Error occurred while streaming data");
        eventSource.close(); // Close the connection
    };
}

function onSubmit(token) {
    const formData = new FormData();
    formData.append("g-recaptcha-response", token);
    fetch("/validate-recaptcha", { method: "POST", body: formData })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const hero = document.getElementById("hero");
                hero.classList.add("searched");

                const formtosubmit = document.getElementById("formtosubmit");

                const formdata = new FormData(formtosubmit);

                const custom_btn = document.getElementById("custom_btn");

                if (custom_btn.getAttribute("disabled")) {
                    formdata.set("type_form", "custom");
                } else {
                    formdata.set("type_form", "bulk");
                }

                fetch("/get-ips", {
                    method: "POST",
                    body: formdata,
                })
                    .then((response) => {
                        return response.json();
                    })
                    .then((response) => {
                        const ips = response.ips;

                        fetch("/get-bulkblacklist-table-template", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({ ips: ips }),
                        })
                            .then((response) => response.text())
                            .then((data) => {
                                // Insert the HTML table into the div with id 'bulkblacklist-ajax-table'
                                const tablediv = document.getElementById("bulkblacklist-ajax-table");
                                const tablesection = document.getElementById("table");
                                tablesection.style.display = "block";
                                tablediv.innerHTML = data; // Insert the fetched HTML into the div
                                get_results();
                            })
                            .catch((error) => {
                                console.error("Error fetching the table:", error);
                            });
                    });
            } else {
                document.getElementById("error-message").innerHTML = data.message;
            }
        });
}
function validate(event) {
    event.preventDefault();
    grecaptcha.execute();
}
function onload() {
    var element = document.getElementById("Submit");
    element.onclick = validate;
}
