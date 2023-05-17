from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.2vnjgxh.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/messages')
def messages():
   return render_template('messages.html')

@app.route('/team')
def team():
   return render_template('team.html')

@app.route('/member')
def member():
   return render_template('member.html')

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name' : name_receive,
        'comment' : comment_receive
    }
    db.messages.insert_one(doc)
    return jsonify({'result': '저장완료!'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    recent_comments = list(db.messages.find({},{'_id':False}).sort('_id',-1).limit(4))  
    return jsonify({'result': recent_comments})

@app.route("/teams", methods=["GET"])
def teams_get():
    team_info = list(db.teams.find({},{'_id':False}))  
    return jsonify({'result': team_info})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)