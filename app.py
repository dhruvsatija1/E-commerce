from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'

db = SQLAlchemy(app)

# User Model with Primary Key
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Product Model (you need this as well for the products page)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Cart Model (you need this too for the cart functionality)
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect('/products')
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

# Products Page
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    user_id = 1  # Hardcoded for simplicity (assume user is logged in)
    cart_item = Cart(user_id=user_id, product_id=product_id)
    db.session.add(cart_item)
    db.session.commit()
    
    return redirect('/products')

# Cart Page
@app.route('/cart')
def cart():
    user_id = 1  # Hardcoded for simplicity
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    products = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        products.append(product)
    return render_template('cart.html', products=products)

# Initialize Database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)