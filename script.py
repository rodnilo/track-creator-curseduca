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
from functions import find_id_by_title
from functions import enroll
from functions import enroll_tenant
from functions import enroll_group
from functions import identify
from functions import get_contents
from functions import revoke
from functions import register
from functions import get_enrollments
from functions import identify_users_enrollments
from functions import restore_enrollments
from functions import register_with_contents
from functions import inactivate
from functions import revoke_all

if input_data['action'] == 'update':
    try:
        print(f"Operação a ser realizada: {input_data['action']} \n 0/4 etapas concluídas")
        token = auth()
        print(f"Autenticação realizada. \n 1/4 etapas")
        email = input_data['email_update']
        print(f"E-mail a ser atualizado: {email}")
        conteudos_selecionados = input_data['contents_update'] #.split(",") # esta e a próxima linha precisam ser descomentadas para funcionar corretamente no Zapier
        # conteudos_selecionados = [i.strip() for i in conteudos_selecionados]
        print(f"Conteúdos selecionados para serem matriculados: {conteudos_selecionados} \n 2/4 etapas")
        conteudos = get_contents(token)
        member_id = identify(email)
        print(f"ID do membro {email}: {member_id}. \n 3/4 etapas")
        status_enroll = enroll(member_id, conteudos=conteudos, conteudos_selecionados=conteudos_selecionados, token=token)
        print(f"Matrículas realizadas: {status_enroll}. \n 4/4 etapas.")
    except KeyError as e:
        print(e)

elif input_data['action'] == 'create':
    try:
        print(f"Operação a ser realizada: {input_data['action']}. \n 0/4 etapas concluídas")
        token = auth()
        print(f"Autenticação realizada. \n 1/4 etapas concluídas")
        nome = input_data['name']
        group_id = input_data['group_id']
        tenant_uuid = input_data['tenant_uuid']
        email = input_data['email_create']
        conteudos = get_contents(token)
        conteudos_selecionados = input_data['contents_create'] #.split(",")
        print(f"Dados a serem preenchidos: \n nome: {nome}; \n email: {email}; \n turma: {group_id}; \n plataforma: {tenant_uuid}; \nConteúdos Selecionados: {conteudos_selecionados}")
        # conteudos_selecionados = [i.strip() for i in conteudos_selecionados]
        member_id = register_with_contents(token=token,
                                           name=nome,
                                           email=email,
                                           conteudos_selecionados=conteudos_selecionados,
                                           conteudos=conteudos)
        print(f"Resposta do register_with_contents: {member_id}. \n 2/4 etapas")
        response_enroll_group = enroll_group(token, member_id, group_id)
        print(f"Resposta do enroll_group: {response_enroll_group}. \n 3/4 etapas")
        response_enroll_tenant = enroll_tenant(token, member_id, tenant_uuid)
        print(f"Resposta do enroll_tenant: {response_enroll_tenant}. \n 4/4 etapas")

    except KeyError as e:
        print(e)

elif input_data['action'] == 'delete':
    try:
        print(f"Operação a ser realizada: {input_data['action']}. \n 0/2 etapas concluídas")
        token = auth()
        print(f"Autenticação realizada. \n 1/2 etapas")
        email = input_data['email_delete']
        print(f"Email a ser desativado: {email}")
        response_inactivate = inactivate(email, token)
        print(f"Resposta ação {input_data['action']}: {response_inactivate}. \n 2/2 etapas")

    except KeyError as e:
        print(e)

elif input_data['action'] == 'create_track_new_user':
    try:
        print(f"Operação a ser realizada: {input_data['action']}. \n 0/5 etapas concluídas")
        token = auth()
        print(f"Autencicação realizada. \n 1/5 etapas")
        name = input_data['name_create_track']
        email = input_data['email_create_track_new']
        group_id = input_data['group_id']
        tenant_uuid = input_data['tenant_uuid']
        conteudos_selecionados = input_data['contents_create_track_new']#.split(",") # esta e a próxima linha precisam ser descomentadas para funcionar corretamente no Zapier
        # conteudos_selecionados = [i.strip() for i in conteudos_selecionados]
        print(f"Nome a ser criado: {name} \n E-mail a ser criado: {email} \n Conteúdos da trilha: {conteudos_selecionados}")
        conteudos = get_contents(token)
        member_id = register(name=name, email=email, token=token)
        print(f"Usuário gerado: {member_id} \n 1/X etapas concluídas")
        response_enroll_group = enroll_group(id=member_id, group_id=group_id, token=token)
        print(f"Usuário {member_id} inserido na turma {group_id}. \n Resposta da solicitação: {response_enroll_group} \n 2/5 etapas concluídas")
        response_enroll_tenant = enroll_tenant(id=member_id, tenant_uuid=tenant_uuid, token=token)
        print(f"Usuário {member_id} inserido no tenant {tenant_uuid} \n Resposta da solicitação: {response_enroll_tenant} \n 3/5 etapas concluídas")
        enrolled_contents = enroll(member_id=member_id, conteudos_selecionados=conteudos_selecionados, conteudos=conteudos, token=token)
        print(f"{len(enrolled_contents)} matrículas realizadas. Os ids são: {enrolled_contents} \n 4/5 etapas concluídas")
        revoked_contents = revoke(enrolled_contents, token=token)
        conteudos_selecionados.pop(0)
        print(f"Os conteúdos: \n {conteudos_selecionados} \n foram bloqueados para o aluno {name} identificador {member_id}. \n 5/5 etapas concluídas. \n Operação realizada com sucesso.")

    except KeyError as e:
        print(e)

