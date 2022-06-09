from flask import jsonify
from funcs import checkuser, connect


def mySales(request):
    info = request.json
    db = connect()
    users = db.users
    sales = db.sales
    if checkuser(info.get("email"), info.get("password"), users):
        mysales = []
        user = users.find_one({'email': info.get("email"), 'password': info.get("password")})
        mysalesid = user["sales"]
        if not mysalesid:
            return jsonify({"status": "error", "message": "you did not create a sale yet"})
        for id in mysalesid:
            sale = sales.find_one({"saleid": float(id)}, {"_id": 0})
            if not sale:
                continue
            sale["isadmin"] = True
            sale["offers"] = False
            sale["saved"] = False
            if sale["saleid"] in user["saved"]:
                sale["saved"] = True
            if sale["saleid"] in user["offers"]:
                sale["offers"] = True
            mysales.append(sale)
        response = {"status": "success", "message": mysales}
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "I don't recognize you"})


def mySaved(request):
    info = request.json
    db = connect()
    users = db.users
    sales = db.sales
    if checkuser(info.get("email"), info.get("password"), users):
        mysaved = []
        user = users.find_one({'email': info.get("email"), 'password': info.get("password")})
        mysavedid = user["saved"]
        if not mysavedid:
            return jsonify({"status": "error", "message": "you have no saved sales"})
        for id in mysavedid:
            sale = sales.find_one({"saleid": float(id)}, {"_id": 0})
            if not sale:
                continue
            sale["isadmin"] = False
            sale["offers"] = False
            sale["saved"] = True
            if sale["saleid"] in user["sales"]:
                sale["isadmin"] = True
            if sale["saleid"] in user["offers"]:
                sale["offers"] = True
            mysaved.append(sale)
        response = {"status": "success", "message": mysaved}
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "I don't recognize you"})


def myOffers(request):
    info = request.json
    db = connect()
    users = db.users
    sales = db.sales
    if checkuser(info.get("email"), info.get("password"), users):
        myoffers = []
        user = users.find_one({'email': info.get("email"), 'password': info.get("password")})
        myoffersid = user["offers"]
        if not myoffersid:
            return jsonify({"status": "error", "message": "you did not bid on a sale yet"})
        for id in myoffersid:
            sale = sales.find_one({"saleid": float(id)}, {"_id": 0})
            if not sale:
                continue
            sale["isadmin"] = False
            sale["offers"] = True
            sale["saved"] = False
            if sale["saleid"] in user["saved"]:
                sale["saved"] = True
            if sale["saleid"] in user["sales"]:
                sale["isadmin"] = True
            myoffers.append(sale)
        response = {"status": "success", "message": myoffers}
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "I don't recognize you"})