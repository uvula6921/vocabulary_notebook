from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/')
def main():
    myname = "경준"
    return render_template("index.html", name = myname)


@app.route('/detail/<keyword>')
def detail(keyword):
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token c48b847a2446b792803940b6a9d48b72acb299c7"})
    result = r.json()
    print(result)
    word_receiver = request.args.get("word_give")
    print(word_receiver)
    return render_template("detail_ajax.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)