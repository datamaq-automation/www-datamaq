import asyncio
import smtplib
from email.message import EmailMessage
from typing import Any, Dict

from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME)


class EmailNotificationGateway(NotificationGateway):
    """Envía notificaciones de nuevos leads por email usando SMTP."""

    def __init__(self, host: str, port: int, username: str, password: str, to_email: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._to_email = to_email

    async def notify_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("[EmailNotificationGateway] Enviando notificación de lead a %s", self._to_email)

        msg = EmailMessage()
        msg["Subject"] = f"Nuevo lead de DataMaq: {lead_data.get('name', 'Sin nombre')}"
        msg["From"] = self._username
        msg["To"] = self._to_email

        name = lead_data.get("name", "No proporcionado")
        email = lead_data.get("email", "No proporcionado")
        phone = lead_data.get("phone", "No proporcionado")
        comment = lead_data.get("comment", "")
        company = lead_data.get("company", "No proporcionada")
        source = lead_data.get("source", "No especificada")

        body = f"""Nuevo lead recibido desde datamaq.com.ar

Nombre: {name}
Email: {email}
Teléfono: {phone}
Empresa: {company}
Origen: {source}

Consulta:
{comment}
---
Este lead fue guardado en data/leads/ del proyecto.
"""
        msg.set_content(body)

        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(
                None,
                self._send_email,
                msg,
            )
            logger.info("[EmailNotificationGateway] Notificación enviada a %s", self._to_email)
            return {"status": "sent", "to": self._to_email}
        except Exception as e:
            logger.error("[EmailNotificationGateway] Error al enviar email: %s", e)
            raise

    def _send_email(self, msg: EmailMessage) -> None:
        with smtplib.SMTP(self._host, self._port, timeout=15) as server:
            server.starttls()
            server.login(self._username, self._password)
            server.send_message(msg)
