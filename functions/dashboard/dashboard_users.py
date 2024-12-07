from flask_mail import Mail
from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mail = Mail()
mysql = MySQL()


def dashboard_users_route():
    if request.method == "GET":

        # fetching the username and password from login session
        username = session.get("username")
        user_fullname = session.get("user_fullname")
        role = session.get("role")

        mycursor = mysql.connection.cursor()
        if not username:
            return redirect(url_for("login"))

        mycursor.execute(
            "Select *from tblusers where username=%s",
            (username,),
        )
        admin = mycursor.fetchone()
        mysql.connection.commit()

        if admin[11] == "admin":

            query = "Select *from tblusers where role='user'"
            mycursor.execute(query)
            result = mycursor.fetchall()

            mysql.connection.commit()
            return render_template(
                "dashboard/users/dashboard_users.html",
                result={
                    "result": result,
                    "fullname": user_fullname,
                    "username": username,
                    "role": role,
                },
            )

    elif request.method == "POST":
        return render_template(
            "dashboard/users/dashboard_users.html",
            result={
                "result": result,
                "fullname": user_fullname,
                "username": username,
                "role": role,
            },
        )
