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

            page = int(request.args.get("page", 1))  # Default page is 1
            per_page = int(request.args.get("per_page", 100))  # Default per_page is 100

            offset = (page - 1) * per_page

            # initialize the cursor
            mycursor = mysql.connection.cursor()

            mycursor.connection.commit()
            # execute the query to get all ips of respected user,
            # adds ipgroup_name to the list as ipgroup name of that ip
            mycursor.execute(
                f"""SELECT tblips.*, tblipgroups.group_name AS ipgroup_name
                    FROM tblips
                    LEFT JOIN tblipgroups ON tblips.ipgroup = tblipgroups.id
                    WHERE tblips.ownerid ='{user_id}' ORDER BY id ASC LIMIT {per_page} OFFSET {offset}"""
            )
            results = mycursor.fetchall()
            mycursor.connection.commit()

            mycursor.execute(f"""SELECT id FROM tblips WHERE ownerid ='{user_id}'""")

            total_pages_len = mycursor.fetchall()
            mycursor.connection.commit()

            mycursor.execute(f"SELECT * FROM tblipgroups WHERE ownerid='{user_id}'")
            groups = mycursor.fetchall()
            mycursor.connection.commit()

            groups_obj = []
            for group in groups:
                groups_obj.append({"id": group[0], "name": group[1]})

            # render the template with results

            total_pages = 0

            total_res = len(total_pages_len) / per_page
            is_greater = int(total_res) < total_res
            if is_greater:
                total_pages = int(len(total_pages_len) / per_page) + 1
            else:
                total_pages = int(total_res)

            return render_template(
                "dashboard/ip/dashboard-ip.html",
                result={
                    "page": page,
                    "total_pages": total_pages,
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
