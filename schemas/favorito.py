from typing import List
from pydantic import BaseModel


class FavoritoSchema(BaseModel):
    """ Define como um novo favorito a ser inserido deve ser representado
    """
    url: str
    titulo: str
    descricao: str


class FavoritoViewSchema(BaseModel):
    """ Define como um novo favorito deve ser representado
    """
    id: int
    url: str
    titulo: str
    descricao: str
    usuario: int


class FavoritoBuscaSchema(BaseModel):
    """ Define como buscar um favorito a partir do seu título.
    """
    titulo: str


class ListagemFavoritoSchema(BaseModel):
    """ Define como uma listagem de favoritos será retornada.
    """
    favoritos: List[FavoritoSchema]


def apresenta_favorito(favorito: FavoritoSchema):
    """ Retorna uma representação do favorito seguindo o schema definido em
        FavoritoSchema.
    """
    return {
        "id": favorito.id,
        "url": favorito.url,
        "titulo": favorito.titulo,
        "descricao": favorito.descricao,
        "data_insercao": favorito.data_insercao
    }
