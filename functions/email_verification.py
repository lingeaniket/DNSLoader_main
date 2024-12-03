import secrets
from flask import redirect, render_template, request, url_for, session
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from itsdangerous import URLSafeTimedSerializer

mysql = MySQL()
mail = Mail()
secret_key = secrets.token_hex(16)

serializer = URLSafeTimedSerializer(secret_key=secret_key)

mysql = MySQL()


def generate_token():
    return secrets.token_hex(16)


def send_verification_email(email, username):
    token = generate_token()

    link = url_for("verify_email", token=token, _external=True)

    mycursor = mysql.connection.cursor()

    mycursor.execute(
        "UPDATE tblusers SET email_verification_token=%s WHERE email=%s", (token, email)
    )
    mycursor.connection.commit()

    msg = Message(
        subject="Email Verification",
        recipients=[email],
    )

    msg.body = (
        f"Hi '{username}' Please click the following link to verify your email: {link}"
    )
    mail.send(msg)


def verify_email_route():
    token = request.args.get("token")
    print(token)
    mycursor = mysql.connection.cursor()

    query = f"""SELECT * FROM tblusers WHERE email_verification_token='{token}'"""
    mycursor.execute(query)
    user = mycursor.fetchone()
    if user:
        id = user[0]
        email = user[3]

        session["user_id"] = id
        session["user_fullname"] = user[1] + " " + user[2]
        session["username"] = user[5]

        query = f"""UPDATE tblusers SET email_verified=1,email_verification_token=NULL where id='{user[0]}'"""
        mycursor.execute(query)
        mysql.connection.commit()
        return render_template(
            "verify_email.html", result={"is_verified": True, "email": email}
        )
    else:
        return render_template(
            "verify_email.html", result={"is_verified": False, "email": email}
        )


def resend_email_verification_route():
    if request.method == "POST":
        email = request.form.get("email")

        mycursor = mysql.connection.cursor()
        query = f"""SELECT * FROM tblusers WHERE email='{email}'"""
        mycursor.execute(query)
        result = mycursor.fetchone()

        if result:
            send_verification_email(email, result[5])

            return render_template("email_verify.html")

        else:
            return redirect(url_for("login"))
