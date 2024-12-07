from flask import redirect, render_template, session, url_for


def dashboard_profile_route():
    user_id = session.get("user_id")
    user_fullname = session.get("user_fullname")
    username = session.get("username")
    role = session.get("role")
    print(role)
    if user_id:
        return render_template(
            "dashboard/profile/dashboard-profile.html",
            result={"fullname": user_fullname, "username": username, "role": role},
        )
    redirect(url_for("login"))
