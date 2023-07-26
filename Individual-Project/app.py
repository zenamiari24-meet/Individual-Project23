from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBkCc1WY7Yu2BETjmYA6m3jmHYU4Ll5qMI",
  "authDomain": "fir-17f02.firebaseapp.com",
  "projectId": "fir-17f02",
  "storageBucket": "fir-17f02.appspot.com",
  "messagingSenderId": "787139879406",
  "appId": "1:787139879406:web:e62a546ade52375942eeff",
  "measurementId": "G-K9LW85TTZH", "databaseURL":"https://fir-17f02-default-rtdb.firebaseio.com/"}


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()


#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"

    return render_template("login.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        username = request.form['username']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"fullname":fullname,"username": username,"email":email,"password":password}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"

    return render_template("signup.html")   





@app.route('/home')
def home():
    dishes=["fish","meat","vegi/vege"]
    return render_template('home.html', dishes = dishes)



@app.route('/food')
def food():
    return render_template('food.html')




@app.route('/fish')
def fish():
    return render_template('fish.html')



@app.route('/vege')
def vege():
    return render_template('vege.html')


@app.route('/meat')
def meat():
    return render_template('meat.html')



@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == "POST":
        comments = request.form["comments"]
        try:
            UID = login_session['user']['localId']
            comment = {"comments": comments, "UID":UID}
            db.child("comments").push(comment)
            return redirect(url_for('all_comments'))
        except:
            error = "Authentication failed"
            return redirect(url_for('comments'))
    return render_template("comments.html")


@app.route('/all_comments',methods=["GET","POST"])
def all_comments():
    comments=db.child("comments").get().val()
    return render_template("all_comments.html", comments=comments)

def get_food_dishes():
    dishes = [
        {
            "name": "Sushi",
            "image_url": "https://australianavocados.com.au/wp-content/uploads/2021/05/AusAvo_Sushi.jpg"
        },
        {
            "name": "Smashburger",
            "image_url": "https://assets.epicurious.com/photos/5c745a108918ee7ab68daf79/1:1/w_2560%2Cc_limit/Smashburger-recipe-120219.jpg"
        },
        {
            "name": "Vegan Dish",
            "image_url": "https://images.everydayhealth.com/images/what-is-a-vegan-diet-benefits-food-list-beginners-guide-alt-1440x810.jpg?sfvrsn=1d260c85_1"
        },
        {
            "name": "Healthy Bowl",
            "image_url": "https://i0.wp.com/post.healthline.com/wp-content/uploads/2021/09/healthy-eating-food-sweet-potato-kale-bowl-grain-vegan-1296x728-header.jpg?w=1155&h=1528"
        }
    ]
    return jsonify(dishes)

 

#Code goes above here

if __name__ == '__main__': 
    app.run(debug=True)