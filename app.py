from flask import Flask, request, render_template
from helper import Db_Manager as db_mg

app = Flask(__name__)
db = db_mg()  

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    pg_no=1
    # Create a new instance for each request
    ttl_pg = db.total_pages
    movies = db.fetch_by_page_no(pg_no)
    # db.close_connection()  # Close the connection after use
    
    return render_template('home.html', movies=movies ,pg_no=pg_no , total_pages =ttl_pg )

@app.route('/home/page=<int:pg_no>')
def pages(pg_no):
    movies = db.fetch_by_page_no(pg_no)
    ttl_mv = db.total_movies
    ttl_pg = db.total_pages
    
    return render_template('home.html', pg_no=pg_no , movies=movies , total_movies=ttl_mv , total_pages =ttl_pg )

@app.route('/home/movie/<string:title>/<int:id>')
def movie(title,id):
    movie = db.fetch_by_id(id)
    
    return render_template('movie.html' , id=id, title=title ,movie=movie)
    

if __name__ == "__main__":
    app.run(debug=True)
