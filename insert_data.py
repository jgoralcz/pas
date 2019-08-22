import sys
import os
import pandas as pd
import subprocess
import argparse
import pdb
import pickle
from setup import setup_environment


# Make PostgreSQL Connection
engine = setup_environment.get_database()
try:
    con = engine.raw_connection()
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS comments(
                    parent_id TEXT,
                    comment_id TEXT,
                    parent TEXT,
                    comment varchar(256),
                    subreddit TEXT,
                    subreddit_id TEXT,
                    created_utc INT,
                    controversiality INT,
                    score INT
                )
                PRIMARY KEY(parent_id, subreddit_id);
                """
              )
except:
    print('Error setting up postgres.')
    pass


def insert_comment(parent_id, comment_id, parent_data, comment, sub, utc, controversiality, score):
    try:
        sql = """
            INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, created_utc, score)
            VALUES ("{}", "{}", "{}", "{}", "{}", {}, {})
            ON CONFLICT (parent_id, subreddit_id) DO NOTHING;
            """.format(parent_id, comment_id, parent_data, comment, sub, utc, controversiality, score)
        print('Inserting...')
    except Exception as e:
        print('Could not insert', parent_id)
        return None
