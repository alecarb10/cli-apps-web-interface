from flask import Flask, render_template, request, \
    make_response, redirect, url_for, flash, session
import csv
import requests
import json
import base64
from datetime import datetime


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "r") as filecsv:
    reader = csv.DictReader(filecsv, delimiter="\t")
    header = reader.fieldnames
    repositories = []
    names = []
    gits = []
    for data in reader:
        data['like']
        gits.append(data['git'])
        names.append(data['name'])
        repositories.append(data)


def save_like(repo, like, fieldnames):
    with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for data in repositories:
            if repo == data['git']:
                data['like'] = like
                writer.writerow(data)
            else:
                writer.writerow(data)


def save_users(users):
    with open("../files/users.csv", "a") as userscsv:
        fieldnames = ['username', 'password', 'timestamp']
        writer = csv.DictWriter(userscsv, delimiter="\t", fieldnames=fieldnames)
        writer.writerow(users)


with open("../files/users.csv", "r") as readusers:
    reader = csv.DictReader(readusers, delimiter="\t")
    accounts = []
    for row in reader:
        accounts.append(row)


def user_liked(liked):
    with open("../files/user_liked.csv", "a") as likedcsv:
        fieldnames = ['username', 'git_liked', 'timestamp']
        writer = csv.DictWriter(likedcsv, delimiter="\t", fieldnames=fieldnames)
        writer.writerow(liked)


with open("../files/user_liked.csv", "r") as readliked:
    reader = csv.DictReader(readliked, delimiter="\t")
    liked = []
    for row in reader:
        liked.append(row)


title = "Cli Apps Web Interface"


@app.route("/")
def base():
    session['logged_in'] = False
    return render_template("base.html", title=title)


@app.route("/home")
def home():
    return render_template("home.html", title=title)


@app.route("/data", methods=["GET", "POST"])
def stats():
    i = 0

    if request.method == "POST":
        if session['logged_in'] is True:
            for repo in repositories:
                if request.form.get(repo['git']) == 'LIKE':
                    repo['like'] = int(repo['like']) + 1
                    user_liked({"username": session['username'],
                                "git_liked": repo['git'],
                                "timestamp": str(datetime.now())})
                    save_like(request.form.get(repo['git']), repo['like'], header)
                    i += 1
                else:
                    i += 1
                    pass
        else:
            for repo in repositories:
                if request.form.get(repo['git']) == 'LIKE':
                    secret_key = open("../../recaptcha_private_key", "r").read()
                    captcha_response = request.form.get("g-recaptcha-response")
                    user_ip = request.remote_addr

                    captcha_url = f'''https://www.google.com/recaptcha/api/siteverify?secret={secret_key}&response={captcha_response}&remoteip={user_ip}'''

                    response_data = requests.get(captcha_url).text
                    parsed_data = json.loads(response_data)

                    if parsed_data["success"] is False:
                        flash('You dont submit the recaptcha')
                    else:
                        repo['like'] = int(repo['like']) + 1
                        user_liked({"username": user_ip,
                                    "git_liked": repo['git'],
                                    "timestamp": str(datetime.now())})
                        save_like(request.form.get(repo['git']), repo['like'], header)
                        i += 1
                else:
                    i += 1
                    pass

    context = {
        "header": header,
        "repositories": repositories,
    }

    resp = make_response(render_template("data1.html", **context))

    return resp


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    message = ""

    if request.method == "POST":
        encoded_psw = base64.b64encode(request.form['password'].encode("utf-8"))

        secret_key = open("../../recaptcha_private_key", "r").read()
        captcha_response = request.form.get("g-recaptcha-response")
        user_ip = request.remote_addr

        captcha_url = f'''https://www.google.com/recaptcha/api/siteverify?secret={secret_key}&response={captcha_response}&remoteip={user_ip}'''

        response_data = requests.get(captcha_url).text
        parsed_data = json.loads(response_data)

        if parsed_data['success']:
            for account in accounts:
                if request.form['username'] == account['username']:
                    flash('Account already created')
                    return redirect(url_for('sign_up'))
                else:
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    flash('Your account has been submitted successfully!')  # Show the user if reCAPTCHA is valid
                    save_users({"username": request.form['username'],
                                "password": encoded_psw,
                                "timestamp": parsed_data['challenge_ts']})
                    return redirect(url_for('stats'))
        else:
            message = "<p style='color: red;'>Invalid reCAPTCHA</p>"  # Show error if the reCAPTCHA is invalid

    context = {
        "message": message,
    }

    resp = make_response(render_template("sign_up.html", **context))

    return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    for account in accounts:
        if request.method == "POST":
            input_password = str(base64.b64encode(request.form['password'].encode("utf-8")))
            if request.form['username'] != account['username'] \
                    or input_password != account['password']:
                error = "Invalid Credentials. Please try again."
            else:
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('stats'))

    context = {
        # "message": message,
        "error": error,
    }

    resp = make_response(render_template("login.html", **context))

    return resp


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


# message = ""

    # if request.method == "POST":
    #     secret_key = open("../../recaptcha_private_key", "r").read()
    #     captcha_response = request.form.get("g-recaptcha-response")
    #     user_ip = request.remote_addr
    #
    #     captcha_url = f'''https://www.google.com/recaptcha/api/siteverify?secret={secret_key}&response={captcha_response}&remoteip={user_ip}'''
    #
    #     response_data = requests.get(captcha_url).text
    #     parsed_data = json.loads(response_data)
    #
    #     if parsed_data['success']:
    #         message = "<p style='color: green;'>Your form has been submitted successfully!</p>"  # Show the user if reCAPTCHA is valid
    #         return redirect(url_for('stats'))
    #     else:
    #         message = "<p style='color: red;'>Invalid reCAPTCHA</p>"  # Show error if the reCAPTCHA is invalid
