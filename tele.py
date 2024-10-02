import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def send_to_telegram(message, bot_token, chat_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Optional: use 'HTML' or 'Markdown' if you want to format the message
    }

    # Configure retry strategy
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        response = http.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

def read_blocked_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    bot_token = 'replace with your bot token'
    chat_id = 'replace with your chat ID'
    
    blocked_message = read_blocked_file('blocked.txt')
    id_message = read_blocked_file('id.txt')
    
    # Include id_message directly in the URL
    message = f'{blocked_message}\n<a href="http://yourdomain:3000/api/{id_message}">Click here for details</a>'
    
    send_to_telegram(message, bot_token, chat_id)
