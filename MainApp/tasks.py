from celery import shared_task
import requests
chat_id = "chat id"
chat_token = "Your telegram secret key"
URL = 'https://api.telegram.org/bot' + chat_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=html&text=Hi This is Test message'


@shared_task
def send_telegram_message(): # To get arguments -> def send_telegram_message(self, data):
    for i in range(5):
        final_url = URL+str(i)
        requests.post(url = final_url)
    return "Congratulations! All sessages sent Successfully"


