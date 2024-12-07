import bcrypt

from flask import redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

from functions.mail.email_verification import send_verification_email

mysql = MySQL()


def registration_route():
    # if user is already logged in, redirect to profile
    if session.get("user_id"):
        return redirect(url_for("dashboard_profile"))
    elif request.method == "GET":  # if method is GET, render registration.html template
        return render_template("auth/registration.html")
    elif request.method == "POST":
        # get all form data from form
        username = request.form.get("username")  # get username
        firstname = request.form.get("firstname")  # get firstname
        lastname = request.form.get("lastname")  # get lastname
        email = request.form.get("email")  # get email
        password = request.form.get("password")  # get password
        confirm_password = request.form.get("confirm_password")  # get confirm_password

        # to check whether password matches with confirmation password
        if password != confirm_password:
            # if not matches render template with error message
            return render_template(
                "registration.html",
                result={"error": "Current password does'nt match with password"},
            )
        # password and confirm_password matches
        mycursor = mysql.connection.cursor()  # start the cursor
        # execute the query to find is there any user with given username and email
        mycursor.execute(
            f"Select *from tblusers where username='{username}' OR email='{email}'"
        )

        myresult = mycursor.fetchall()  # fetch the result

        if myresult.__len__() > 0:  # if length > 0 then user is already registred
            # print("Is available")
            # render template with given error
            return render_template(
                "auth/registration.html",
                result={"error": "Username or email already exists"},
            )

        salt = bcrypt.gensalt(rounds=12)  # create a salt with rounds=12

        # hash the password with bcrypt algorithm and salt
        hash_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        # print(hash_password)
        # execute the query to insert given data into the database
        mycursor.execute(
            """ Insert into tblusers(firstname,lastname,email,username,password) values(%s,%s,%s,%s,%s)""",
            (firstname, lastname, email, username, hash_password),
        )

        # again, execute the query to get currently added user
        mycursor.execute(f"Select *from tblusers where username='{username}' ")

        mysql.connection.commit()  # close connection

        send_verification_email(email, username)
        session["email_verify"] = email

        # after successful creation of user, redirect to the dashboard
        return redirect(url_for("email_verification"))
