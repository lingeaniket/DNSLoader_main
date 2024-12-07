function onSubmit(token) {
    const formData = new FormData();
    formData.append("g-recaptcha-response", token);
    const form = document.createElement("form");
    fetch("/validate-recaptcha", { method: "POST", body: formData })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const formToSubmit = document.getElementById("form-to-submit");
                formToSubmit.submit();

                document.getElementById("loader").style.display = "block";
                var buttons = document.querySelectorAll("button");
                buttons.forEach(function (btn) {
                    btn.classList.add("disabled");
                });
                document.body.removeChild(form);
            } else {
                document.getElementById("error-message").innerHTML = data.message;
            }
        });
}
function validate(event) {
    event.preventDefault();
    if (!document.getElementById("domain").value) {
        alert("You must add text to the required field");
    } else {
        console.log("grecaptcha validation started");
        grecaptcha.execute();
    }
}
function onload() {
    var element = document.getElementById("Submit");
    element.onclick = validate;
}
