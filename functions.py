import requests
import os
from dotenv import load_dotenv, dotenv_values

username = os.getenv("username")
password = os.getenv("password")
api_key = os.getenv("api_key")
endpoint_register = os.getenv("endpoint_register")
endpoint_contents = os.getenv("endpoint_contents")
endpoint_groups = os.getenv("endpoint_groups")
endpoint_tenants = os.getenv("endpoint_tenants")
endpoint_enrollments = os.getenv("endpoint_enrollments")
endpoint_inactivate = os.getenv("endpoint_inactivate")
endpoint_identify = os.getenv("endpoint_identify")
endpoint_enrollments_report = os.getenv("endpoint_enrollments_report")
endpoint_restore_enrollments = os.getenv("endpoint_restore_enrollments")
url = os.getenv("url")

headers = {
    "api_key": api_key,
    "Content-Type": "application/json"
}

def auth():
    """
    função de autenticação na api da curseduca, enviando user, password, apikey
    :return: retorna access_token
    """
    body = {
        "username": username,
        "password": password,
    }

    headers = {
        "api_key": api_key,
        "Content-Type": "application/json"
    }

    # Autentica
    response_post = requests.post(url, headers=headers, json=body)

    # Extrai token
    response_json = response_post.json()
    access_token = response_json['accessToken']
    return access_token


def inactivate(email, token):
    """
    Função que realiza a ação de remoção do usuário no typeform. muda o status na curseduca para inativo
    :param email: email escrito no typeform
    :param token: token resultado da função auth
    :return:
    """

    headers = {
        "api_key": api_key,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "member": {"entries": [email]}
    }
    response_patch = requests.patch(endpoint_inactivate, headers=headers, json=body)
    return response_patch.json()


def register(name, email, token):
    body = {
        "name": name,
        "email": email,
        "password": "123456",
        "sendConfirmationEmail": "true"
    }

    headers = {
        "api_key": api_key,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response_post = requests.post(endpoint_register, headers=headers, json=body)

    response_json = response_post.json()
    user_id = response_json['id']
    if type(user_id) is int:
        return user_id
    else:
        return response_json

def enroll_group(token, id, group_id):
    """
    Função que tem objetivo atribuir o usuário criado pela função register_with_contents à respectiva turma da empresa.
    :param token: token de acesso gerado pela função auth
    :param id: id do usuário gerado pela função register_with_contents
    :param group_id: group_id atribuído pelo typeform da empresa
    :return: retorna o body da chamada
    """

    body = {
        "member": {"id": id},
        "group": {"id": group_id},
        "customExpirationDate": "XXX"
    }

    headers = {
        "api_key": api_key,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response_post = requests.post(endpoint_groups, headers=headers, json=body)

    return response_post

def enroll_tenant(token, id, tenant_uuid):
    """
    Função que tem objetivo atribuir o usuário criado pela função register_with_contents ao respectivo tenant da empresa.
    :param token: token de acesso gerado pela função auth
    :param id: id do usuário gerado pela função register_with_contents
    :param tenant_uuid: tenant_uuid atribuído pelo typeform da empresa
    :return: retorna o body da chamada
    """
    body = {
        "member": {"id": id},
        "tenant": {"uuid": tenant_uuid}
    }

    headers = {
        "api_key": api_key,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response_post = requests.post(endpoint_tenants, headers=headers, json=body)

    return response_post