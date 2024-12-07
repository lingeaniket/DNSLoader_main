from flask_mail import Mail, Message
from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

mail = Mail()
mysql = MySQL()


def dashboard_users_actions_route():
    if request.method == "POST":
        mycursor = mysql.connection.cursor()

        email = request.args.get("email")
        action = request.args.get("action")

        # user_fullname = session.get("user_fullname")
        # username = session.get("username")
        # role = session.get("role")

        query = "Select *from tblusers where email=%s"
        mycursor.execute(query, (email,))
        user = mycursor.fetchone()
        mysql.connection.commit()

        if user:
            if action == "Deny":
                query = "Delete from tblusers where email=%s and role=%s"
                mycursor.execute(query, (email, "user"))
                mysql.connection.commit()

            elif action == "Approved":
                msg = Message(
                    "Congrats! your request has been approved!",
                    recipients=[email],
                )
                mycursor.execute(
                    f"Update tblusers set is_approved=1,status='Active' where email='{email}'"
                )
                mysql.connection.commit()
                link = url_for("login", _external=True)
                msg.body = f"Hi {user[5]}! Your request has been approved! Kindly login here: {link}"

                mail.send(msg)

    return "0"
