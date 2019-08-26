from insert_data import insert_comment
import os
import json
from datetime import datetime


def _worker(self, start, end, increment):
    fp = open("my_file")
    skip = False
    for i, line in enumerate(fp):
        if start <= i < end:
            skip = False
            print(line)
        elif skip:
            continue
        else:
            start += increment
            end += increment
            skip = True

    return "Processed thread batch [{},{}]".format(start, end)


with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    batch_size = 1000
    for i in range(0, 4000, batch_size):
        future = executor.submit(self._worker, i, i + batch_size, 3000)
        futures.append(future)

    for future in as_completed(futures):
        try:
            future_result = future.result()
            # do something with result
        except Exception as e:
            self._log.error("Failed to get future {}".format(str(e)))


if __name__ == '__main__':
    row_counter = 0

    # get properties from json
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        rc_dir = data['comments_directory']
        score_threshold = data['score_threshold']

    # get info from filename
    for filename in os.listdir(rc_dir):
        with open(os.path.join(rc_dir, filename), buffering=1000) as f:
            for row in f:
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

                comment_id = 't1_' + row['id']
                # comment_id = row['link_id']

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
