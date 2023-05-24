from flask import Flask, render_template, request
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


@app.route("/data", methods=["GET", "POST"])
def stats():
    context = {
        "title": title,
        "header": header,
        "repositories": repositories,
    }
    return render_template("data.html", **context)


like = 0
dislike = 0
@app.route("/vote", methods=["GET", "POST"])
def button():
    if request.method == "POST":
        return render_template("vote.html", like=like+1, dislike=dislike+1)
    return render_template("vote.html", like=like, dislike=dislike)


if __name__ == "__main__":
    app.run(debug=True)
