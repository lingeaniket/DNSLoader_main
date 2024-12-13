function onSubmit(token) {
    const formData = new FormData();
    formData.append("g-recaptcha-response", token);
    fetch("/validate-recaptcha", { method: "POST", body: formData })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const formid = window.formid;
                const formel = document.getElementById(formid);
                console.log(formel);
                if (formel) {
                    formel.requestSubmit();
                }
                const loader = document.getElementById("loader");
                if (loader) {
                    loader.style.display = "block";
                }

                var buttons = document.querySelectorAll("button");
                buttons.forEach(function (btn) {
                    btn.classList.add("disabled");
                });

                setTimeout(() => {
                    var buttons = document.querySelectorAll("button");
                    buttons.forEach(function (btn) {
                        btn.classList.remove("disabled");
                    });
                }, 5000);
            } else {
                const errormsg = document.getElementById("error-message");
                if (errormsg) {
                    errormsg.innerHTML = data.message;
                }
            }
        });
}

function onload() {
    var element = document.getElementById("Submit");
    if (element) {
        element.onclick = validate;
    }
}
