from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mysql = MySQL()


def update_ipgroup_route():
    if request.method == "POST":
        old_name = request.form.get("old_name")
        new_name = request.form.get("new_name")
        owner_id = session.get("user_id")
        mycursor = mysql.connection.cursor()

        query = """UPDATE tblipgroups SET group_name=%s
                    WHERE group_name=%s and ownerid=%s"""

        values = (new_name, old_name, owner_id)
        mycursor.execute(query, values)

        mycursor.fetchall()
        mycursor.connection.commit()

        return redirect(url_for("dashboard_ipgroup"))
    else:
        return render_template("group_id.html")
