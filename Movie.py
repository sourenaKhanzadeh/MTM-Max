from flask import Flask
from flask import render_template
from flask import request
from database import cursor,db, insertUser

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "GET":
        return render_template('homepage.html')
    else:
        return "Hello"

@app.route('/create/<member>', methods=['GET', 'POST'])
def create_member(member):
    # trying to create new user
    if request.method == "GET":
        return render_template('sign_up.html', mem=member)
    else:
        # user created
        form = request.form
        admin = True if member == 'admin' else False
        insertUser(form["fname"], form["lname"], form["email"], form["username"],
                   admin=admin)
        print("User Created....")
        return render_template('sign_up.html', mem=member)


if __name__ == '__main__':
    app.run(debug=True)
    cursor.close()
    db.close()

