import datetime
import secrets
from flask import redirect, render_template, request, url_for, session
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from itsdangerous import URLSafeTimedSerializer
import os

mysql = MySQL()
mail = Mail()
secret_key = secrets.token_hex(16)

serializer = URLSafeTimedSerializer(secret_key=secret_key)

mysql = MySQL()


def generate_token():
    return secrets.token_hex(16)


def send_verification_email(email, username):
    token = generate_token()

    new_date = datetime.datetime.today() + datetime.timedelta(minutes=30)
    expiry_date = new_date.strftime("%Y-%m-%d %H:%M:%S")

    # _external= True, if link has to add link feature with geeting domain
    link = url_for("verify_email", token=token, _external=False)
    domain = os.getenv("DOMAIN")
    link = f"{domain}{link}"

    mycursor = mysql.connection.cursor()

    mycursor.execute(
        "UPDATE tblusers SET email_verification_token=%s, email_verification_token_expiry=%s WHERE email=%s",
        (token, expiry_date, email),
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
    mycursor = mysql.connection.cursor()

    query = f"""SELECT * FROM tblusers WHERE email_verification_token='{token}'"""
    mycursor.execute(query)
    user = mycursor.fetchone()
    if user:
        id = user[0]
        email = user[3]
        username = user[5]
        fullname = user[1] + " " + user[2]
        date = datetime.datetime.today()
        recent_date = date.strftime("%Y-%m-%d %H:%M:%S")

        recent_date_obj = datetime.datetime.strptime(recent_date, "%Y-%m-%d %H:%M:%S")
        given_date_obj = user[6]
        if given_date_obj < recent_date_obj:
            return render_template(
                "email-verification-template/email-verification-template.html",
                result={
                    "type": "expired",
                    "mode": "token-expired",
                    "email": email,
                },
            )

        # session["user_id"] = id
        # session["user_fullname"] = fullname
        # session["username"] = username

        query = f"""UPDATE tblusers SET email_verified=1,email_verification_token=NULL where id='{user[0]}'"""
        mycursor.execute(query)
        mysql.connection.commit()
        return render_template(
            "email-verification-template/email-verification-template.html",
            result={"type": "verified", "fullname": fullname, "username": username},
        )
    else:
        return render_template(
            "email-verification-template/email-verification-template.html",
            result={
                "type": "expired",
                "mode": "no-user-found",
            },
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

            return render_template(
                "email-verification-template/email-verification-template.html",
                result={"type": "after-register", "email": email},
            )

        else:
            return redirect(url_for("login"))
