import datetime
import random
import lorem
from model import Session, Favorito

total_itens = 12
urls = ['google.com', 'youtube.com', 'facebook.com', 'twitter.com',
        'wikipedia.org', 'instagram.com', 'reddit.com', 'amazon.com', 'duckduckgo.com', 'yahoo.com']

if __name__ == "__main__":
    print("Iniciando o seeding...")
    session = Session()

    for numero in range(total_itens):
        data_insercao = datetime.datetime.now() - datetime.timedelta(days=numero)
        url = urls[random.randint(0, len(urls)) - 1]
        favorito = Favorito(
            url=f'https://www.{url}',
            titulo=lorem.sentence(),
            descricao=lorem.sentence(),
            curtidas=random.randint(0, 20),
            data_insercao=data_insercao)
        session.add(favorito)

    session.commit()
    print("Seeding concluído")
