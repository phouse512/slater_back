import psycopg2
import sys
import time
import yaml

from admin.shared.poll import Poll
from typing import List


def load_polls(filename: str) -> List[Poll]:

    with open(filename, 'r') as stream:
        try:
            sys.stdout.write("Loading polls from %s\n" % filename)
            raw_yaml = yaml.load(stream)
        except yaml.YAMLError as e:
            sys.stderr.write(e)
            sys.stderr.write("\nUnable to load yaml file to polls\n\n")
            sys.exit()

    polls_list = []
    for poll_object in raw_yaml:
        polls_list.append(Poll.load_from_yaml(poll_object))

    return polls_list


def validate_polls(polls: List[Poll], cursor, connection) -> List[Poll]:
    """
    validates that polls don't already exist

    :param polls: a list of polls to validate
    :return: a list of valid polls, non-valid polls will be written to stdout
    """

    current_time = int(round(time.time()))

    valid_polls = []
    for poll in polls:

        poll_query = "SELECT * from polls where title=%s"
        cursor.execute(poll_query, (poll.question,))
        result = cursor.fetchone()

        if result:
            sys.stderr.write("Poll with title: %s  already exists, skipping\n" % poll.question)
            continue

        # check that the poll closes in more than a half-hour from now
        if (current_time + 1800) > poll.close_time:
            sys.stderr.write("Poll with close time: %d is in the past or less than 30 minutes "
                             "from now, skipping\n" % poll.close_time)
            continue

        sys.stdout.write("Poll with title: %s is valid!\n" % poll.question)
        valid_polls.append(poll)

    return valid_polls


def run(poll_filename: str) -> None:

    # set up db
    with open('admin/db.yml', 'r') as stream:
        try:
            db_config = yaml.load(stream)['db_creds']
        except yaml.YAMLError as e:
            sys.stderr.write(e)
            sys.stderr.write("\nUnable to load DB config\n\n")
            sys.exit()

    connection = psycopg2.connect(database=db_config['database'],
                                  user=db_config['user'],
                                  password=db_config['password'],
                                  host=db_config['host'],
                                  port=db_config['port'])
    cursor = connection.cursor()

    # load file
    polls_from_yaml = load_polls(poll_filename)

    # validate each poll, return if valid
    valid_polls = validate_polls(polls_from_yaml, cursor, connection)

    # insert poll and bank account with data
    for poll in valid_polls:
        poll.store_poll(cursor, connection)

    sys.stdout.write("\nSuccessfully stored %d new polls.\n\n" % len(valid_polls))
