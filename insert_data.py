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
                    score INT,
                    id SERIAL,
                )
                PRIMARY KEY(parent_id, subreddit_id);
                """
              )
except Exception as ex:
    print('Error setting up postgres.')
    pass


class Transaction:
    """
    creates a Transaction builder
    """
    sql_transaction = []

    def append(self, sql):
        self.sql_transaction.append(sql)

        if len(self.sql_transaction) > 500:
            c.execute('BEGIN TRANSACTION')
            for s in trans.sql_transaction:
                try:
                    c.execute(s)
                except Exception as e:
                    print('error', str(e))
                    pass
            con.commit()
            self.clear()

        self.sql_transaction.append(sql)

    def clear(self):
        self.sql_transaction = []


trans = Transaction()


def insert_comment(parent_id, comment_id, parent_data, comment, sub, utc, controversiality, score):
    try:
        sql = """
            INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, created_utc, score)
            VALUES ("{}", "{}", "{}", "{}", "{}", {}, {})
            ON CONFLICT (parent_id, subreddit_id) DO NOTHING;
            """.format(parent_id, comment_id, parent_data, comment, sub, utc, controversiality, score)
        print('Inserting...')
        trans.append(sql)
    except Exception as e:
        print('Could not insert', parent_id)
        return None
