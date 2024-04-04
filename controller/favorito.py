from utils.auth import validar_token
from flask import request
from schemas import *
from model import Session, Favorito, Usuario
from logger import logger
from datetime import datetime
from sqlalchemy import desc
import jwt


class FavoritoControlador:
    def cadastrar_favorito(form: FavoritoSchema):
        """Cadastra um favorito.

        Args:
            form (FavoritoSchema): O formulário contendo os dados.

        Returns:
            tuple: O favorito.
        """
        session = Session()

        try:
            token = validar_token(request.headers.get("Token"))
        except (Exception, jwt.ExpiredSignatureError):
            error_msg = "Token não fornecido ou inválido."
            logger.warning(
                f"Erro ao adicionar favorito', {error_msg}")
            return {"message": error_msg}, 401

        try:
            usuario = session.query(Usuario).filter(
                Usuario.id == token['id']).first()

            favorito = Favorito(
                url=form.url,
                titulo=form.titulo,
                descricao=form.descricao,
                data_insercao=datetime.now())
            usuario.adiciona_favorito(favorito=favorito)

            session.add(favorito)
            session.commit()
            return apresenta_favorito(favorito)
        except Exception as e:
            error_msg = "Não foi possível adicionar o favorito."
            logger.warning(
                f"Erro ao adicionar favorito', {error_msg}")
            return {"message": error_msg}, 400

    def obter_favoritos():
        """Retorna os favoritos mais recentes.

        Returns:
            tuple: A lista em JSON.
        """
        session = Session()
        busca = session.query(Favorito).order_by(
            desc(Favorito.data_insercao)).limit(10).all()

        return apresenta_favoritos(busca)

    def obter_meus_favoritos():
        """Retorna os favoritos de um usuário específico.

        Returns:
            tuple: A lista em JSON.
        """
        session = Session()

        try:
            token = validar_token(request.headers.get("Token"))
        except (Exception, jwt.ExpiredSignatureError):
            error_msg = "Token não fornecido ou inválido."
            logger.warning(
                f"Erro ao obter favoritos, {error_msg}")
            return {"message": error_msg}, 401

        try:
            busca = session.query(Favorito).order_by(
                desc(Favorito.data_insercao)).filter(
                Favorito.usuario == token['id']).limit(10).all()
            return apresenta_favoritos(busca)
        except Exception as e:
            error_msg = "Não foi possível obter os favoritos."
            logger.warning(
                f"Erro ao obter favoritos, {error_msg}")
            return {"message": error_msg}, 400

    def remover_favorito(favorito: FavoritoBuscaSchema):
        """Remove o favorito de acordo com o id fornecido

        Returns:
            dict: Retorno em JSON.
        """
        session = Session()
        usuario_id = 0

        try:
            token = validar_token(request.headers.get("Token"))
            usuario_id = token['id']
        except (Exception, jwt.ExpiredSignatureError):
            error_msg = "Token não fornecido ou inválido."
            logger.warning(
                f"Erro ao obter favoritos, {error_msg}")
            return {"message": error_msg}, 401

        try:
            favorito = session.query(Favorito).filter_by(
                id=favorito.id, usuario=usuario_id).delete()
            session.commit()

            if not favorito:
                raise Exception

            return {"removido": favorito}, 200
        except Exception as e:
            error_msg = "Não foi possível encontrar o favorito."
            logger.warning(
                f"Erro ao obter favoritos, {error_msg}")
            return {"message": error_msg}, 400
