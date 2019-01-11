from twilio.rest import Client
from twilio_credentials import authToken, accSid

client = Client(accSid, authToken)

def send(number, message):
    client.messages.create(
        to=number,
        from_='+16789495337',
        body=message
    )