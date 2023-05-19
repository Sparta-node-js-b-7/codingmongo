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

@app.route('/post_member')
def post_member():
   return render_template('postmember.html')

@app.route('/create_member')
def create_member():
   return render_template('create.html')

@app.route("/members-info", methods=["POST"])
def members_info():
    name_receive = request.form['name_give']
    mbti_receive = request.form['mbti_give']
    birthday_receive = request.form['birthday_give']
    hobby_receive = request.form['hobby_give']
    blog_receive = request.form['blog_give']
    goal_receive = request.form['goal_give']
    
    doc = {
      'name': name_receive,
      'mbti':mbti_receive,
      'birthday' : birthday_receive,
      'hobby': hobby_receive,
      'blog': blog_receive,
      'goal': goal_receive,
      'memberId' : name_receive.lower()
      }
    db.members.insert_one(doc)
    return jsonify({'result': '생성 완료!'})

@app.route("/members", methods=["GET"])
def get_members():
    all_members = list(db.members.find({},{'_id':False}))
    return jsonify({'result': all_members})

@app.route("/members/<name>", methods=["GET"])
def member_get(name):
    member_data = db.members.find_one({'name': name},{'_id':False})
    return jsonify({'result': member_data})

@app.route("/members/<name>", methods=["DELETE"])
def member_delete(name):
    db.members.delete_one({'name': name})
    return jsonify({'result':'삭제 완료!'})

@app.route("/teams", methods=["GET"])
def teams_get():
    team_info = list(db.teams.find({},{'_id':False}))  
    return jsonify({'result': team_info})

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

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)