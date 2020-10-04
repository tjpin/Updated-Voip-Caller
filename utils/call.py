from twilio.rest import Client
from accounts import account_sid, twilio_number, auth_token


class MakeCall:
    client = Client(account_sid, auth_token)

    def __init__(self, _to, _url, _from):
        self._to = _to
        self._from = twilio_number
        self._url = _url

    @staticmethod
    def make_call(to, from_, twiml, timeout=0):
        client = Client(account_sid, auth_token)
        try:
            call = client.calls.create(
                twiml=twiml,
                to=to,
                from_=from_
            )
            print(call.sid)
            return call
        except ConnectionAbortedError:
            return False

    def end_call(self):
        pass
