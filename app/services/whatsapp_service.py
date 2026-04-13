import os
import requests


class WhatsappService:
    def __init__(self):
        self.api_url = os.getenv("EVOLUTION_API_URL", "http://evolution:8080")
        self.api_key = os.getenv("EVOLUTION_API_KEY", "kumon-evolution-key")
        self.instance = os.getenv("EVOLUTION_INSTANCE", "kumon")

    def enviar_mensagem(self, telefone: str, mensagem: str):
        """
        Envia mensagem de texto via Evolution API.
        telefone: formato 5517991234567 (DDI + DDD + número, sem + ou espaços)
        """
        url = f"{self.api_url}/message/sendText/{self.instance}"
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "number": telefone,
            "text": mensagem
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()


def get_whatsapp_service():
    return WhatsappService()