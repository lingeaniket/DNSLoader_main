from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mysql = MySQL()


def delete_ipgroup_route():
    print(request.method)
    if request.method == "POST":
        owner_id = session.get("user_id")
        delete_group = request.form.get("delete_group")
        mycursor = mysql.connection.cursor()

        query = """DELETE FROM tblipgroups WHERE id=%s AND ownerid=%s AND NOT EXISTS (SELECT 1 FROM tblips WHERE ipgroup=%s)"""
        mycursor.execute(query, (delete_group, owner_id, delete_group))
        # mycursor.execute(query)
        mycursor.fetchall()
        mycursor.connection.commit()

        return redirect(url_for("dashboard_ipgroup"))
    else:
        return redirect(url_for("dashboard_ipgroup"))
