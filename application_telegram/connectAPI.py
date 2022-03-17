from telethon.sync import TelegramClient
#Kết nối với telegram
def connectClientTelegram():
    try:
        api_id = 18812462
        api_hash = "d9ee8054d89b7020eb90f064c1acae6a"
        phone = "+84 354482801"
        client = TelegramClient(phone,api_id,api_hash)
        return True
    except KeyError:
        return False