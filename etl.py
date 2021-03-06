import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from create_tables import CONNECT_TO_DB, SPARKIFY_DB_NAME, USER_NAME, PASSWORD, HOST_NAME


def process_song_file(cur, filepath):
    """ This function loads data from song_data directory into songs and artists table """
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = df.filter(items=['song_id', 'title', 'artist_id', 'year', 'duration']).values.tolist()
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df.filter(
        items=['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']).values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """ This function loads data from log_data directory into time, users and songplay table """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    df['timestamp'] = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = list((df.timestamp.tolist(), t.dt.hour.tolist(), t.dt.day.tolist(), t.dt.week.tolist(),
                      t.dt.month.tolist(), t.dt.year.tolist(), t.dt.weekday_name.tolist()))

    column_labels = ['start_ts', 'hour', 'day', 'week', 'month', 'year', 'weekday']

    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        df['artistid'] = artistid
        df['songid'] = songid
        df['ts'] = pd.to_datetime(row.ts, unit='ms')

        songplay_data = (df[['ts', 'userId', 'level', 'songid', 'artistid', 'sessionId', 'location', 'userAgent']]
                         .values[0].tolist())
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ function to collect all the files from the directory in the input """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect(CONNECT_TO_DB.format(HOST_NAME, SPARKIFY_DB_NAME, USER_NAME, PASSWORD))
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
