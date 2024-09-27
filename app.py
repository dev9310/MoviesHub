from flask import Flask, request, render_template
from helper import Db_Manager as db_mg

app = Flask(__name__)
db = db_mg()  
genre_list = None


def get_movies(pg_no):
    ttl_pg = db.total_pages
    movies = db.fetch_by_page_no(pg_no)
    genre_list = db.unique_genre_
    return ttl_pg , movies ,genre_list


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    pg_no=1
    
    
    ttl_pg ,movies ,genre_list = get_movies(pg_no)
    country_list = db.unique_country_
    production = db.unique_production_
    return render_template('home.html', movies=movies ,pg_no=pg_no , total_pages =ttl_pg  ,genre_list=genre_list,country_list =country_list ,production=production ,genre = 'all')

@app.route('/home/page=<int:pg_no>')
def pages(pg_no):
    
    ttl_pg ,movies ,genre_list = get_movies(pg_no)
    country_list = db.unique_country_
    production = db.unique_production_
    if pg_no > ttl_pg:
        return render_template('error.html' , pg_no=pg_no, total_pages =ttl_pg )
    elif pg_no <=0:
        return render_template('error.html' , pg_no=pg_no, total_pages =ttl_pg )
    
    else:
        return render_template('home.html', pg_no=pg_no , movies=movies  , total_pages =ttl_pg  ,genre_list=genre_list ,country_list =country_list,production=production)

@app.route('/home/movie/<string:title>/<int:id>')
def movie(title,id):
    movie = db.fetch_by_id(id)    
    genre_list =db.unique_genre_
    country_list = db.unique_country_
    production = db.unique_production_

    return render_template('movie.html' , id=id, title=title ,movie=movie  ,genre_list=genre_list  ,country_list =country_list ,production=production)
    


@app.route('/home/page=<int:pg_no>&genre=<string:genre>')
def homeFilter(pg_no ,genre):
    
    ttl_pg = db.total_pages
    movies = db.fetch_by_page_no(pg_no , genre)
    genre_list = db.unique_genre_    
    country_list = db.unique_country_

    if pg_no > ttl_pg:
        return render_template('error.html' , pg_no=pg_no, total_pages =ttl_pg )
    elif pg_no <=0:
        return render_template('error.html' , pg_no=pg_no, total_pages =ttl_pg )
    
    else:
        return render_template('home.html', pg_no=pg_no , movies=movies  , total_pages =ttl_pg  ,genre_list=genre_list ,country_list =country_list ,genre = genre)


if __name__ == "__main__":
    app.run(debug=True)
