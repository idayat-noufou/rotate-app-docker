from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://superadmin:superadmin@localhost:5432/rotate')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Image {self.name}>'

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html', img_url='https://attic.sh/b2foeufhqfnkv5svkgdh47ejpkgh')

@app.route('/<name>')
def homeWithName(name):
    image = Image.query.filter_by(name=name).first()

    if image:
        img_url = image.url
    else:
        img_url = 'https://w7.pngwing.com/pngs/658/622/png-transparent-page-not-found-illustration-thumbnail.png'

    return render_template('index.html', img_url=img_url)

@app.route('/saveUrl', methods=['POST'])
def saveUrl():
    name = request.form['name']
    url = request.form['url']

    new_image = Image(name=name, url=url)
    db.session.add(new_image)
    db.session.commit()

    return redirect(url_for('homeWithName', name=name))

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
