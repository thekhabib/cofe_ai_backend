import qrcode
from io import BytesIO
import requests
from django.conf import settings

def generate_qr_image(slug: str) -> BytesIO:
    link = f"https://t.me/{settings.BOT_USERNAME}?start={slug}"
    img = qrcode.make(link)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def send_qr_to_telegram_channel(image: BytesIO, caption: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendPhoto"
    files = {'photo': ('qr.png', image)}
    data = {
        'chat_id': settings.TELEGRAM_CHANNEL_ID,
        'caption': caption
    }
    response = requests.post(url, data=data, files=files)
    if response.status_code != 200:
        print(f"Ошибка отправки QR-кода: {response.text}")

def generate_all_desk_qrs(library):
    """Генерирует QR-коды для всех столов библиотеки и отправляет в канал"""
    for desk_number, desk_slug in enumerate(library.get_desk_slugs(), start=1):
        try:
            qr_image = generate_qr_image(desk_slug)
            send_qr_to_telegram_channel(
                qr_image,
                caption=f"{library.name} - Стол №{desk_number}\nСсылка: t.me/{settings.BOT_USERNAME}?start={desk_slug}"
            )
        except Exception as e:
            print(f"Ошибка при генерации QR-кода для {desk_slug}: {str(e)}")