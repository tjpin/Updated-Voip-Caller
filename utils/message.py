from twilio.rest import Client
from twilio.rest import TwilioRestClient
from twilio.base.exceptions import TwilioRestException

from accounts import account_sid, twilio_number, auth_token


class Message():
    client = Client(account_sid, auth_token)

    def __init__(self, _to, callback_url, _from):
        self._to = _to
        self._from = twilio_number
        self.callback_url = callback_url

    def sendMessage(self, _to, from_, body, *args):
        try:
            message = self.client.messages.create(
                to=_to,
                from_=from_,
                body=body,
                status_callback=self.callback_url
            )
            return message
        except TwilioRestException:
            return False

    def inbox(self):
        sms_record = self.client.messages.list()

        msg_reciever = []
        msg = []
        date = []

        for record in sms_record:
            msg_reciever.append(record.to)
            msg.append(record.body)
            date.append(record.date_created.strftime("%b %d %Y %H:%M:%S"))
