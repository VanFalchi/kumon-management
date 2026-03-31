import os
import uuid
import requests
import base64


def get_token():
    client_id = os.getenv("EFI_CLIENT_ID")
    client_secret = os.getenv("EFI_CLIENT_SECRET")
    cert_path = os.getenv("EFI_CERT_PATH")
    key_path = os.getenv("EFI_KEY_PATH")
    sandbox = os.getenv("EFI_SANDBOX", "true").lower() == "true"

    base_url = "https://pix-h.api.efipay.com.br" if sandbox else "https://pix.api.efipay.com.br"

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{base_url}/oauth/token",
        headers=headers,
        data='{"grant_type": "client_credentials"}',
        cert=(cert_path, key_path)
    )
    return response.json()["access_token"], base_url, cert_path, key_path


def gerar_boleto_bolix(
    charge_id_interno: str,
    valor_cheio: float,
    valor_real: float,
    data_vencimento: str,
    nome_responsavel: str,
    cpf_responsavel: str,
    descricao: str = "Mensalidade Kumon"
):
    token, base_url, cert_path, key_path = get_token()
    desconto_valor = round(valor_cheio - valor_real, 2)
    txid = uuid.uuid4().hex[:26]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "calendario": {
            "dataDeVencimento": data_vencimento
        },
        "devedor": {
            "cpf": cpf_responsavel.replace(".", "").replace("-", ""),
            "nome": nome_responsavel
        },
        "valor": {
            "original": f"{valor_cheio:.2f}",
            "desconto": {
                "modalidade": 2,
                "descontoDataFixa": [
                    {
                        "data": data_vencimento,
                        "valorPerc": "10.00"
                    }
                ]
            }
        },
        "chave": os.getenv("EFI_PIX_KEY", ""),
        "infoAdicionais": [
            {"nome": "Referência", "valor": charge_id_interno},
            {"nome": "Descrição", "valor": descricao}
        ]
    }

    response = requests.put(
        f"{base_url}/v2/cobv/{txid}",
        headers=headers,
        json=body,
        cert=(cert_path, key_path)
    )
    result = response.json()
    result["txid"] = txid
    return result


def cancelar_boleto(txid: str):
    token, base_url, cert_path, key_path = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {"status": "REMOVIDA_PELO_USUARIO_RECEBEDOR"}
    response = requests.patch(
        f"{base_url}/v2/cobv/{txid}",
        headers=headers,
        json=body,
        cert=(cert_path, key_path)
    )
    return response.json()


def consultar_boleto(txid: str):
    token, base_url, cert_path, key_path = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{base_url}/v2/cobv/{txid}",
        headers=headers,
        cert=(cert_path, key_path)
    )
    return response.json()