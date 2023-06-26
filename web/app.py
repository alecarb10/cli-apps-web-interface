from flask import Flask, render_template, request, make_response, redirect, url_for
import csv
import requests
import json
import base64

app = Flask(__name__)


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


def save_like(like, fieldnames):
    with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for data in repositories:
            data['like'] = like
            writer.writerow(data)


def save_users(users):
    with open("../files/users.csv", "a") as userscsv:
        fieldnames = ['username', 'password', 'timestamp']
        writer = csv.DictWriter(userscsv, delimiter="\t", fieldnames=fieldnames)
        writer.writerow(users)

with open("../files/users.csv", "r", encoding="utf-8") as readusers:
    reader = csv.DictReader(readusers, delimiter="\t")
    accounts = []
    for row in reader:
        accounts.append(row)

title = "Cli Apps Web Interface"


@app.route("/")
def base():
    return render_template("base.html", title=title)


@app.route("/home")
def home():
    return render_template("home.html", title=title)


@app.route("/data", methods=["GET", "POST"]) # Manca il salvataggio del numero di like
def stats():
    i = 0
    for repo in repositories:
        if request.form.get(repo['git']) == 'LIKE':
            repositories[i]['like'] = int(repositories[i]['like']) + 1
            i += 1
        else:
            i += 1
            pass

    context = {
        "title": title,
        "header": header,
        "repositories": repositories,
    }

    # save(repositories[i]['like'], header)
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
            message = "<p style='color: green;'>Your account has been submitted successfully!</p>"  # Show the user if reCAPTCHA is valid
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

    error = None

    for account in accounts:
        if request.method == "POST":
            input_password = str(base64.b64encode(request.form['password'].encode("utf-8")))
            if request.form['username'] != account['username'] \
                    or input_password != account['password']:
                error = "Invalid Credentials. Please try again."
            else:
                return redirect(url_for('stats'))

    context = {
        # "message": message,
        "error": error,
    }

    resp = make_response(render_template("login.html", **context))

    return resp


if __name__ == "__main__":
    app.run(debug=True)


# sign up -> prima iscrizione
# sign in -> successivi login
