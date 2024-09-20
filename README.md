# MovieJoy

MovieJoy is a web application that allows users to browse and discover movies. Built using Flask, this application fetches movie data from an SQLite database and displays it in a user-friendly interface.

## Features

- Displays a list of movies with details such as title, release year, type, duration, IMDB rating, genre, cast, country, and production.
- Responsive design using Bootstrap for a seamless user experience on various devices.
- Search functionality to find specific movies (placeholder functionality).

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap
- **Python Libraries**: pandas

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- pandas

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bannu82/moviejoy.git
   cd moviejoy

2. Install Virtual environment:
   ```bash
   pip install virtualenv
   
3. Create a virtual environment (optional but recommended):
   ```bash
   viretual venv
   venv\Scripts\activate

4. Install the required packages:
   ```bash
   pip install -r requirements.txt

5. Make sure you have the SQLite database (data.db) with the movies table.

### Running the Application
1. Start the Flask server:
   ```bash
   python app.py
2. Open your web browser and go to url
   ```url
   http://127.0.0.1:5000

### File Structure
   ```tree
moviejoy/
├── app.py
├── helper.py
├── templates/
│   └── home.html
└── static/
    └── css/
        └── style.css
