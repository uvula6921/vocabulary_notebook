from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    words = list(db.words.find({}, {"_id": False}))
    msg = request.args.get("msg")
    return render_template("index.html", words = words, msg = msg)

@app.route('/detail/<keyword>')
def detail(keyword):
    status_receive = request.args.get("status_give")
    # API에서 단어 뜻 찾아서 결과 보내기
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token c48b847a2446b792803940b6a9d48b72acb299c7"})
    if r.status_code != 200:
        return redirect(url_for("main", msg = "단어가 이상해요 ㅜㅜ")) # main() 함수를 호출하는것, main의 template인 index.html로 가면서 msg를 파라미터로 넘겨줌
    result = r.json()
    print(result)
    return render_template("detail_jinja.html", word = keyword, result = result, status = status_receive)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive = request.form["word_give"]
    definition_receive = request.form["definition_give"]
    doc = {
        'word': word_receive,
        'definition': definition_receive
    }
    db.words.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form["word_give"]
    db.words.delete_one({"word": word_receive})
    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 삭제'})

@app.route('/api/get_examples', methods=['GET'])
def get_exs():
    word_receive = request.args.get("word_give") # get 요청이기 때문에 파라미터로 값을 받음
    result = list(db.examples.find({"word": word_receive}, {'_id': False}))
    print(word_receive, len(result))

    return jsonify({'result': 'success', 'examples': result})


@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    word_receive = request.form['word_give']
    example_receive = request.form['example_give']
    doc = {"word": word_receive, "example": example_receive}
    db.examples.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'example "{example_receive}" saved'})


@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    word_receive = request.form['word_give']
    number_receive = int(request.form["number_give"])
    target_example = list(db.examples.find({"word": word_receive}))[number_receive]
    db.examples.delete_one(target_example)
    return jsonify({'result': 'success', 'msg': f'example #{number_receive} of "{word_receive}" deleted'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)