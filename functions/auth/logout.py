from flask import redirect, request, url_for, session


def logout_route():
    if request.method == "GET" and session.get("user_id"):
        # remove all the session data of current user
        session.pop("username", None)
        session.pop("user_id", None)
        session.pop("user_fullname", None)
    # redirect to login page
    return redirect(url_for("login"))
