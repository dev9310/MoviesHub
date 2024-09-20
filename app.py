from flask import Flask, request, render_template
import helper

app = Flask(__name__)

@app.route('/')
def home():
    movies = helper.fetch_movie()

    return render_template('home.html', movies=movies)





if __name__ == "__main__":
    app.run(debug=True)
