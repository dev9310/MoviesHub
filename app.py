from flask import Flask, request, render_template
from helper import Db_Manager as db_mg

app = Flask(__name__)
db = db_mg()

# Commonly used lists
genre_list = db.unique_genre_
country_list = db.unique_country_
country_code = db.countryCodes_
production_list = db.unique_production_

country_zip  = list(zip( country_list , country_code) )

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
                               genre_list=genre_list, production=production_list, genre='all' ,country_zip=country_zip)
    return render_template('home.html', movies=movies, pg_no=pg_no, total_pages=total_pages,
                           genre_list=genre_list, production=production_list, genre='all',country_zip=country_zip)

@app.route('/home/page=<int:pg_no>&genre=<string:genre>')
def home_genre(pg_no, genre):
    total_pages, movies = get_movies(pg_no, genre)
    
    if pg_no > total_pages or pg_no <= 0:
        return render_template('error.html', pg_no=pg_no, total_pages=total_pages ,
                               genre_list=genre_list, production=production_list, genre=genre,country_zip=country_zip)
    return render_template('home.html', movies=movies, pg_no=pg_no, total_pages=total_pages,
                           genre_list=genre_list, production=production_list, genre=genre,country_zip=country_zip)

@app.route('/home/page=<int:pg_no>&country=<string:country>')
def home_country(pg_no ,country):
    
    total_pages,movies  = db.fetch_by_country_code(pg_no , country)
    
    if pg_no > total_pages or pg_no <= 0:
        return render_template('error.html', pg_no=pg_no, total_pages=total_pages ,
                               genre_list=genre_list, production=production_list,country_zip=country_zip)
    return render_template('home.html', movies=movies, pg_no=pg_no, total_pages=total_pages,
                           genre_list=genre_list, production=production_list,country_zip=country_zip)

    
@app.route('/home/movie/<string:title>/<int:id>')
def movie(title, id):
    movie_detail = db.fetch_by_id(id)
    return render_template('movie.html', movie=movie_detail, genre_list=genre_list, 
                            production=production_list,country_zip=country_zip)

if __name__ == "__main__":
    app.run(debug=True)
