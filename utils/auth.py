from datetime import datetime, timedelta, timezone
from model.usuario import Usuario
import jwt

ALGORITHM = "HS256"
PRIVATE_KEY = "hv5!7Fo*k55aX21myW$th37$d90Ugg3@lb"


def gerar_token(usuario: Usuario):
    """ Retorna um token, do tipo JSON Web Token, contendo dados do login.

    Args:
        nome (str): O nome.
        email (str): O e-mail.

    Returns:
        str: O token.
    """
    data_atual = datetime.now(tz=timezone.utc)
    exp = data_atual + timedelta(days=30)
    encoded_jwt = jwt.encode(
        {"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "exp": exp}, PRIVATE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def validar_token(token: str):
    """ Verifica a validade de token e retorna o payload.

    Args:
        token (str): O token.

    Raises:
        Exception: jwt.ExpiredSignatureError

    Returns:
        dict: O payload.
    """
    try:
        payload = jwt.decode(token, PRIVATE_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
