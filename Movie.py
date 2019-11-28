from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import Session
from flask import send_from_directory
from database import cursor,db, insertUser, checkUserExists,insertPorduct
from poster import Poster
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
            return render_template('homepage.html', header=True, admin=True, user=user)
        elif exist:
            flash("Welcome user, {}".format(user))
            return render_template('homepage.html', header=True, admin=False, user=user)
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
        flash("User Created....")
        return render_template('sign_up.html', mem=member)


@app.route('/<user>/products', methods=['GET', 'POST'])
def product(user):
    cursor.execute("SELECT * FROM product")
    return render_template('product.html',user=user,
                           header=True, query=cursor.fetchall(), prod=True)

@app.route('/<user>/admin', methods=['GET', 'POST'])
def login(user):
    if request.method == "GET" and checkUserExists(user)[1]:
        return render_template('admin.html',
                               header=True,
                               click_a=True,
                               admin=True,
                               user=user)
    elif request.method == "POST":
        form = request.form

        year = '{1}-{0}-01'.format(form['month'], form['year'])
        poster = Poster(form['name'])

        vals = (form['name'], int(form['len']),form['des'],
                form['genre'],float(form['price']), form['rating'],
                form['tomato'], year, form['country'])

        vals += str(poster.poster_path()),

        print(vals)
        product_id = insertPorduct(vals)

        if form['type'] == 'm':
            cursor.execute("""
            INSERT INTO movie(MovieID)VALUES({})
            """.format(product_id))
        elif form['type'] == 't':
            cursor.execute("""
                        INSERT INTO tvseries(SeriesID, Seasons, Episodes)VALUES(%s,%s,%s)
                        """, (product_id, 0, 0))
        else:
            cursor.execute("""
                    INSERT INTO music(SongID)VALUES({})
                    """.format(product_id))
        db.commit()
        flash("Product Added!!")
        return render_template('admin.html',
                               header=True,
                               click_a=True,
                               admin=True,
                               user=user)
    else:
        flash("Page does not exist", category='error')
        redirect('/')



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<user>/products/<product>', methods=['GET', 'POST'])
def get_product(user, product):
    cursor.execute("SELECT * FROM product WHERE Name='{}'".format(product))
    p = cursor.fetchone()
    print(p)
    return render_template('product.html', user=user,
                           header=True, query=p, prod=False)

@app.route('/<user>/purchase/<product>', methods=['GET', 'POST'])
def purchase(user ,product):
    if request.method == 'GET':
        cursor.execute("SELECT UserID FROM movie_user WHERE Username='{}'".format(user))
        userID = cursor.fetchone()[0]
        cursor.execute("SELECT ProductID FROM product WHERE name='{}'".format(product))
        productID = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO purchases(CustomerID,ProductID)VALUES(%s,%s)
        """, (userID, productID))

        db.commit()
        flash("{} purchased".format(product))
        return redirect('/{}/products/{}'.format(user, product))

@app.route('/<user>', methods=['GET', 'POST'])
def profile(user):
    cursor.execute("SELECT * FROM movie_user WHERE Username='{}'".format(user))
    l = ['First Name', 'Last Name', 'Email ']
    prof = cursor.fetchone()
    cursor.execute("""
        SELECT Name, Image, SellPrice  
           FROM product p, purchases pu 
        WHERE CustomerID={} AND p.ProductID=pu.ProductID
    """.format(prof[0]))
    prof = prof[1:-1]
    product = cursor.fetchall()
    tot = list(map(lambda x:x[-1], product))
    return render_template('profile.html',
                           header=True,
                           prof=list(zip(l,prof)),
                           product=product,
                           user=user,
                           tot=round(sum(tot),2))


if __name__ == '__main__':
    app.secret_key = "movie_max12xs32"
    app.run(debug=True)
    cursor.close()
    db.close()

