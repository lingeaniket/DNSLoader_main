from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mysql = MySQL()


def edit_ip_route():
    if request.method == "POST":
        # get old_ip as original ip and new_ip as changed ip
        old_ip = request.form.get("old_ip")
        new_ip = request.form.get("new_ip")

        # get old_comment as original comment and new_comment as changed comment
        old_comment = request.form.get("old_comment")
        new_comment = request.form.get("new_comment")

        # get onwer_id from session
        owner_id = session.get("user_id")

        # initialize the cursor
        mycursor = mysql.connection.cursor()

        # query for update the ip
        query = """UPDATE tblips SET ipaddress=%s,comments=%s
                    WHERE ipaddress=%s AND ownerid=%s AND comments=%s"""
        # get values for each variable in query
        values = (new_ip, new_comment, old_ip, owner_id, old_comment)

        # execute the query with given parameters
        mycursor.execute(query, values)
        mycursor.connection.commit()

        # after completion, redirect to ip dashboard
        return redirect(url_for("dashboard/ip/dashboard_ip"))
    else:
        return render_template("dashboard/ip/dashboard_ip.html")
