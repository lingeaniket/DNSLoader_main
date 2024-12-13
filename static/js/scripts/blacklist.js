function onSubmit(token) {
    const formData = new FormData();
    formData.append("g-recaptcha-response", token);
    const form = document.createElement("form");
    fetch("/validate-recaptcha", { method: "POST", body: formData })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                form.action = "/ip-blacklist";
                form.method = "POST";
                const recaptchaInput = document.createElement("input");
                recaptchaInput.value = document.getElementById("ip").value;
                recaptchaInput.name = "ip";
                form.appendChild(recaptchaInput);
                document.body.appendChild(form);
                form.submit();
                document.getElementById("loader").style.display = "block";
                var buttons = document.querySelectorAll("button");
                buttons.forEach(function (btn) {
                    btn.classList.add("disabled");
                });
                document.body.removeChild(form);
            } else {
                document.getElementById("error-message").innerHTML = data.message;
            }
        })
        .catch((e) => {
            console.log(e);
        });
}
function validate(event) {
    event.preventDefault();
    if (!document.getElementById("ip").value) {
        alert("You must add text to the required field");
    } else {
        grecaptcha.execute();
    }
}
function onload() {
    var element = document.getElementById("submit");
    element.onclick = validate;
}
