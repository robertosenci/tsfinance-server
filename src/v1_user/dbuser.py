from src.database import Database
from flask import current_app
from src.utils import str2sql

class UserDAO(Database):
    def __init__(self):
        self.app = current_app

    def insert(self, user):
        query = (f"""
            INSERT INTO public."CAD_USUARIO" (
                ds_nome, 
                ds_email, 
                ds_senha, 
                nr_phone, 
                dt_nascimento, 
                nr_cpf, 
                tp_perfil, 
                sn_ativo, 
                sn_excluido)
            VALUES(
                {str2sql(user.get('username'))},
                {str2sql(user.get('email'))},
                {str2sql(user.get('password'))},
                {str2sql(user.get('phone'))},
                TO_DATE({str2sql(user.get('birthday'))}, 'DD/MM/YYYY'), 
                {str2sql(user.get('cpf'))},
                {str2sql(user.get('office'))},
                {user.get('active')},
                'false'
            )
        """)
        print(query)
        return self.exec_command(query)

    def update(self, user):
        query = (f"""
            UPDATE public."CAD_USUARIO" SET
                ds_nome = {str2sql(user['username'])}
              , ds_email = {str2sql(user['email'])} 
              , ds_senha = {str2sql(user['password'])}
              , nr_phone = {str2sql(user['phone'])} 
              , dt_nascimento = TO_DATE({str2sql(user.get('birthday'))}, 'DD/MM/YYYY')
              , nr_cpf = {str2sql(user.get('cpf'))}
              , tp_perfil = {str2sql(user.get('office'))}  
              , sn_ativo = {user.get('active')}
            WHERE id_usuario = {user['id']}
        """)
        print(query)
        return self.exec_command(query)

    def delete(self, codigo):
        query = (f"""
            DELETE public."CAD_USUARIO" 
            WHERE id_usuario = {codigo}
        """)
        print(query)
        return self.exec_command(query)

    def active(self, codigo, active):
        query = (f"""
            UPDATE public."CAD_USUARIO" SET
                sn_ativo = {active}
            WHERE id_usuario = {codigo}
        """)
        print(query)
        return self.exec_command(query)

    def get_by_cpf(self, cpf):
        query = (f"""
            SELECT * FROM public."CAD_USUARIO" WHERE nr_cpf = '{cpf}'
        """)
        print(query)
        return self.exec_query(query)


    def get_by_email(self, email):
        query = (f"""
            SELECT  
                id_usuario as id
              , ds_nome as name
              , ds_senha as senha
              , ds_email as email
              , nr_phone as phone
              , dt_nascimento as birthday
              , nr_cpf as cpf
              , tp_perfil as office
              , sn_ativo as active
            FROM public."CAD_USUARIO" WHERE ds_email = '{email}'
        """)
        return self.exec_query(query)
