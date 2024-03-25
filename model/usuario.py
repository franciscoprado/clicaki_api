from sqlalchemy import Column, String, Integer
from datetime import datetime
from typing import Union

from  model import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    senha = Column(String(162), nullable=False)

    def __init__(self, nome: str, email:str, senha:str):
        """
        Cria um usuário

        Arguments:
            nome: O nome do usuário.
            email: o email do usuário.
            senha: a senha escolhida pelo usuário.
        """
        self.nome = nome
        self.email = email
        self.senha = senha
