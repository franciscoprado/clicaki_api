from model.usuario import Usuario
from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    nome: str
    email: str
    senha: str


class UsuarioViewSchema(BaseModel):
    """ Define como um usuario será retornado, mostrando o email.
    """
    id: int = 1
    nome: str = "John Doe"
    email: str = "johndoe@example.com"
    
    
class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de um usuário, com base no seu id.
    """
    id: int = 1


class UsuarioTokenSchema(BaseModel):
    """ Define como será retornado o token após o login.
    """
    token: str


def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
    }
