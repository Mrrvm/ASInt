import requests
import time


def turn_on_bot():
    print("Insert Bot ID, key and message")
    bot_id = int(input("Bot ID:"))
    key = input("Key:")
    message = input("Message:")
    return bot_id, key, message

if __name__ == '__main__':
    bot_id, key, message = turn_on_bot()
    while(1):
        toSend = {'id': bot_id, 'key': key, 'message': message}
        r = requests.post('http://127.0.0.1:5000/bot', json=toSend)  # TODO change IP to any
        bot_response = r.json()
        if bot_response['status'] == "error":
            print("Error during message sending.")
            exit(0)
        time.sleep(60)