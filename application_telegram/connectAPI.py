from telethon.sync import TelegramClient
#Kết nối với telegram
def connectClientTelegram():
    try:
        api_id = your_api_id
        api_hash = your_api_hash
        phone = your_phone
        client = TelegramClient(phone,api_id,api_hash)
        return True
    except KeyError:
        return False
