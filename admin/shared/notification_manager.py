from admin.shared.notification import Notification
from admin.shared.sender import Sender


class NotificationManager(object):
    """
    the class responsible for taking notifications, gathering the
    appropriate info and then sending it to its respective sender
    """

    def __init__(self):
        self.senders = []  # type: List[Sender]

    def add_sender(self, sender: Sender):
        self.senders.append(sender)

    def send_notification(self, notification: Notification):

        for sender in self.senders:
            sender.send(notification)
