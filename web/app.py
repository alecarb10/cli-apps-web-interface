from flask import Flask, render_template
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


@app.route("/data")
def results():
    context = {
        "title": title,
        "header": header,
        "repositories": repositories,
    }
    return render_template("data.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
