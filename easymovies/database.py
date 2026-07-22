import os
import sqlite3

DB_NAME = os.getenv("DB_NAME", "easymovies.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Movies table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            theatre TEXT NOT NULL,
            available_seats INTEGER NOT NULL
        )
    """)

    # Bookings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            customer TEXT NOT NULL,
            seats INTEGER NOT NULL,
            FOREIGN KEY(movie_id) REFERENCES movies(id)
        )
    """)

    # Insert demo data only once
    count = cur.execute("SELECT COUNT(*) FROM movies").fetchone()[0]

    if count == 0:
        movies = [
            ("Avatar 3", "PVR Noida", 120),
            ("Superman", "INOX Delhi", 90),
            ("Jurassic World", "Cinepolis Gurgaon", 150),
            ("Mission Impossible", "PVR Saket", 100),
            ("F1", "PVR Mall of India", 80),
        ]

        cur.executemany(
            "INSERT INTO movies(name,theatre,available_seats) VALUES(?,?,?)",
            movies
        )

    conn.commit()
    conn.close()


def get_movies():
    conn = get_connection()

    movies = conn.execute(
        "SELECT * FROM movies ORDER BY id"
    ).fetchall()

    conn.close()

    return movies


def book_ticket(movie_id, customer, seats):

    conn = get_connection()
    cur = conn.cursor()

    movie = cur.execute(
        "SELECT available_seats FROM movies WHERE id=?",
        (movie_id,)
    ).fetchone()

    if movie is None:
        conn.close()
        return False

    if movie["available_seats"] < seats:
        conn.close()
        return False

    cur.execute(
        """
        INSERT INTO bookings(movie_id,customer,seats)
        VALUES(?,?,?)
        """,
        (movie_id, customer, seats)
    )

    cur.execute(
        """
        UPDATE movies
        SET available_seats = available_seats - ?
        WHERE id=?
        """,
        (seats, movie_id)
    )

    conn.commit()
    conn.close()

    return True


def get_bookings():

    conn = get_connection()

    bookings = conn.execute("""
        SELECT
            bookings.id,
            movies.name,
            movies.theatre,
            bookings.customer,
            bookings.seats
        FROM bookings
        JOIN movies
        ON movies.id = bookings.movie_id
        ORDER BY bookings.id DESC
    """).fetchall()

    conn.close()

    return bookings


def cancel_booking(booking_id):

    conn = get_connection()
    cur = conn.cursor()

    booking = cur.execute("""
        SELECT movie_id,seats
        FROM bookings
        WHERE id=?
    """, (booking_id,)).fetchone()

    if booking:

        cur.execute("""
            UPDATE movies
            SET available_seats = available_seats + ?
            WHERE id=?
        """, (booking["seats"], booking["movie_id"]))

        cur.execute(
            "DELETE FROM bookings WHERE id=?",
            (booking_id,)
        )

    conn.commit()
    conn.close()