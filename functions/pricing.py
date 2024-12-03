from flask import render_template


def pricing_route():
  return render_template("pricing.html")