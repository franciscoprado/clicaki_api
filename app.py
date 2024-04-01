from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session
from logger import logger
from schemas import *
from flask_cors import CORS
from controller import *

info = Info(title="Minha API", version="1.0.0")
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


@app.post('/cadastro', tags=[usuario_tag],
          responses={"201": UsuarioViewSchema, "403": ErrorSchema, "404": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo usuário na base identificado pelo id

    Retorna uma representação do usuário, no caso id e o e-mail.
    """
    return UsuarioControlador.adicionar_usuario(form)


@app.post('/login', tags=[usuario_tag],
          responses={"200": UsuarioTokenSchema, "404": ErrorSchema})
def login(form: UsuarioLoginSchema):
    """Faz login de um usuário através de um e-mail e senha

    Retorna um token do tipo JWT
    """
    return UsuarioControlador.login(form)


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "401": ErrorSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):
    """Busca um usuário a partir do seu id

    Retorna os dados do usuário.
    """
    return UsuarioControlador.obter_usuario(query)


@app.post('/favorito', tags=[favorito_tag],
          responses={"200": FavoritoViewSchema, "401": ErrorSchema, "404": ErrorSchema})
def post_favorito(form: FavoritoSchema):
    """Busca um usuário a partir do seu id

    Retorna os dados do usuário.
    """
    return FavoritoControlador.cadastrar_favorito(form)


@app.get('/favoritos', tags=[favorito_tag],
         responses={"200": ListagemFavoritoSchema})
def get_favoritos():
    """Busca um usuário a partir do seu id

    Retorna os dados do usuário.
    """
    return FavoritoControlador.obter_favoritos()
