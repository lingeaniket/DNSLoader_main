from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mysql = MySQL()


def dashboard_ipgroup_route():
    if session.get("user_id"):
        if request.method == "GET":
            user_id = session.get("user_id")
            user_fullname = session.get("user_fullname")
            username = session.get("username")

            mycursor = mysql.connection.cursor()

            mycursor.execute(f"SELECT * FROM tblipgroups WHERE ownerid='{user_id}'")

            results = mycursor.fetchall()
            mycursor.connection.commit()

            return render_template(
                "dashboard/ipgroup/dashboard_ipgroup.html",
                result={
                    "group": results,
                    "fullname": user_fullname,
                    "username": username,
                },
            )
        elif request.method == "POST":
            group_name = request.form.get("group_name")
            user_id = session.get("user_id")
            user_fullname = session.get("user_fullname")
            username = session.get("username")

            mycursor = mysql.connection.cursor()
            mycursor.execute(
                "INSERT INTO tblipgroups(group_name,ownerid) values(%s,%s)",
                (group_name, user_id),
            )
            mycursor.execute(f"SELECT * FROM tblipgroups WHERE ownerid='{user_id}'")

            results = mycursor.fetchall()
            mycursor.connection.commit()

            return render_template(
                "dashboard/ipgroup/dashboard_ipgroup.html",
                result={
                    "group": results,
                    "fullname": user_fullname,
                    "username": username,
                },
            )
    else:
        return redirect(url_for("login"))
