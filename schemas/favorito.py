from typing import List
from pydantic import BaseModel, validator, AnyHttpUrl


class FavoritoSchema(BaseModel):
    """ Define como um novo favorito a ser inserido deve ser representado
    """
    id: int = 1
    url: AnyHttpUrl
    titulo: str
    descricao: str
    curtidas: int = 0

    @validator('titulo')
    def verifica_titulo(cls, v):
        """Verifica se o título não está sem preenchimento"""
        if not v:
            raise ValueError("O título não pode ser em branco.")

        return v


class FavoritoViewSchema(BaseModel):
    """ Define como um novo favorito deve ser representado
    """
    id: int
    url: AnyHttpUrl = "http://www.exemplo.com.br"
    titulo: str = "Meu link favorito"
    descricao: str = "Descrição do link"
    curtidas: int = 0


class FavoritoBuscaSchema(BaseModel):
    """ Define como buscar um favorito a partir do seu id.
    """
    id: int = 1


class ListagemFavoritoSchema(BaseModel):
    """ Define como uma listagem de favoritos será retornada.
    """
    favoritos: List[FavoritoSchema]
    paginas_total: int


class FavoritoPaginaSchema(BaseModel):
    """ Define a pagina da lista de resultados.
    """
    pagina: int = 1


def apresenta_favorito(favorito: FavoritoSchema):
    """ Retorna uma representação do favorito seguindo o schema definido em
        FavoritoSchema.
    """
    return {
        "id": favorito.id,
        "url": favorito.url,
        "titulo": favorito.titulo,
        "descricao": favorito.descricao,
        "curtidas": favorito.curtidas,
        "data_insercao": favorito.data_insercao
    }, 200


def apresenta_favoritos(favoritos: List[BaseModel], paginas_total: int):
    """ Retorna uma representação de lista de favoritos.

    Args:
        favoritos (List[BaseModel]): A lista de favoritos buscada do banco.
        paginas_total (int): O total de páginas

    Returns:
        dict: Lista dos favoritos FavoritoSchema. 
    """
    lista = []
    codigo = 200

    for favorito in favoritos:
        lista.append(
            {'id': favorito.id, 'url': favorito.url, 'titulo': favorito.titulo, 'descricao': favorito.descricao, 'curtidas': favorito.curtidas, 'data_insercao': favorito.data_insercao})

    if not lista:
        codigo = 204

    return {"favoritos": lista, "paginas_total": paginas_total}, codigo
