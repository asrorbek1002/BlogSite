import requests

TELEGRAM_TOKEN = '8108945501:AAF9bnymPoj7UDE2f3nGNgZUIoQEH2G9poo'  # o‘zgaruvchi sifatida saqlab qo‘ying
ADMIN_CHAT_ID = '6194484795'  # Adminning Telegram ID-si

def notify_admin_telegram(comment):
    text = (
        f"📝 Yangi komment:\n"
        f"👤 Ismi: {comment.name}\n"
        f"📧 Email: {comment.email}\n"
        f"💬 Xabar: {comment.message}\n"
        f"📌 Post: {comment.post.title}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        'chat_id': ADMIN_CHAT_ID,
        'text': text
    }
    requests.post(url, data=data)
