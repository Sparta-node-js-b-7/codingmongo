from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.lngkyzb.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')
@app.route('/message')
def message():
   return render_template('message.html')

@app.route("/profile", methods=["POST"])
def profile_post():
    mbti_receive = request.form['mbti_give']
    birthday_receive = request.form['birthday_give']
    hobby_receive = request.form['hobby_give']
    blog_receive = request.form['blog_give']
    goal_receive = request.form['goal_give']
    doc = {
        'mbti' : mbti_receive,
        'birthday' : birthday_receive,
        'hobby' : hobby_receive,
        'blog' : blog_receive,
        'goal' : goal_receive
    }
    db.profile.insert_one(doc)
    return jsonify({'result': '저장완료!'})

@app.route("/profile", methods=["GET"])
def profile_get():
   profile_data = list(db.profile.find({},{'_id':False}).sort('_id',-1).limit(4))    
   return jsonify({'result': profile_data})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)