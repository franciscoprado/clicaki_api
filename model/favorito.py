from typing import Union
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from model import Base


class Favorito(Base):
    __tablename__ = 'favorito'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String(250))
    curtidas = Column(Integer, default=0)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, url: str,
                 titulo: str,
                 descricao: str,
                 curtidas: int,
                 data_insercao: Union[DateTime, None] = None):
        """Cria um favorito

        Args:
            url (str): A url.
            titulo (str): O título do link.
            descricao (str): A descrição do link
            data_insercao (Union[DateTime, None], optional): O usuário. Defaults to None.
        """
        self.url = url
        self.titulo = titulo
        self.descricao = descricao
        self.curtidas = curtidas

        if data_insercao:
            self.data_insercao = data_insercao
