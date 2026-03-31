import os
import requests


class WhatsappService:
    def __init__(self, api_url: str, instance_id: str, token: str):
        self.api_url = api_url
        self.instance_id = instance_id
        self.token = token

    def enviar_mensagem(self, telefone: str, mensagem: str):
        """
        Envia mensagem de texto via Z-API.
        telefone: formato 5517991234567 (DDI + DDD + número)
        """
        url = f"{self.api_url}/instances/{self.instance_id}/token/{self.token}/send-text"
        payload = {
            "phone": telefone,
            "message": mensagem
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()


def get_whatsapp_service():
    return WhatsappService(
        api_url=os.getenv("ZAPI_BASE_URL"),
        instance_id=os.getenv("ZAPI_INSTANCE_ID"),
        token=os.getenv("ZAPI_TOKEN")
    )