from flask import Flask
from flask import render_template
from flask import request
from database import cursor,db

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "GET":
        return render_template('homepage.html')
    else:
        return "Hello"

@app.route('/create/<member>')
def create_member(member):
    return render_template('sign_up.html', mem=member)

if __name__ == '__main__':
    app.run(debug=True)
    cursor.close()
    db.close()