elif input_data['action'] == 'create_track_existing_user':
    try:
        print(f"Operação a ser realizada {input_data['action']}. \n 0/X etapas concluídas.")
        token = auth()
        email = input_data['email_create_track_existing']
        conteudos_selecionados = input_data['contents_create_track_existing']#.split(",") # esta e a próxima linha precisam ser descomentadas para funcionar corretamente no Zapier
        # conteudos_selecionados = [i.strip() for i in conteudos_selecionados]
        conteudos = get_contents(token)
        member_id = identify(email=email)
        print(f"Email existente: {email}. Identificador: {member_id}")
        enrolled_contents = enroll(member_id=member_id, conteudos=conteudos, conteudos_selecionados=conteudos_selecionados, token=token)
        print(f"{len(enrolled_contents)} matrículas realizadas. Os ids são: {enrolled_contents} \n 4/X etapas concluídas")
        revoked_contents = revoke(enrolled_contents, token=token)
        conteudos_selecionados.pop(0)
        print(f"Os conteúdos: \n {conteudos_selecionados} \n foram bloqueados para o aluno {email} identificador {member_id}")
    except KeyError as e:
        print(e)

elif input_data['action'] == 'release_track':
    try:
        print(f"Operação a ser realizada {input_data['action']}. \n 0/3 etapas concluídas.")
        token = auth()
        email = input_data['email_release_track']
        conteudos_selecionados = input_data['contents_release']#.split(",") # esta e a próxima linha precisam ser descomentadas para funcionar corretamente no Zapier
        # conteudos_selecionados = [i.strip() for i in conteudos_selecionados]
        conteudos = get_contents(token)
        member_id = identify(email=email)
        print(f"Email existente: {email}. Identificador: {member_id}. \n 1/3 etapas concluídas")
        enrollments = get_enrollments(token)
        content_ids = find_id_by_title(conteudos, conteudos_selecionados)
        print(content_ids)
        member_enrollments = identify_users_enrollments(enrollments, member_id=member_id, content_ids=content_ids)
        print(f"{len(member_enrollments)} identificado para liberação, identificador {member_enrollments}. \n 2/3 etapas concluídas")
        restored_enrollments = restore_enrollments(member_enrollments, token=token)
        print(f"{len(restored_enrollments)} identificado para liberação, identificador {member_enrollments}. \n 3/3 etapas concluídas")
    except KeyError as e:
        print(e)


elif input_data['action'] == 'revoke_all':
    try:
        print(f"Operação a ser realizada {input_data['action']}. \n 0/X etapas concluídas.")
        token = auth()
        email = input_data['email_revoke_all']
        conteudos_selecionados = input_data['contents_to_revoke']#.split(",") # esta e a próxima linha precisam ser descomentadas para funcionar corretamente no Zapier
        # conteudos_selecionados = [i.strip() for i in conteudos_selecionados]
        conteudos = get_contents(token)
        member_id = identify(email)
        print(f"Email existente: {email}. Identificador: {member_id}")
        enrollments = get_enrollments(token)
        content_ids = find_id_by_title(conteudos, conteudos_selecionados)
        member_enrollments = identify_users_enrollments(enrollments, member_id=member_id, content_ids=content_ids)
        print(f"Matrículas identificadas: {member_enrollments}")
        revoked_contents = revoke_all(enrollments=member_enrollments, token=token)
        print(f"Os conteúdos: \n {conteudos_selecionados} \n foram bloqueados para o aluno {email} identificador {member_id}")
    except KeyError as e:
        print(e)