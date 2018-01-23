"""Populate postgresql database with parsed results."""
import os

from pdf_parser import page_parser

import psycopg2


def db_connector():
    """Create database connection."""
    dbname = os.environ.get('DB_NAME')
    host = os.environ.get('DB_HOST')
    try:
        conn = psycopg2.connect("dbname={} host={}".format(dbname, host))
        print("Connection to {} made on host {}.".format(dbname, host))
        return conn
    except:
        print("No connection made.")


def create_race_result_tables():
    """Create database tables for race results."""
    conn = db_connector()
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE TRACK (
                                            TrackID serial PRIMARY KEY,
                                            TrackCode VARCHAR(3) UNIQUE,
                                            TrackName VARCHAR(50) UNIQUE
                                           );
                    """)
        cur.execute("""CREATE TABLE HORSE (
                                           HorseID serial PRIMARY KEY,
                                           HorseName VARCHAR(50) UNIQUE
                                          );
                    """)
        cur.execute("""CREATE TABLE RACE (
                                          RaceID serial PRIMARY KEY,
                                          RaceDate date,
                                          RaceNum INT,
                                          Odds DECIMAL,
                                          SlotNum INT,
                                          HorseID INT REFERENCES HORSE(HorseID),
                                          TrackID INT REFERENCES TRACK(TrackID)
                                          );
                    """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tables made.")
    except:
        print("No tables made.")


def drop_race_db_tables():
    """Drop tables in race results database."""
    conn = db_connector()
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE track, horse, race CASCADE;")
        conn.commit()
        cur.close()
        conn.close()
        print("Tables dropped.")
    except:
        print("No tables dropped.")


def db_populate():
    """Populate database with parsed race results."""
    conn = db_connector()
    cur = conn.cursor()
    rr_gen = page_parser()
    for res in rr_gen:
        try:
            sql = """INSERT INTO horse (HorseName)
                     VALUES (%s)
                     WHERE NOT EXIXTS (SELECT HorseName
                                       FROM horse
                                       WHERE HorseName  = (%s));"""
            data = (res['Winner'], res['Winner'], )
            cur.execute(sql, data)
            conn.commit()
        except Exception as e:  # pragma: no cover
            with open('./../results/error_log.txt', 'a+') as f:
                f.write(str(e) + ' ' + str(res) + '\n')
    cur.close()
    conn.close()
