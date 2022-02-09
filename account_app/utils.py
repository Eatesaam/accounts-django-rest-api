from django.core.mail import EmailMessage


class Util:

    @staticmethod
    def send_email(self, data):
        email = EmailMessage(
            to=[data.get('to')], subject=data.get('subject'), body=data.get('body')
        )

        email.send()
