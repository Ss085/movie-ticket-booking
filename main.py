from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus  # ✅ For special characters in password

app = Flask(__name__)

# 🔑 Local MySQL credentials
DB_USER = "root"
DB_PASS = quote_plus("novak@24")  # Encode special characters like @
DB_HOST = "localhost"
DB_NAME = "movie_booking"

# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS ---
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    movie = db.relationship('Movie', backref=db.backref('bookings', lazy=True))

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    all_movies = Movie.query.all()
    return render_template('movies.html', movies=all_movies)

@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        name = request.form['name']
        seats = int(request.form['seats'])
        booking = Booking(name=name, seats=seats, movie=movie)
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('bookings'))
    return render_template('book.html', movie=movie)

@app.route('/bookings')
def bookings():
    all_bookings = Booking.query.all()
    return render_template('bookings.html', bookings=all_bookings)

# --- DB INIT ---
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
