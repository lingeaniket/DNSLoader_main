function onSubmit(token) {
    console.log(token);
    const formData = new FormData();
    formData.append("g-recaptcha-response", token);
    const form = document.createElement("form");
    fetch("/validate-recaptcha", { method: "POST", body: formData })
        .then((response) => response.json())
        .then((data) => {
            // console.log(data);
            if (data.success) {
                const formtosubmit = document.getElementById("loginForm");
                formtosubmit.submit();
            } else {
                // document.getElementById("error-message").innerHTML = data.message;
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
