from insert_data import insert_comment
import os
import json
from datetime import datetime

if __name__ == '__main__':
    row_counter = 0

    # get properties from json
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        rc_dir = data['comments_directory']
        score_threshold = data['score_threshold']

    # get info from filename
    for filename in os.listdir(rc_dir):
        with open(os.path.join(rc_dir, filename), buffering=10000) as f:
            for row in f:
                try:
                    row_counter += 1
                    row = json.loads(row)
                    parent_id = row['parent_id']
                    body = row['body']
                    created_utc = row['created_utc']
                    subreddit = row['subreddit']
                    subreddit_id = row['subreddit_id']
                    controversiality = row['controversiality']
                    score = row['score']

                    body = body.replace(u"\u2019", "\'").replace(u"\u2018", "\'").replace(u"\u201c", "\"").replace(
                        u"\u201d", "\"")

                    # comment_id = 't1_' + row['id']
                    comment_id = row['link_id']

                    # try:
                    #     comment_id = row['name']
                    # except KeyError:
                    #     comment_id = 't1_' + row['id']
                    #     pass
                    # make sure the upvote/score are valid and have an acceptable body

                    if score >= score_threshold:
                        insert_comment(parent_id, comment_id, body, subreddit, subreddit_id, created_utc, controversiality, score)
                        # show the row counter
                        if row_counter % 100000 == 0:
                            print("Total rows read: {},  Time: {}".format(row_counter, str(datetime.now())))
                except Exception as e:
                    print("exception found", e)
