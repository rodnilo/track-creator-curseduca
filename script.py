import os

input_data = os.getenv("input_data")
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

from functions import auth
from functions import enroll_tenant
from functions import enroll_group
from functions import register

name = input_data['name']
email = input_data['email']
tenant_uuid = input_data['tenant_uuid']
group_id = input_data['group_id']


token = auth()
try:
    member_id = register(name=name, email=email, token=token)
    print(f"Membro cadastrado: \n Nome: {name} \n E-mail: {email} \n Identificador: {member_id} \n Etapa 1/3 realizada")
except TypeError or KeyError as e:
    print("Erro ao cadastrar o membro. Erro: {e}")

try:
    enroll_tenant(id=member_id, token=token, tenant_uuid=tenant_uuid)
    print(f"Tenant {tenant_uuid} cadastrado para o membro {member_id} \n Etapa 2/3 realizada")
except TypeError or KeyError as e:
    print(f"Erro ao cadastrar tenant {tenant_uuid} para o membro {member_id}. Erro: {e}")
try:
    enroll_group(id=member_id, token=token, group_id=group_id)
    print(f"Grupo {group_id} cadastrado para o membro {member_id} \n Etapa 3/3 realizada")
except TypeError or KeyError as e:
    print(f"Erro ao cadastrar grupo {group_id} para o membro {member_id}. Erro: {e}")
