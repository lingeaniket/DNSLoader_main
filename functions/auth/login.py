import bcrypt

from flask import redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL

mysql = MySQL()


def login_route():
    # if user is already logged in, redirect to profile
    if session.get("user_id"):
        return redirect(url_for("dashboard_profile"))
    elif request.method == "GET":
        # for "GET" request render login template
        return render_template("auth/login.html")
    elif request.method == "POST":
        # get data from form
        username = request.form.get("username")  # username entered
        password = request.form.get("password")  # password entered

        mycursor = mysql.connection.cursor()  # start the cursor
        # execute the query to find is user is registred with given username or email address
        mycursor.execute(
            f"Select *from tblusers where username='{username}' or email='{username}'"
        )
        user = mycursor.fetchone()  # fetch the result

        if not user:  # means user is not found in the database
            # return error message
            return render_template("login.html", result={"error": "User not found!"})

        # convert the db password to "utf-8" string, to avoid problems with bcrypt
        hash_password = user[4].encode("utf-8")

        password = password.encode("utf-8")

        # check the user's entered password matches with db's stored password
        result = bcrypt.checkpw(password, hash_password)

        if result:  # if the password matches
            # check if user's email is verified and it is approved by admin

            # store required data in the session
            # myresult = ((Id, Firstname, Lastname, email, password, username))
            session["user_id"] = user[0]  # store user_id in session
            # store user_fullname in session, concat firstname and lastname
            session["user_fullname"] = user[1] + " " + user[2]
            session["username"] = user[5]  # store username in session
            # after successful login, redirect to dashboard
            return redirect(url_for("dashboard_ip"))
        # if password does not matches, return error as "Invalid Credentials!!"
        return render_template(
            "auth/login.html", result={"error": "Invalid Credentials!!"}
        )