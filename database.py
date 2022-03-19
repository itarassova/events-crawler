import psycopg2
from event import Event

class EventPSQL:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)
        self.cursor = self.conn.cursor()
        self.__create_tables()

    

    def __create_tables(self):
        """ create tables in the PostgreSQL database"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS event_details  (
                event_id SERIAL PRIMARY KEY,
                event_title TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                event_location TEXT NOT NULL,
                event_image_link TEXT NOT NULL,
                event_identifier TEXT 
            )
            """,
            """ CREATE TABLE IF NOT EXISTS event_artists (
                event_id INTEGER,
                event_artist TEXT,
                FOREIGN KEY (event_id)
                REFERENCES event_details (event_id)
                ON UPDATE CASCADE ON DELETE CASCADE
                )
            """,
            """
            CREATE TABLE IF NOT EXISTS event_works (
                event_id INTEGER,
                event_work TEXT,
                FOREIGN KEY (event_id)
                REFERENCES event_details (event_id)
                ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)
        for command in commands:
            self.cursor.execute(command)
        self.conn.commit()

    def insert_event_details(self, event: Event):
        sql_insert_details = ''' INSERT INTO event_details (event_title, event_date, event_time, event_location, event_image_link, event_identifier) VALUES (%s,%s, %s, %s, %s, %s) RETURNING event_id; '''
        self.cursor.execute(sql_insert_details, (event.title, event.date, event.time, event.location, event.image_link, event.identifier))
        event_id = self.cursor.fetchone()[0]
        sql_insert_artist = ''' INSERT INTO event_artists (event_id, event_artist) VALUES (%s,%s); '''
        for artist in event.artists:
            self.cursor.execute(sql_insert_artist, (event_id, artist))
        sql_insert_work = ''' INSERT INTO event_works (event_id, event_work) VALUES (%s,%s); '''
        for work in event.works:
            self.cursor.execute(sql_insert_work, (event_id, work))
        self.conn.commit()
        

        
