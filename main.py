
# connect to socket.io

from flask import Flask, request, render_template, jsonify

from pip._internal.vcs import git
import git
from pymongo import MongoClient
import os

app = Flask(__name__)


@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./onlineAuctionAPI')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200


@app.route('/')
def hello_world():

    return jsonify({"status": "ok", "message": "send here a link to the sign up page"})


@app.route('/signup', methods=['POST'])
def signup():
    # might need to change to form not args
    info = request.args
    if info["password"] == info["password2"] and info["name"] and info["email"] and info["password"] and info["password2"]:
        password = os.environ.get("password")
        link = 'mongodb+srv://yakov:' + password + '@cluster0.irzzw.mongodb.net/myAuctionDB?retryWrites=true&w=majority'
        client = MongoClient(link)
        db = client.get_database('myAuctionDB')
        users = db.users
        if not users.find_one({'email': info["email"]}):
            user = {
                "name": info["name"],
                "email": info["email"],
                "password": info["password"],
                "sales": [],
                "offers": [],
                "saved": []
            }
            users.insert_one(user)
            return jsonify({"status": "ok", "message": " welcome to {} {} ".format(info["name"], info["email"])})
        else:
            return jsonify({"status": "error", "message": "you already exist"})
    else:
        return jsonify({"status": "error", "message": "you are missing some arguments"})


@app.route('/signin')
def signin():
    # might need to change to form not args
    info = request.args
    password = os.environ.get("password")
    link = 'mongodb+srv://yakov:' + password + '@cluster0.irzzw.mongodb.net/myAuctionDB?retryWrites=true&w=majority'
    client = MongoClient(link)
    db = client.get_database('myAuctionDB')
    users = db.users
    if users.find_one({'email': info["email"], 'password': info["password"]}):
        return jsonify({"status": "ok", "message": " welcome, here i need a link to the website, for render :)"})
    else:
        return jsonify({"status": "error", "message": "you dont exist, i need a link to the sign up page"})


@app.route('/sales')
def sales():
    password = os.environ.get("password")
    link = 'mongodb+srv://yakov:' + password + '@cluster0.irzzw.mongodb.net/myAuctionDB?retryWrites=true&w=majority'
    client = MongoClient(link)
    db = client.get_database('myAuctionDB')
    sales = db.sales
    results = []
    for s in sales.find({}, {"_id": 0}).limit(10):
        results.append(s)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)