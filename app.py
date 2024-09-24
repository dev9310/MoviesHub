from flask import Flask, request, render_template
import helper

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    movies = helper.fetch_movie()
    total_movies= helper.count_movies()
    
    return render_template('home.html', movies=movies ,total_movies=total_movies)
    

if __name__ == "__main__":
    app.run(debug=True)
