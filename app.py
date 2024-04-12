from math import ceil
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from schemas import *
from flask_cors import CORS
from model import Session, Favorito
from datetime import datetime
from sqlalchemy import desc

info = Info(title="Clicaki", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição de um usuário à base")
favorito_tag = Tag(
    name="Favorito", description="Adição de um favorito à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/favorito', tags=[favorito_tag],
          responses={"201": FavoritoViewSchema, "400": ErrorSchema})
def post_favorito(form: FavoritoSchema):
    """Cadastra um favorito

    Args:
        form (FavoritoSchema): Os dados.

    Returns:
        tuple: O favorito cadastrado.
    """
    try:
        session = Session()
        favorito = Favorito(
            url=str(form.url),
            titulo=form.titulo,
            descricao=form.descricao,
            curtidas=form.curtidas,
            data_insercao=datetime.now())
        session.add(favorito)
        session.commit()
        return apresenta_favorito(favorito, 201)
    except Exception as e:
        return {"mensagem": "Campos inválidos"}, 400


@app.get('/favorito', tags=[favorito_tag],
         responses={"200": FavoritoViewSchema, "404": ErrorSchema})
def get_favorito(query: FavoritoBuscaSchema):
    """Retorna um favorito a partir do id

    Args:
        query (FavoritoBuscaSchema): O id do favorito.

    Returns:
        tuple: O favorito.
    """
    session = Session()
    busca = session.query(Favorito).get(query.id)

    if not busca:
        return {"mensagem": "Favorito não encontrado"}, 404

    return apresenta_favorito(busca)


@app.get('/favoritos', tags=[favorito_tag],
         responses={"200": ListagemFavoritoSchema, "204": ListagemFavoritoSchema})
def get_favoritos(query: FavoritoPaginaSchema):
    """Retorna últimos favoritos adicionados

    Args:
        query (FavoritoPaginaSchema): A página.

    Returns:
        tuple: A lista de favoritos.
    """
    session = Session()
    limite = 10
    pagina = (query.pagina - 1) * limite
    busca = session.query(Favorito).order_by(
        desc(Favorito.data_insercao)).limit(limite).offset(pagina).all()
    paginas_total = ceil(session.query(Favorito).count() / limite)

    return apresenta_favoritos(busca, paginas_total)


@app.delete('/favorito', tags=[favorito_tag],
            responses={"200": FavoritoViewSchema, "404": ErrorSchema})
def delete_favorito(query: FavoritoBuscaSchema):
    """Remove um favorito a partir do seu id

    Args:
        query (FavoritoBuscaSchema): O id do favorito.

    Raises:
        ValueError: Erro de favorito de tal id não existir.

    Returns:
        tuple: Mensagem de sucesso ou erro.
    """
    try:
        session = Session()
        favorito = session.query(Favorito).filter_by(
            id=query.id).delete()
        session.commit()

        if not favorito:
            raise ValueError

        return {}, 204
    except ValueError as e:
        error_msg = "Não foi possível encontrar o favorito."
        return {"mensagem": error_msg}, 404


@app.put('/favorito/curtir', tags=[favorito_tag],
         responses={"200": FavoritoViewSchema, "404": ErrorSchema})
def curtir_favorito(query: FavoritoBuscaSchema):
    """Dá uma curtida em um favorito a partir do seu id

    Args:
        query (FavoritoBuscaSchema): O id do favorito.

    Raises:
        ValueError: Erro de favorito de tal id não existir.

    Returns:
        tuple: Mensagem de sucesso ou erro.
    """
    try:
        session = Session()
        favorito = session.query(Favorito).get(query.id)
        favorito.curtidas = favorito.curtidas + 1
        session.commit()

        if not favorito:
            raise ValueError

        return apresenta_favorito(favorito)
    except ValueError as e:
        error_msg = "Não foi possível encontrar o favorito."
        return {"mensagem": error_msg}, 404
