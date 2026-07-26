##############################################################
# Title: movies_update_and_delete.py
# Author: Rakesh Shrestha
# Date: 07/25/2026
# Description: Module 7.2 Assignment - Movies: Update/Insertion/Deletion
#              Connects to the movies database, inserts a new film,
#              updates a film's genre, and deletes a film, displaying
#              the film table after each change.
##############################################################

import mysql.connector
from mysql.connector import errorcode

import dotenv
from dotenv import dotenv_values

# using our .env file
secrets = dotenv_values(".env")

# database config object
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # not in .env file
}


def show_films(cursor, title):
    """
    Method to execute an inner join on all tables,
    iterate over the dataset and output the results to the terminal window.

    :param cursor: an active MySQL cursor object
    :param title: a string label describing which output this is
    """
    # inner join query
    cursor.execute(
        "select film_name as Name, film_director as Director, "
        "genre_name as Genre, studio_name as 'Studio Name' "
        "from film INNER JOIN genre ON film.genre_id=genre.genre_id "
        "INNER JOIN studio ON film.studio_id=studio.studio_id "
        "ORDER BY film.film_id"
    )

    # get the results from the cursor object
    films = cursor.fetchall()

    print("\n -- {} --".format(title))

    # iterate over the film data set and display the results
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(
            film[0], film[1], film[2], film[3]))


try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # 1. show the film table before any changes
    show_films(cursor, "DISPLAYING FILMS")

    # 2. insert a new film (using a studio already in the studio table)
    insert_film = (
        "INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, genre_id, studio_id) "
        "VALUES (%s, %s, %s, %s, "
        "(SELECT genre_id FROM genre WHERE genre_name = %s), "
        "(SELECT studio_id FROM studio WHERE studio_name = %s))"
    )
    new_film = ("Inception", "2010", 148, "Christopher Nolan", "SciFi", "Universal Pictures")
    cursor.execute(insert_film, new_film)
    conn.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # 3. update the film Alien to being a Horror film
    update_film = (
        "UPDATE film SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = %s) "
        "WHERE film_name = %s"
    )
    cursor.execute(update_film, ("Horror", "Alien"))
    conn.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    # 4. delete the movie Gladiator
    delete_film = "DELETE FROM film WHERE film_name = %s"
    cursor.execute(delete_film, ("Gladiator",))
    conn.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
