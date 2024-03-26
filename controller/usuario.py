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
    def add_usuario(form: UsuarioSchema):
        """Adiciona um usuário.

        Args:
            form (UsuarioSchema): Os dados do usuário.

        Returns:
            _type_: _description_
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
            return apresenta_usuario(usuario), 201

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
            _type_: _description_
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
            token = gerar_token(usuario.nome, usuario.email)
            resp = make_response({"token": token}, 200)
            return resp

    def get_usuario(query: UsuarioBuscaSchema):
        """Retorna um usuário a partir do id

        Args:
            query (UsuarioBuscaSchema): O id.

        Returns:
            _type_: _description_
        """
        usuario_id = query.id
        logger.debug(f"Obtendo usuário de id #{usuario_id}")

        try:
            token = request.headers['Token']
            validar_token(token)
        except:
            error_msg = "Usuário não autorizado."
            logger.warning(
                f"Usuário não autorizado #'{usuario_id}'")
            return {"message": error_msg}, 401

        session = Session()
        usuario = session.query(Usuario).filter(
            Usuario.id == usuario_id).first()
        session.commit()

        if usuario:
            logger.debug(f"Buscando usuário #{usuario_id}")
            return apresenta_usuario(usuario), 200
        else:
            logger.warning(
                f"Erro ao buscar usuário de id #'{usuario_id}")
            return {"message": error_msg}, 404