from db import get_database
import logging
log = logging.getLogger(__name__)


class Transaction:
    """
    creates a Transaction builder
    """
    sql_transaction = []

    def __init__(self):
        # Make PostgreSQL Connection
        engine = get_database()
        try:
            self.con = engine.raw_connection()
            self.c = self.con.cursor()
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS comments(
                    parent_id TEXT,
                    comment_id TEXT,
                    comment varchar(256),
                    subreddit TEXT,
                    subreddit_id TEXT,
                    created_utc INT,
                    controversiality INT,
                    score INT,
                    id SERIAL,
                    
                    PRIMARY KEY(parent_id, comment_id, subreddit_id, score)
                );
                """)
            self.con.commit()
        except Exception as ex:
            raise Exception('Error setting up postgres.', ex)

    def append(self, sql):
        self.sql_transaction.append(sql)

        if len(self.sql_transaction) > 50:
            self.c.execute('BEGIN TRANSACTION')
            try:
                print('Inserting...')
                for [s, t] in trans.sql_transaction:
                    self.c.execute(s, t)
                self.con.commit()
            except Exception as e:
                print('error', str(e))
                self.con.rollback()
                pass
            self.clear()

        self.sql_transaction.append(sql)

    def clear(self):
        self.sql_transaction = []


trans = Transaction()


def insert_comment(parent_id, comment_id, comment, sub, sub_id, utc, controversiality, score):
    try:
        if len(comment) <= 256:
            sql = ["""
                INSERT INTO comments (parent_id, comment_id, comment, subreddit, subreddit_id, created_utc, controversiality, score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (parent_id, comment_id, subreddit_id, score) DO NOTHING;
                """, (parent_id, comment_id, comment, sub, sub_id, utc, controversiality, score)]
            trans.append(sql)
    except Exception as e:
        print('Exception:', e)
        print('Could not insert', parent_id)
        return None
