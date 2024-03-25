import re
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, make_response
from urllib.parse import unquote
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Comentario, Usuario
from logger import logger
from schemas import *
from flask_cors import CORS
from utils import *

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(
    name="Produto", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(
    name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")
usuario_tag = Tag(name="Usuario", description="Adição de um usuário à base")

# regex para validação de e-mail
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(
        Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"message": "Produto removido", "id": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = form.produto_id
    logger.debug(f"Adicionando comentários ao produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(
            f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao produto
    produto.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{produto_id}")

    # retorna a representação de produto
    return apresenta_produto(produto), 200


@app.post('/cadastro', tags=[usuario_tag],
          responses={"201": UsuarioViewSchema, "403": ErrorSchema, "404": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo usuário na base identificado pelo id

    Retorna uma representação do usuário, no caso id e o e-mail.
    """
    if not EMAIL_REGEX.match(form.email) or not form.nome or not form.senha:
        error_msg = "Dados inválidos"
        return {"message": error_msg}, 403

    usuario = Usuario(
        nome=form.nome,
        email=form.email,
        senha=generate_password_hash(form.senha))

    try:
        session = Session()
        session.add(usuario)
        session.commit()
        logger.debug(f"Adicionado usuário de e-mail: '{usuario.email}'")
        return apresenta_usuario(usuario), 201

    except IntegrityError as e:
        error_msg = "Usuário com o mesmo e-mail já existente."
        logger.warning(
            f"Erro ao adicionar usuário '{usuario.email}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível adicionar o usuário."
        logger.warning(
            f"Erro ao adicionar usuário '{usuario.email}', {error_msg}")
        return {"message": error_msg}, 400


@app.post('/login', tags=[usuario_tag],
          responses={"200": UsuarioTokenSchema, "404": ErrorSchema})
def login(form: UsuarioSchema):
    """Faz login de um usuário na base através de um e-mail e senha

    Retorna um token do tipo JWT
    """
    email = form.email
    senha = form.senha
    logger.debug(f"Coletando dados sobre usuário de e-mail #{email}")
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        error_msg = "E-mail não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar usuário de e-mail '{email}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        if not check_password_hash(usuario.senha, senha):
            error_msg = "Senha inválida."
            logger.error(error_msg)
            return {"message": error_msg}, 409

        logger.debug(f"Usuário econtrado: '{usuario.email}'")
        token = gerar_token(usuario.nome, usuario.email)
        resp = make_response({"token": token}, 200)
        return resp


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "401": ErrorSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):
    """Busca um usuário a partir do seu id.

    Retorna os dados do usuário.
    """
    usuario_id = query.id
    logger.debug(f"Obtendo usuário de id #{usuario_id}")

    try:
        token = request.headers['Token']
        validar_token(token)
    except:
        error_msg = "Usuário não autorizado."
        logger.warning(
            f"Usuário não autorizado #'{usuario_id}'")
        return {"message": error_msg}, 401

    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    session.commit()

    if usuario:
        logger.debug(f"Buscando usuário #{usuario_id}")
        return apresenta_usuario(usuario), 200
    else:
        logger.warning(
            f"Erro ao buscar usuário de id #'{usuario_id}")
        return {"message": error_msg}, 404
