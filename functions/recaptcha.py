import requests

from flask import jsonify, request


def validate_recaptcha_route():
    recaptcha_response = request.form.get("g-recaptcha-response")

    # Verify the reCAPTCHA token with Google API
    data = {
        "secret": "6Lf1ZE4qAAAAAFLwY-REEvuFI6wL921ub-nOMOgd",
        "response": recaptcha_response,
    }
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    result = r.json()

    if result["success"]:
        # Return a JSON response with a redirect URL after successful form submission
        return jsonify(success=True)
    else:
        # Send an error message to the frontend
        return jsonify(success=False, message="Invalid reCAPTCHA. Please try again.")
