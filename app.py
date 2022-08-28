from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserPostMessage.db'
db = SQLAlchemy(app)


class UserPostMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<PostMessage %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        post_content = request.form['content']
        new_message = UserPostMessage(content=post_content)

        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your post'

    else:
        posts = UserPostMessage.query.order_by(UserPostMessage.date_created).all()
        return render_template('index.html', posts = posts)


@app.route('/delete/<int:id>')
def delete(id):
    message_to_delete = UserPostMessage.query.get_or_404(id)

    try:
        db.session.delete(message_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that post'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    postmessage = UserPostMessage.query.get_or_404(id)

    if request.method == 'POST':
        postmessage.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your post'

    else:
        return render_template('update.html', postmessage=postmessage)


if __name__ == "__main__":
    app.run(debug=True)
