from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from schemas import *
from flask_cors import CORS
from controller import *

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


@app.post('/cadastro', tags=[usuario_tag],
          responses={"201": UsuarioViewSchema, "403": ErrorSchema, "404": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo usuário na base identificado pelo id

    Retorna uma representação do usuário, no caso id, nome e o e-mail.
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
def get_usuario():
    """Busca um usuário a partir do seu token

    Retorna os dados do usuário.
    """
    return UsuarioControlador.obter_usuario()


@app.post('/favorito', tags=[favorito_tag],
          responses={"200": FavoritoViewSchema, "401": ErrorSchema, "404": ErrorSchema})
def post_favorito(form: FavoritoSchema):
    """Cadastra um favorito para o usuário logado

    Retorna o JSON com o favorito.
    """
    return FavoritoControlador.cadastrar_favorito(form)


@app.get('/favoritos', tags=[favorito_tag],
         responses={"200": ListagemFavoritoSchema})
def get_favoritos():
    """Retorna últimos favoritos adicionados

    Retorna o JSON com a lista de favoritos mais recentes.
    """
    return FavoritoControlador.obter_favoritos()


@app.get('/meus-favoritos', tags=[favorito_tag],
         responses={"200": ListagemFavoritoSchema, "401": ErrorSchema, "404": ErrorSchema})
def get_meus_favoritos():
    """Retorna favoritos adicionados pelo usuário

    Retorna o JSON com a lista dos favoritos cadastros pelo usuário.
    """
    return FavoritoControlador.obter_meus_favoritos()


@app.delete('/favorito', tags=[favorito_tag],
            responses={"200": FavoritoViewSchema, "401": ErrorSchema, "404": ErrorSchema})
def delete_favorito(query: FavoritoBuscaSchema):
    """Remove um favorito a partir do seu id

    Retorna o JSON de sucesso
    """
    return FavoritoControlador.remover_favorito(query)
