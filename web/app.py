from flask import Flask, render_template, request, make_response
import csv

app = Flask(__name__)


with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "r") as filecsv:
    reader = csv.DictReader(filecsv, delimiter="\t")
    header = reader.fieldnames
    repositories = []
    for data in reader:
        data['name']
        data['like']
        data['dislike']
        repositories.append(data)


def save(like, dislike, fieldnames):
    with open("/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv", "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for data in repositories:
            data['like'] = like
            data['dislike'] = dislike
            writer.writerow(data)


title = "Cli Apps Web Interface"


@app.route("/")
def base():
    return render_template("base.html", title=title)


@app.route("/home")
def home():
    return render_template("home.html", title=title)


@app.route("/data")
def stats():
    context = {
        "title": title,
        "header": header,
        "repositories": repositories,
    }
    return render_template("data1.html", **context)


@app.route("/vote", methods=["GET", "POST"])
def vote():
    like = int(data['like'])
    dislike = int(data['dislike'])
    fieldnames = header

    if request.method == "POST":
        if request.form.get('like') == 'LIKE':
            like += 1
        elif request.form.get('dislike') == 'DISLIKE':
            dislike += 1
        else:
            pass

    context = {
        "title": title,
        "name": data['name'],
        "like": like,
        "dislike": dislike,
    }

    save(like, dislike, fieldnames)
    resp = make_response(render_template("vote1.html", **context))

    # if has_voted:
    #     vote_stamp = hex(random.getrandbits(64))[2:-1]
    #     print("Set cookie for voted")
    #     resp.set_cookie("vote_stamp", vote_stamp)

    return resp


if __name__ == "__main__":
    app.run(debug=True)
