function fetchips() {
    const eventsource = new EventSource("/fetch-ips-stream");
    eventsource.onmessage = function (event) {
        const { data } = JSON.parse(event.data);

        console.log(data);
    };

    eventsource.onerror = function () {
        console.error("Error occurred while streaming data");
        eventsource.close(); // Close the connection
    };
}

function callFetch(event) {
    event.preventDefault();

    fetch("/fetch-ips", { method: "POST" })
        .then((response) => {
            return response.json();
        })
        .then((response) => {
            const ips = response.ips;
            let ipdata = [];

            for (const ip in ips) {
                const statusTd = document.getElementById(`${ips[ip]}-01`);
                statusTd.innerHTML = "";
                const inSpinn = document.createElement("div");
                inSpinn.classList.add("spinner");
                statusTd.appendChild(inSpinn);
            }
            fetchips();
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
        form.action = "{{url_for('ips_add_range')}}";
    } else if (name == "custom") {
        form.action = "{{url_for('ips_add_custom')}}";
    } else if (name == "file-input") {
        form.action = "{{url_for('ips_add_csv')}}";
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
    console.log(ip_obj);
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
