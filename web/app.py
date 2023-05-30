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


def save(like, dislike, fieldnames):
    with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for data in repositories[:5]:
            data['like'] = like
            data['dislike'] = dislike
            writer.writerow(data)


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
    like = 0
    dislike = 0
    fieldnames = header

    if request.method == "POST":
        is_like = request.form.get('like')
        is_dislike = request.form.get('dislike')
        like += 1
        dislike += 1

    # if request.method == "POST":
    #     has_voted = True
    #     is_like = request.form.get('like')
    #     is_dislike = request.form.get('dislike')
    #     if vote_stamp:
    #         print(("You've already voted! The vote stamp is: " + vote_stamp))
    #     else:
    #         print("You can vote!")
    #         like += 1
    #         dislike += 1

    save(like, dislike, fieldnames)
    resp = make_response(render_template("vote.html"))

    # if has_voted:
    #     vote_stamp = hex(random.getrandbits(64))[2:-1]
    #     print("Set cookie for voted")
    #     resp.set_cookie("vote_stamp", vote_stamp)

    return resp


if __name__ == "__main__":
    app.run(debug=True)
