function fetchips() {
    const eventsource = new EventSource("/fetch-ips-stream");
    eventsource.onmessage = function (event) {
        const { data } = JSON.parse(event.data);

        const spinnTd = document.getElementById(`${data.ip}-01`);
        if (spinnTd) {
            spinnTd.innerHTML = data.ip;
            if (data.is_blacklisted) {
                spinnTd.className = "tb-detected";
            } else {
                spinnTd.className = "tb-detected1";
            }
        }
    };

    eventsource.onerror = function () {
        eventsource.close(); // Close the connection
    };
}

function callFetchIPs(event) {
    event.preventDefault();

    fetch("/fetch-ips", { method: "POST" })
        .then((response) => {
            return response.json();
        })
        .then((response) => {
            const ips = response.ips;

            for (const ip in ips) {
                const statusTd = document.getElementById(`${ips[ip]}-01`);
                if (statusTd) {
                    statusTd.innerHTML = "";
                    const inSpinn = document.createElement("div");
                    inSpinn.classList.add("spinner");
                    statusTd.appendChild(inSpinn);
                }
            }
            const subBtn = document.getElementById("fetch-ips");

            let coundown = 15;

            const timer = setInterval(() => {
                subBtn.innerHTML = `Please Wait for ${coundown} seconds`;

                if (coundown == 0) {
                    clearInterval(timer);
                    subBtn.innerHTML = "Fetch IPs";
                    subBtn.removeAttribute("disabled");
                }
                coundown--;
            }, 1000);
            subBtn.setAttribute("disabled", "true");
            fetchips();
        });
}

function fetchrdns() {
    const eventsource = new EventSource("/fetch-rdns-stream");
    eventsource.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log(data);
        const spinnTd = document.getElementById(`${data.ip}-02`);
        if (spinnTd) {
            spinnTd.innerHTML = data.rdns;
        }
    };
    eventsource.onerror = function () {
        eventsource.close(); // Close the connection
    };
}

function callFetchRdns(event) {
    event.preventDefault();
    fetch("/fetch-rdns", { method: "POST" })
        .then((response) => response.json())
        .then((response) => {
            const ips = response.ips;

            for (const ip in ips) {
                const statusTd = document.getElementById(`${ips[ip]}-02`);

                if (statusTd) {
                    statusTd.innerHTML = "";
                    const inSpinn = document.createElement("div");
                    inSpinn.classList.add("spinner");
                    statusTd.appendChild(inSpinn);
                }
            }
            const subBtn = document.getElementById("fetch-rdns");

            let coundown = 15;

            const timer = setInterval(() => {
                subBtn.innerHTML = `Please Wait for ${coundown} seconds`;

                if (coundown == 0) {
                    clearInterval(timer);
                    subBtn.innerHTML = "Fetch RDNS";
                    subBtn.removeAttribute("disabled");
                }
                coundown--;
            }, 1000);
            subBtn.setAttribute("disabled", "true");
            fetchrdns();
        });
}

function showComponent(button) {
    //show component
    const name = button.name;
    let form = button.closest("form");

    //hide the other components on click
    const components = document.querySelectorAll(".component");
    components.forEach((component) => {
        component.style.display = "none";
    });
    const buttons = document.querySelectorAll(".modal-button");
    buttons.forEach((button1) => {
        button1.removeAttribute("disabled");
    });
    if (name == "range") {
        form.action = "/ips-add-range";
    } else if (name == "custom") {
        form.action = "/ips-add-custom";
    } else if (name == "file-input") {
        form.action = "/ips-add-csv";
        form.enctype = "multipart/form-data";
    }

    button.setAttribute("disabled", "true");

    //Show selected component
    const matchingComponent = document.getElementById(name);
    if (matchingComponent) {
        matchingComponent.style.display = "block";
    }
}
function editIP(ip_obj) {
    const [ip, comment] = ip_obj.split("|");
    let oldElement = document.getElementById("old_ip");
    oldElement.value = ip;
    let newElement = document.getElementById("new_ip");
    newElement.value = ip;

    //comment
    let oldComment = document.getElementById("old_comment");
    oldComment.value = comment;
    let newComment = document.getElementById("new_comment");
    newComment.value = comment;
}

function handleFormSubWithRecaptcha(event, formid) {
    event.preventDefault();
    window.formid = formid;
    grecaptcha.execute();
}
