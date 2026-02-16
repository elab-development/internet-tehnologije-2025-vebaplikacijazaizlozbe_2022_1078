import logging
import httpx
import base64
from datetime import datetime
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

MAILERSEND_API_URL = "https://api.mailersend.com/v1/email"


def _build_registration_html(
    korisnik_ime: str,
    izlozba_naslov: str,
    broj_karata: int,
    datum_izlozbe: Optional[str] = None,
    lokacija: Optional[str] = None
) -> str:
    datum_html = f'<tr><td style="padding:8px 16px;color:#555;">📅 Datum:</td><td style="padding:8px 16px;font-weight:600;">{datum_izlozbe}</td></tr>' if datum_izlozbe else ""
    lokacija_html = f'<tr><td style="padding:8px 16px;color:#555;">📍 Lokacija:</td><td style="padding:8px 16px;font-weight:600;">{lokacija}</td></tr>' if lokacija else ""

    return f"""
    <!DOCTYPE html>
    <html lang="sr">
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;background-color:#f4f4f7;font-family:'Segoe UI',Arial,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f7;padding:40px 0;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
                        <!-- Header -->
                        <tr>
                            <td style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:40px 30px;text-align:center;">
                                <h1 style="color:#ffffff;margin:0;font-size:28px;font-weight:700;">🎨 Galerija</h1>
                                <p style="color:#e0d4f7;margin:8px 0 0;font-size:14px;">Potvrda prijave za izložbu</p>
                            </td>
                        </tr>
                        <!-- Body -->
                        <tr>
                            <td style="padding:30px;">
                                <p style="font-size:16px;color:#333;">Poštovani/a <strong>{korisnik_ime}</strong>,</p>
                                <p style="font-size:15px;color:#555;line-height:1.6;">
                                    Uspešno ste se prijavili za izložbu. Ispod su detalji vaše prijave:
                                </p>

                                <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8f7ff;border-radius:8px;margin:20px 0;border:1px solid #e8e5f3;">
                                    <tr>
                                        <td style="padding:8px 16px;color:#555;">🖼️ Izložba:</td>
                                        <td style="padding:8px 16px;font-weight:600;color:#333;">{izlozba_naslov}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:8px 16px;color:#555;">🎫 Broj karata:</td>
                                        <td style="padding:8px 16px;font-weight:600;color:#333;">{broj_karata}</td>
                                    </tr>
                                    {datum_html}
                                    {lokacija_html}
                                </table>

                                <!-- QR Kod -->
                                <div style="text-align:center;margin:30px 0;padding:20px;background:#fafafa;border-radius:8px;border:2px dashed #ddd;">
                                    <p style="color:#667eea;font-weight:600;margin:0 0 12px;">Vaš QR kod za ulaz:</p>
                                    <img src="cid:qr_code" alt="QR Kod" style="width:200px;height:200px;" />
                                    <p style="color:#999;font-size:12px;margin:12px 0 0;">Pokažite ovaj QR kod na ulazu u galeriju</p>
                                </div>

                                <p style="font-size:13px;color:#999;line-height:1.5;border-top:1px solid #eee;padding-top:16px;">
                                    Ova poruka je automatski generisana. Molimo vas da ne odgovarate na ovaj email.
                                </p>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background:#f8f7ff;padding:20px 30px;text-align:center;border-top:1px solid #e8e5f3;">
                                <p style="color:#888;font-size:13px;margin:0;">Srdačan pozdrav,<br><strong>Tim Galerija</strong></p>
                                <p style="color:#aaa;font-size:11px;margin:8px 0 0;">© {datetime.now().year} Galerija - Sva prava zadržana</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _build_validation_html(korisnik_ime: str, izlozba_naslov: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="sr">
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;background-color:#f4f4f7;font-family:'Segoe UI',Arial,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f7;padding:40px 0;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
                        <tr>
                            <td style="background:linear-gradient(135deg,#43e97b 0%,#38f9d7 100%);padding:40px 30px;text-align:center;">
                                <h1 style="color:#ffffff;margin:0;font-size:28px;font-weight:700;">✅ Karta Validirana</h1>
                                <p style="color:#d4fff0;margin:8px 0 0;font-size:14px;">Hvala na poseti!</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:30px;">
                                <p style="font-size:16px;color:#333;">Poštovani/a <strong>{korisnik_ime}</strong>,</p>
                                <p style="font-size:15px;color:#555;line-height:1.6;">
                                    Vaša karta za izložbu <strong>"{izlozba_naslov}"</strong> je uspešno validirana.
                                </p>
                                <div style="text-align:center;margin:25px 0;padding:20px;background:#f0fff4;border-radius:8px;border:1px solid #c6f6d5;">
                                    <p style="font-size:18px;color:#38a169;font-weight:600;margin:0;">🎉 Dobrodošli!</p>
                                    <p style="color:#555;font-size:14px;margin:8px 0 0;">Uživajte u izložbi!</p>
                                </div>
                                <p style="font-size:13px;color:#999;line-height:1.5;border-top:1px solid #eee;padding-top:16px;">
                                    Ova poruka je automatski generisana. Molimo vas da ne odgovarate na ovaj email.
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background:#f0fff4;padding:20px 30px;text-align:center;border-top:1px solid #c6f6d5;">
                                <p style="color:#888;font-size:13px;margin:0;">Srdačan pozdrav,<br><strong>Tim Galerija</strong></p>
                                <p style="color:#aaa;font-size:11px;margin:8px 0 0;">© {datetime.now().year} Galerija - Sva prava zadržana</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _extract_base64_from_data_uri(data_uri: str) -> str:
    if data_uri.startswith("data:"):
        return data_uri.split(",", 1)[1]
    return data_uri


def _send_email_via_mailersend(
    to_email: str,
    to_name: str,
    subject: str,
    html_content: str,
    text_content: str,
    attachments: list = None
) -> bool:
    api_key = settings.MAILERSEND_API_KEY
    from_email = settings.MAILERSEND_FROM_EMAIL
    from_name = settings.MAILERSEND_FROM_NAME

    if not api_key:
        logger.warning("MAILERSEND_API_KEY nije podešen. Email neće biti poslat.")
        return False

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": {
            "email": from_email,
            "name": from_name,
        },
        "to": [
            {
                "email": to_email,
                "name": to_name,
            }
        ],
        "subject": subject,
        "html": html_content,
        "text": text_content,
    }

    if attachments:
        payload["attachments"] = attachments

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(MAILERSEND_API_URL, json=payload, headers=headers)

        if response.status_code == 202:
            message_id = response.headers.get("x-message-id", "N/A")
            logger.info(f"Email uspešno poslat na {to_email}. Message ID: {message_id}")
            return True
        else:
            logger.error(
                f"Greška pri slanju emaila. Status: {response.status_code}, "
                f"Odgovor: {response.text}"
            )
            return False

    except httpx.TimeoutException:
        logger.error(f"Timeout pri slanju emaila na {to_email}")
        return False
    except Exception as e:
        logger.error(f"Neočekivana greška pri slanju emaila: {str(e)}")
        return False


def send_registration_email(
    email: str,
    korisnik_ime: str,
    izlozba_naslov: str,
    qr_image: str,
    broj_karata: int,
    datum_izlozbe: Optional[str] = None,
    lokacija: Optional[str] = None
) -> bool:
    try:
        html_content = _build_registration_html(
            korisnik_ime=korisnik_ime,
            izlozba_naslov=izlozba_naslov,
            broj_karata=broj_karata,
            datum_izlozbe=datum_izlozbe,
            lokacija=lokacija
        )
        text_content = (
            f"Poštovani/a {korisnik_ime},\n\n"
            f"Uspešno ste se prijavili za izložbu: {izlozba_naslov}\n"
            f"Broj karata: {broj_karata}\n"
        )
        if datum_izlozbe:
            text_content += f"Datum: {datum_izlozbe}\n"
        if lokacija:
            text_content += f"Lokacija: {lokacija}\n"
        text_content += (
            "\nQR kod za ulaz je u prilogu ovog emaila.\n"
            "Molimo vas da ga pokažete na ulazu.\n\n"
            "Srdačan pozdrav,\nTim Galerija"
        )
        qr_base64 = _extract_base64_from_data_uri(qr_image)
        attachments = [
            {
                "filename": "qr_kod.png",
                "content": qr_base64,
                "disposition": "inline",
                "id": "qr_code",
            }
        ]
        return _send_email_via_mailersend(
            to_email=email,
            to_name=korisnik_ime,
            subject=f"Potvrda prijave - {izlozba_naslov}",
            html_content=html_content,
            text_content=text_content,
            attachments=attachments,
        )

    except Exception as e:
        logger.error(f"Greška pri slanju emaila za prijavu: {str(e)}")
        return False


def send_validation_email(
    email: str,
    korisnik_ime: str,
    izlozba_naslov: str
) -> bool:
    try:
        html_content = _build_validation_html(korisnik_ime, izlozba_naslov)

        text_content = (
            f"Poštovani/a {korisnik_ime},\n\n"
            f"Vaša karta za izložbu '{izlozba_naslov}' je uspešno validirana.\n"
            "Hvala vam na poseti!\n\n"
            "Srdačan pozdrav,\nTim Galerija"
        )

        return _send_email_via_mailersend(
            to_email=email,
            to_name=korisnik_ime,
            subject=f"Karta validirana - {izlozba_naslov}",
            html_content=html_content,
            text_content=text_content,
        )

    except Exception as e:
        logger.error(f"Greška pri slanju emaila za validaciju: {str(e)}")
        return False
