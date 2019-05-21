# DROP TABLES

all_tables = ['songplays', 'users', 'songs', 'artists', 'time']
DROP_TABLE_QUERY = 'DROP TABLE IF EXISTS {}'


def drop_table_queries():
    """ function to return all drop table queries """
    all_table_drop_queries = []

    for table_name in all_tables:
        """ Iterate over all table names to generate drop table query """
        all_table_drop_queries.append(DROP_TABLE_QUERY.format(table_name))

    return all_table_drop_queries


# CREATE TABLES

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays(songplay_id SERIAL PRIMARY KEY, "
                         "start_time timestamp NOT NULL, user_id varchar NOT NULL, level varchar NOT NULL, "
                         "song_id varchar, artist_id varchar, session_id int NOT NULL, location varchar NOT NULL, "
                         "user_agent varchar NOT NULL);")

user_table_create = ("CREATE TABLE IF NOT EXISTS users(user_id varchar PRIMARY KEY, first_name varchar NOT NULL, "
                     "last_name varchar NOT NULL, gender varchar NOT NULL, level varchar NOT NULL);")

song_table_create = ("CREATE TABLE IF NOT EXISTS songs(song_id varchar PRIMARY KEY, title varchar not null, "
                     "artist_id varchar not null , year integer not null, duration NUMERIC NOT NULL);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artists(artist_id varchar PRIMARY KEY, name varchar not null, "
                       "location varchar not null, latitude numeric, longitude numeric);")

time_table_create = ("CREATE TABLE IF NOT EXISTS time(start_time timestamp WITHOUT TIME ZONE PRIMARY KEY, "
                     "hour integer not null, day integer not null , week integer not null, month integer not null, "
                     "year integer not null, weekday varchar not null);")

# INSERT RECORDS

songplay_table_insert = ("INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, "
                         "location, user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")

user_table_insert = "INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES(%s,%s,%s,%s,%s) " \
                    "ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level"

song_table_insert = "INSERT INTO songs(song_id, title, artist_id, year, duration) VALUES(%s, %s, %s, %s, %s) " \
                    "ON CONFLICT (song_id) DO NOTHING"

artist_table_insert = "INSERT INTO artists(artist_id, name, location, latitude, longitude) VALUES (%s,%s,%s,%s,%s) " \
                      "ON CONFLICT (artist_id) DO NOTHING"

time_table_insert = "INSERT INTO time(start_time, hour, day, week, month, year, weekday) VALUES(%s,%s,%s,%s,%s,%s,%s)" \
                    " ON CONFLICT (start_time) DO NOTHING "

# FIND SONGS

song_select = ("SELECT songs.song_id, artists.artist_id FROM songs LEFT JOIN artists ON "
               "songs.artist_id = artists.artist_id where "
               "songs.title = (%s) and artists.name = (%s) and songs.duration = (%s) ")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create,
                        time_table_create]
drop_table_queries = drop_table_queries()
