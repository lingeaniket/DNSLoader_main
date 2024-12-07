from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mysql = MySQL()


def dashboard_ip_route():
    # if user is not logged in, redirect to login page
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # if user is logged in
    elif session.get("user_id"):
        if request.method == "GET":

            # get user_id, user_fullname, username from session
            user_id = session.get("user_id")
            user_fullname = session.get("user_fullname")
            username = session.get("username")
            role = session.get("role")

            # initialize the cursor
            mycursor = mysql.connection.cursor()

            mycursor.connection.commit()
            # execute the query to get all ips of respected user,
            # adds ipgroup_name to the list as ipgroup name of that ip
            mycursor.execute(
                f"""SELECT tblips.*, tblipgroups.group_name AS ipgroup_name
                    FROM tblips
                    LEFT JOIN tblipgroups ON tblips.ipgroup = tblipgroups.id
                    WHERE tblips.ownerid ='{user_id}'"""
            )
            results = mycursor.fetchall()

            mycursor.execute(f"SELECT * FROM tblipgroups WHERE ownerid='{user_id}'")
            groups = mycursor.fetchall()
            mycursor.connection.commit()

            groups_obj = []
            for group in groups:
                groups_obj.append({"id": group[0], "name": group[1]})

            # render the template with results
            return render_template(
                "dashboard/ip/dashboard-ip.html",
                result={
                    "Ips": results,
                    "ip_group": groups_obj,
                    "fullname": user_fullname,
                    "username": username,
                    "role": role,
                },
            )


def dashboard_ip_list_route():
    if request.method == "GET":

        # get user_id, user_fullname, username from session
        user_id = session.get("user_id")
        user_fullname = session.get("user_fullname")
        username = session.get("username")
        role = session.get("role")

        # initialize the cursor
        mycursor = mysql.connection.cursor()

        mycursor.connection.commit()
        # execute the query to get all ips of respected user,
        # adds ipgroup_name to the list as ipgroup name of that ip
        mycursor.execute(
            f"""SELECT tblips.*, tblipgroups.group_name AS ipgroup_name
                    FROM tblips
                    LEFT JOIN tblipgroups ON tblips.ipgroup = tblipgroups.id
                    WHERE tblips.ownerid ='{user_id}'"""
        )
        results = mycursor.fetchall()

        mycursor.execute(f"SELECT * FROM tblipgroups WHERE ownerid='{user_id}'")
        groups = mycursor.fetchall()
        mycursor.connection.commit()

        groups_obj = []
        for group in groups:
            groups_obj.append({"id": group[0], "name": group[1]})

        # render the template with results
        return render_template(
            "dashboard/ip/dashboard-ip.html",
            result={
                "Ips": results,
                "ip_group": groups_obj,
                "fullname": user_fullname,
                "username": username,
                "role": role,
            },
        )
