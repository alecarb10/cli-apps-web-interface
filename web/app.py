import random

from flask import Flask, render_template, request, make_response
import csv

app = Flask(__name__)


title = "Cli Apps Web Interface"


@app.route("/")
def home():
    return render_template("home.html", title=title)


with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "r") as filecsv:
    reader = csv.DictReader(filecsv, delimiter="\t")
    header = reader.fieldnames
    repositories = []
    for data in reader:
        repositories.append(data)

def save(repositories):
    with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t")
        writer.writeheader()
        for data in repositories[:5]:
            writer.writerow(data)


like = 0
dislike = 0
@app.route("/data")
def stats():
    context = {
        "title": title,
        "header": header,
        "repositories": repositories,
    }
    return render_template("data.html", **context)


@app.route("/vote", methods=["GET", "POST"])
def vote():
    has_voted = False
    vote_stamp = request.cookies.get('vote_stamp')

    if request.method == "POST":
        has_voted = True
        vote = request.form['vote']
        if vote_stamp:
            print(("You've already voted! The vote stamp is: " + vote_stamp))
        else:
            print("You can vote!")
            vote_like = int(repositories['like'])
            vote_dislike = int(repositories['dislike'])
            vote_like += 1
            vote_dislike += 1
            save(repositories)

    resp = make_response(render_template("vote.html"))

    if has_voted:
        vote_stamp = hex(random.getrandbits(64))[2:-1]
        print("Set cookie for voted")
        resp.set_cookie("vote_stamp", vote_stamp)

    return resp


if __name__ == "__main__":
    app.run(debug=True)
