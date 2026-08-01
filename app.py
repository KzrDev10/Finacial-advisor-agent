from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.models import db, User
import uuid
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "Users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-in-production'  # needed for session

db.init_app(app)


# ── Home ──────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template("homepage.html")


# ── Signup ────────────────────────────────────────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name', '').strip()
        email      = request.form.get('email', '').strip().lower()
        password   = request.form.get('password', '')
        confirm    = request.form.get('confirm_password', '')

        # ── Validation ──
        errors = {}

        if not first_name or not last_name:
            errors['name'] = 'First and last name are required.'

        if not email or '@' not in email:
            errors['email'] = 'Please enter a valid email address.'
        elif User.query.filter_by(email=email).first():
            errors['email'] = 'An account with this email already exists.'

        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        elif password != confirm:
            errors['confirm'] = 'Passwords do not match.'

        if errors:
            return render_template('signup.html', errors=errors,
                                   first_name=first_name, last_name=last_name,
                                   email=email)

        # ── Create user ──
        user_id = str(uuid.uuid4())[:20]
        new_user = User(id=user_id, first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = user_id
        session['user_email'] = email
        flash('Account created! Welcome to FinanceAI.', 'success')
        return redirect(url_for('home'))

    return render_template('signup.html', errors={})


# ── Login ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        errors = {}

        if not email or '@' not in email:
            errors['email'] = 'Please enter a valid email address.'

        if not password:
            errors['password'] = 'Password is required.'

        if not errors:
            user = User.query.filter_by(email=email).first()
            if user is None or not user.check_password(password):
                errors['auth'] = 'Incorrect email or password.'

        if errors:
            return render_template('login.html', errors=errors, email=email)

        # ── Success ──
        session['user_id']    = user.id
        session['user_email'] = user.email
        flash('Welcome back!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', errors={})


# ── Logout ────────────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ── Run ───────────────────────────────────────────────────────────────────────
if "__main__" == __name__:
    with app.app_context():
        db.create_all()
    app.run(debug=True)