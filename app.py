import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, 
            static_folder=os.path.join(base_dir, 'static'), 
            template_folder=os.path.join(base_dir, 'templates'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'guestbook.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.date_posted.desc()).all()
    # 타이틀과 안내 문구를 변수로 전달합니다.
    return render_template('index.html', 
                           entries=entries, 
                           title="충청남도의원 예비후보 전성일",
                           subtitle="우리 동네 불편한 점을 적어주세요")

@app.route('/add', methods=['POST'])
def add_entry():
    name = request.form.get('name')
    content = request.form.get('content')
    if name and content:
        new_entry = Entry(name=name, content=content)
        db.session.add(new_entry)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)