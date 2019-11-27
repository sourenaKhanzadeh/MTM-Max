from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import Session
from flask import send_from_directory
from database import cursor,db, insertUser, checkUserExists
import os

SESSION_TYPE = 'memcache'
app = Flask(__name__)
sess = Session()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "GET":
        return render_template('landingpage.html')
    else:
        user = request.form['user']
        typeUser = checkUserExists(user)
        exist = typeUser[0]
        admin = typeUser[1]
        if exist and admin:
            flash("Welcome admin, {}".format(user), category='success')
            return render_template('homepage.html', admin=True, user=user)
        elif exist:
            flash("Welcome user, {}".format(user))
            return render_template('homepage.html', admin=False, user=user)
        else:
            flash("Failure: Login was a failure", category='error')
            return redirect('/?login=fail')

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


@app.route('/<user>/admin', methods=['GET'])
def login(user):
    if request.method == "GET" and checkUserExists(user)[1]:
        return 'hello admin'
    else:
        flash("Page does not exist", category='error')
        redirect('/')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.secret_key = "movie_max12xs32"
    app.run(debug=True)
    cursor.close()
    db.close()

