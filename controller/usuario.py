import re

from flask import redirect, request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from logger import logger
from sqlalchemy.exc import IntegrityError

from schemas import *
from utils import *
from model import Session, Usuario

# regex para validação de e-mail
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


class UsuarioControlador:
    def adicionar_usuario(form: UsuarioSchema):
        """Adiciona um usuário.

        Args:
            form (UsuarioSchema): Os dados do usuário.

        Returns:
            UsuarioTokenSchema: O token do usuário.
        """
        if not EMAIL_REGEX.match(form.email) or not form.nome or not form.senha:
            error_msg = "Dados inválidos"
            return {"message": error_msg}, 403

        usuario = Usuario(
            nome=form.nome,
            email=form.email,
            senha=generate_password_hash(form.senha))

        try:
            session = Session()
            session.add(usuario)
            session.commit()
            logger.debug(f"Adicionado usuário de e-mail: '{usuario.email}'")
            token = gerar_token(usuario)
            resp = make_response({"token": token}, 200)
            return resp

        except IntegrityError as e:
            error_msg = "Usuário com o mesmo e-mail já existente."
            logger.warning(
                f"Erro ao adicionar usuário '{usuario.email}', {error_msg}")
            return {"message": error_msg}, 409

        except Exception as e:
            error_msg = "Não foi possível adicionar o usuário."
            logger.warning(
                f"Erro ao adicionar usuário '{usuario.email}', {error_msg}")
            return {"message": error_msg}, 400

    def login(form: UsuarioLoginSchema):
        """Faz o login de usuário e retorna o token.

        Args:
            form (UsuarioLoginSchema): Dados de login.

        Returns:
            UsuarioTokenSchema: O token do usuário.
        """
        email = form.email
        senha = form.senha
        logger.debug(f"Coletando dados sobre usuário de e-mail #{email}")
        session = Session()
        usuario = session.query(Usuario).filter(
            Usuario.email == email).first()

        if not usuario:
            error_msg = "E-mail não encontrado na base :/"
            logger.warning(
                f"Erro ao buscar usuário de e-mail '{email}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            if not check_password_hash(usuario.senha, senha):
                error_msg = "Senha inválida."
                logger.error(error_msg)
                return {"message": error_msg}, 409

            logger.debug(f"Usuário econtrado: '{usuario.email}'")
            token = gerar_token(usuario)
            resp = make_response({"token": token}, 200)
            return resp

    def obter_usuario():
        """Retorna um usuário a partir do token

        Returns:
            UsuarioSchema: O usuário.
        """
        try:
            token = validar_token(request.headers['Token'])
        except:
            error_msg = "Usuário não autorizado."
            logger.warning(
                f"Usuário não autorizado'")
            return {"message": error_msg}, 401

        session = Session()
        usuario = session.query(Usuario).filter(
            Usuario.id == token['id']).first()
        session.commit()

        if usuario:
            logger.debug(f"Buscando usuário #{usuario.id}")
            return apresenta_usuario(usuario), 200
        else:
            logger.warning(
                f"Erro ao buscar usuário de id #'{usuario.id}")
            return {"message": error_msg}, 404
