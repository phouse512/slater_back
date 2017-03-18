import psycopg2
import sys
import yaml

from admin.shared.user import User


def run(username: str) -> None:

    with open('admin/db.yml', 'r') as stream:
        try:
            db_config = yaml.load(stream)['db_creds']
        except yaml.YAMLError as e:
            sys.stderr.write(e)
            sys.stderr.write("\nUnable to load DB config.\n\n")
            sys.exit()

    connection = psycopg2.connect(database=db_config['database'],
                                  user=db_config['user'],
                                  password=db_config['password'],
                                  host=db_config['host'],
                                  port=db_config['port'])
    cursor = connection.cursor()

    user_obj = User(username)
    if not user_obj.exists(cursor):
        sys.stderr.write("User: %s does not exist.\n" % username)
        sys.exit()

    sys.stdout.write("User: %s found in db.\n" % username)

    result = user_obj.delete(cursor, connection)
    if result:
        sys.stdout.write("User: %s was successfully deleted.\n" % username)
        sys.exit()
    else:
        sys.stdout.write("User: %s was not deleted.\n" % username)
        sys.exit()
