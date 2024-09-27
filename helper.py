import sqlite3
import pandas as pd
import ast
import pycountry


class Db_Manager:
    
    def __init__(self):
        self.total_movies = 0 
        self.conn = None
        self.count_movies()
        self.total_pages = self.total_movies//30 
        self.unique_genre_ = self.genreList_extractor()
        self.unique_country_ = self.countryList_extractor()
        self.unique_production_ = self.productionList_extractor()

    def countryList_extractor(self):
        if self.conn is None:
            self.get_db_connection()

        df = pd.read_sql("""
    SELECT `Country`, COUNT(*) as country_count 
    FROM `movies`
    GROUP BY `Country`
    ORDER BY country_count DESC
    LIMIT 40
    """, self.conn)
        
        country_codes = df['Country'].tolist()

        country_names = []
        for code in country_codes:
            try:

                country_name = pycountry.countries.get(alpha_2=code).name
                country_names.append(country_name)
            except AttributeError:

                country_names.append(f"Unknown ({code})")

        return country_names

    def productionList_extractor(self):
        if self.conn is None:
            self.get_db_connection()
            
        df = pd.read_sql(f'''SELECT `Production`, COUNT(*) as production_count 
    FROM `movies`
    GROUP BY `Production`
    ORDER BY production_count DESC
    LIMIT 30''', self.conn)
        
        productions = df['Production'].apply(ast.literal_eval)
        all_production = [production for sublist in productions for production in sublist]
        unique_production = pd.Series(all_production).unique()
        
        print(unique_production)
        return unique_production

    def genreList_extractor(self):
        if self.conn is None:
            self.get_db_connection()
            
        df = pd.read_sql(f"SELECT DISTINCT `Genre` FROM `movies`", self.conn)
        
        genres = df['Genre'].apply(ast.literal_eval)
        all_genres = [genre for sublist in genres for genre in sublist]
        unique_genres = pd.Series(all_genres).unique()
        
        return unique_genres

        

    def get_db_connection(self):
        # Set check_same_thread=False to allow usage across threads
        self.conn = sqlite3.connect('movies.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        
    def fetch_movie(self, n=30):
        if self.conn is None:
            self.get_db_connection()

        df = pd.read_sql(f"SELECT * FROM 'movies' WHERE Time = 2024 LIMIT {n}", self.conn)
        
        
        data = df.to_dict(orient='records')
        return data

        
    def fetch_by_page_no(self, pg_no=1, genre='all'):
        if self.conn is None:
            self.get_db_connection()

        offset = (pg_no - 1) * 30  # Calculate the offset based on the page number

        if genre == 'all':    
            query = f"SELECT * FROM 'movies' LIMIT 30 OFFSET {offset}"
        else:
            query = f"SELECT * FROM 'movies' WHERE Genre LIKE ? LIMIT 30 OFFSET {offset}"

        # Execute the query with the genre parameter if provided
        if genre == 'all':
            df = pd.read_sql(query, self.conn)
        else:
            df = pd.read_sql(query, self.conn, params=(f"%{genre}%",))

        data = df.to_dict(orient='records')
        return data


    def fetch_by_id(self, id):
        if self.conn is None:
            self.get_db_connection()

        query = f"SELECT * FROM `movies` WHERE `Id` = {id}"
        df = pd.read_sql(query, self.conn)
        df_dict = df.iloc[0].to_dict()
        
        movie_detail = {
        
        'id' : df_dict['Id'],
        'title' : df_dict['Title'],
        'time' : df_dict['Time'],
        'type' : df_dict['Type'] ,
        'duration' : df_dict['Duration'] ,
        'img' : df_dict['Img'],
        'coverBg' : df_dict['CoverBg'],
        'movieDesc' : df_dict['movieDesc'],
        'released' : df_dict['Released'],
        'genre' : ast.literal_eval(df_dict['Genre']),
        'casts' : ast.literal_eval(df_dict['Casts']),
        'country' : pycountry.countries.get(alpha_2 = df_dict['Country'].upper()).name,
        'production' : ast.literal_eval(df_dict['Production']),
        'imdb' : df_dict['IMDB_rating']
        
        }
    
        
        if not df.empty:
            return movie_detail
        return {}


    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
                
    def count_movies(self):
        if self.conn == None:
            self.get_db_connection()
            
        query = f"SELECT COUNT(*) AS total_movies FROM 'movies'"
        result = pd.read_sql(query,self.conn)
        self.total_movies = result['total_movies'][0]     
        
