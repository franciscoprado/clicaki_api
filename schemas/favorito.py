from typing import List
from pydantic import BaseModel


class FavoritoSchema(BaseModel):
    """ Define como um novo favorito a ser inserido deve ser representado
    """
    id: int = 1
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
    """ Define como buscar um favorito a partir do seu id.
    """
    id: int = 1


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
    }, 200


def apresenta_favoritos(favoritos: List[BaseModel]):
    """ Retorna uma representação de lista de favoritos.

    Args:
        favoritos (List[BaseModel]): A lista de favoritos buscada do banco.

    Returns:
        dict: Lista dos favoritos FavoritoSchema. 
    """
    lista = []
    codigo = 200

    for favorito in favoritos:
        lista.append(
            {'id': favorito.id, 'url': favorito.url, 'titulo': favorito.titulo, 'descricao': favorito.descricao, 'data_insercao': favorito.data_insercao})
        
    if not lista:
        codigo = 204

    return {"favoritos": lista}, codigo
