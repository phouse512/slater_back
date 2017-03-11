import abc
import subprocess
import sys

from admin.shared.notification import Notification


class Sender(abc.ABC):

    @abc.abstractmethod
    def load_db(self, cursor, connection):
        """
        add the db stuff
        """

    @abc.abstractmethod
    def send(self, notification: Notification):
        """
        send the actual notification
        """


class IOSSender(Sender):

    def load_db(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def send(self, notification: Notification):

        device_token_query = "SELECT token FROM device_tokens WHERE user_id=%s order by created_at desc LIMIT 1"
        self.cursor.execute(device_token_query, (notification.user_id,))
        result = self.cursor.fetchone()

        if not result:
            sys.stdout.write("User with id: %d does not have a device token.\n" % notification.user_id)
            return

        device_token = result[0]
        message = notification.message

        subprocess.call('/Users/PhilipHouse/Documents/Programming/ios_projects/gorush -ios -m "%s" '
                        '-i="/Users/PhilipHouse/Documents/Programming/ios_projects/slaterPush.pem" -t="%s" '
                        '-topic="come.phizzle.slater"' % (message, device_token), shell=True)

