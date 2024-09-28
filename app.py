from flask import Flask, request, render_template
from helper import Db_Manager as db_mg

app = Flask(__name__)
db = db_mg()

# Commonly used lists
genre_list = db.unique_genre_
country_list = db.unique_country_
production_list = db.unique_production_

def get_movies(pg_no, genre='all'):
    movies, total_pages = db.fetch_by_page_no(pg_no, genre)
    return total_pages, movies

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
@app.route('/home/page=<int:pg_no>')
def home(pg_no=1):
    total_pages, movies = get_movies(pg_no)
    if pg_no > total_pages or pg_no <= 0:
        return render_template('error.html', pg_no=pg_no, total_pages=total_pages,
                               genre_list=genre_list, country_list=country_list, production=production_list, genre=genre)
    return render_template('home.html', movies=movies, pg_no=pg_no, total_pages=total_pages,
                           genre_list=genre_list, country_list=country_list, production=production_list, genre='all')

@app.route('/home/page=<int:pg_no>&genre=<string:genre>')
def home_filter(pg_no, genre):
    total_pages, movies = get_movies(pg_no, genre)
    if pg_no > total_pages or pg_no <= 0:
        return render_template('error.html', pg_no=pg_no, total_pages=total_pages ,
                               genre_list=genre_list, country_list=country_list, production=production_list, genre=genre)
    return render_template('home.html', movies=movies, pg_no=pg_no, total_pages=total_pages,
                           genre_list=genre_list, country_list=country_list, production=production_list, genre=genre)

@app.route('/home/movie/<string:title>/<int:id>')
def movie(title, id):
    movie_detail = db.fetch_by_id(id)
    return render_template('movie.html', movie=movie_detail, genre_list=genre_list, 
                           country_list=country_list, production=production_list)

if __name__ == "__main__":
    app.run(debug=True)
