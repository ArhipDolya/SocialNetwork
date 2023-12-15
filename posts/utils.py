from datetime import datetime


def update_last_request(user):
    user.last_request = datetime.utcnow()
    user.save()