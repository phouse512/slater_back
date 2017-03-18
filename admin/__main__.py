import sys


from admin.add_poll import run as add_run
from admin.close_poll import run as close_run
from admin.remove_user import run as remove_user_run


class IncorrectArgumentException(BaseException):

    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


def run():
    command_name = sys.argv[1]

    if command_name == 'close_poll':

        if len(sys.argv) != 4:
            raise IncorrectArgumentException

        close_run(sys.argv[2], sys.argv[3])

    elif command_name == 'add_poll':

        if len(sys.argv) != 3:
            raise IncorrectArgumentException

        add_run(sys.argv[2])

    elif command_name == 'delete_user':

        if len(sys.argv) != 3:
            raise IncorrectArgumentException

        remove_user_run(sys.argv[2])

    else:
        sys.stdout.write("\nCommand not found. Aborting..\n\n")
        sys.exit()


try:
    run()
except IncorrectArgumentException as e:
    sys.stderr.write("\nIncorrect number of arguments given. Aborting..\n\n")
    sys.exit()
