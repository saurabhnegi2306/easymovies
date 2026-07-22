import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from database import (
    init_db,
    get_movies,
    book_ticket,
    get_bookings,
    cancel_booking
)

app = Flask(__name__)

# Create database on first run
init_db()


@app.route("/")
def home():

    movies = get_movies()

    build_info = {
        "build_number": os.getenv("BUILD_NUMBER", "Local"),
        "branch": os.getenv("GIT_BRANCH", "main"),
        "git_commit": os.getenv("GIT_COMMIT", "N/A")[:7],
        "build_url": os.getenv("BUILD_URL", ""),
        "builder": os.getenv("BUILD_USER", "Jenkins"),
        "build_time": os.getenv(
            "BUILD_TIME",
            datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        )
    }

    return render_template(
        "index.html",
        movies=movies,
        build_info=build_info
    )


@app.route("/book/<int:movie_id>", methods=["GET", "POST"])
def book(movie_id):

    if request.method == "POST":

        customer = request.form["customer"]
        seats = int(request.form["seats"])

        book_ticket(movie_id, customer, seats)

        return redirect(url_for("bookings"))

    movies = get_movies()

    movie = None

    for m in movies:
        if m["id"] == movie_id:
            movie = m
            break

    return render_template("book.html", movie=movie)


@app.route("/bookings")
def bookings():

    all_bookings = get_bookings()

    return render_template(
        "bookings.html",
        bookings=all_bookings
    )


@app.route("/cancel/<int:booking_id>")
def cancel(booking_id):

    cancel_booking(booking_id)

    return redirect(url_for("bookings"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)