from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

import pymongo
import json

ca = certifi.where() 
client = MongoClient('mongoDB url 입력')
db = client.dbsparta



@app.route("/")

def home():
   return render_template('index.html')


@app.route("/members", methods=["GET"])
def member_get():
    all_members = list(db.members.find({},{'_id':False}))
    return jsonify({'result':all_members})



@app.route("/reply", methods=["GET"])
def reply_get():
    all_reply = list(db.reply.find({},{'_id':False}))
    return jsonify({'result':all_reply})


@app.route("/update", methods=["POST"]) #/rely로 받음
def modify_post():
   name_receive = request.form['name_give']
   desc1_receive = request.form['desc1_give']
   desc2_receive = request.form['desc2_give']
   desc3_receive = request.form['desc3_give']
     
   myquery = {"name":name_receive}
   newvalue1 = {"$set":{"description1":desc1_receive}}
   newvalue2 = {"$set":{"description2":desc2_receive}}
   newvalue3 = {"$set":{"description3":desc3_receive}}

   db.members.update_one(myquery,newvalue1)
   db.members.update_one(myquery,newvalue2)
   db.members.update_one(myquery,newvalue3)

   return jsonify({'msg':'수정완료!'})


@app.route('/getcomments',methods=['GET'])
def getComments():
    name_receive = str(request.args.get('name'))
    ct = list(db.project_2_comments.find({'name':name_receive},{'_id':False}))
    
    return jsonify({'result':ct})

@app.route('/addcomments',methods=['POST'])
def addComments():
    name_receive = request.form['name_give']
    cid_receive = request.form['cid_give']
    text_receive = request.form['text_give']
    
    doc = {
        'name' : name_receive,
        'cid' : cid_receive,
        'text' : text_receive
    }
    
    db.project_2_comments.insert_one(doc)
    
    return jsonify({'result':'댓글 등록 성공'})

@app.route('/updatecomments',methods=['PUT'])
def updateComments():
    #name_receive = request.args.get('name')
    #cid_receive = request.args.get('cid')
    name_receive = request.form['name_give']
    cid_receive = request.form['cid_give']
    text_receive = request.form['text_give']
    
    print(name_receive)
    print(cid_receive)
    print(text_receive)
    db.project_2_comments.update_one(
        {'name':name_receive, 'cid':cid_receive},
        {"$set": {
            'text': text_receive
        }}
    )
    
    return jsonify({'result':'댓글 수정 성공'})

@app.route('/deletecomments',methods=['DELETE'])
def deleteComments():
    name_receive = request.args.get('name')
    cid_receive = request.args.get('cid')
    
    db.project_2_comments.delete_one(
        {'name':name_receive, 'cid':cid_receive}
    )
    
    return jsonify({'result':'댓글 삭제 성공'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5002, debug=True)