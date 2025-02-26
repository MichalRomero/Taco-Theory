from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Food
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:  # Ensure both fields are filled
            flash('Please fill out both fields.', category='error')
            return render_template("login.html", user=current_user)

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)
    

@auth.route('/logout')
#@login_required means that it is not able to access this route if a user is not already logged in.
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        #Checks if user input is valid, if yes then adds user to database
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 5:
            flash('Password must have at least 5 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), role="customer")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/menu', methods=['GET', 'POST'])
def menu():
    foods = Food.query.all()
    return render_template("menu.html", user=current_user, foods=foods)

@auth.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    foods = Food.query.all()

    if 'basket' not in session:
        session['basket'] = {}  # Initialize basket in session if not present

    if request.method == 'POST':
        food_id = request.form.get('food_id')
        quantity = int(request.form.get('quantity', 1))  # Default to 1

        if not food_id:
            flash("Invalid food item.", category="error")
            return redirect(url_for('auth.order'))

        food = Food.query.get(food_id)
        if not food:
            flash("Food item not found.", category="error")
            return redirect(url_for('auth.order'))

        basket = session['basket']

        # Add item to basket or update quantity
        if food_id in basket:
            basket[food_id] += quantity
        else:
            basket[food_id] = quantity

        session['basket'] = basket  # Save basket in session
        flash(f"{food.name} added to basket!", category="success")

    return render_template("order.html", user=current_user, foods=foods)

@auth.route('/basket')
@login_required
def view_basket():
    if 'basket' not in session or not session['basket']:
        flash("Your basket is empty.", category="info")
        return render_template("basket.html", user=current_user, basket_items=[], total_price=0)

    basket = session['basket']
    food_items = []
    total_price = 0

    for food_id, quantity in basket.items():
        food = Food.query.get(food_id)
        if food:
            food_items.append({'food': food, 'quantity': quantity})
            total_price += food.price * quantity

    return render_template("basket.html", user=current_user, basket_items=food_items, total_price=total_price)

@auth.route('/checkout', methods=['GET'])
@login_required
def checkout():
    if 'basket' not in session or not session['basket']:
        flash("Your basket is empty. Add items before checking out.", category="info")
        return redirect(url_for('auth.order'))

    basket = session['basket']
    food_items = []
    total_price = 0

    for food_id, quantity in basket.items():
        food = Food.query.get(food_id)
        if food:
            food_items.append({'food': food, 'quantity': quantity})
            total_price += food.price * quantity

    return render_template("checkout.html", user=current_user, basket_items=food_items, total_price=total_price)

@auth.route('/confirm-checkout', methods=['POST'])
@login_required
def confirm_checkout():
    session.pop('basket', None)  # Clear basket from session after checkout
    flash("Thank you! Your order has been placed successfully.", category="success")
    return redirect(url_for('auth.order'))  # Redirect back to menu



@auth.route('/staff', methods=['GET', 'POST'])
def staff():
    return render_template("staff.html", user=current_user)