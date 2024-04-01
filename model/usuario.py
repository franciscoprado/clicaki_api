from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from model import Base, Favorito


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column("id", Integer, primary_key=True)
    nome = Column(String(250), nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    senha = Column(String(162), nullable=False)
    favoritos = relationship("Favorito")

    def __init__(self, nome: str, email: str, senha: str):
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

    def adiciona_favorito(self, favorito: Favorito):
        """ Adiciona um novo local atrelado ao usuário
        """
        self.favoritos.append(favorito)
