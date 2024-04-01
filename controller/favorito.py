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
            return apresenta_favorito(favorito), 200
        except Exception as e:
            error_msg = "Não foi possível adicionar o favorito."
            logger.warning(
                f"Erro ao adicionar favorito', {error_msg}")
            return {"message": error_msg}, 400

    def obter_favoritos():
        session = Session()
        busca = session.query(Favorito).order_by(
            desc(Favorito.data_insercao)).limit(10).all()
        favoritos = []
        
        if not busca:
            return {"favoritos": favoritos}, 204

        for favorito in busca:
            favoritos.append(
                {'url': favorito.url, 'titulo': favorito.titulo, 'descricao': favorito.descricao, 'data_insercao': favorito.data_insercao})

        return {"favoritos": favoritos}, 200
