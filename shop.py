# shop.py

# Importa a função 'urlopen' do módulo 'urllib.request'
from urllib.request import urlopen

# Importa a classe 'HTTPError' do módulo 'urllib.error' para tratamento de erro HTTP
from urllib.error import HTTPError

# Importa a classe 'URLError' do módulo 'urllib.error' para tratamento de erro de URL
from urllib.error import URLError

# Importa a classe BeautifulSoup do módulo 'bs4'
from bs4 import BeautifulSoup

# Importa o módulo 're' para expressões regulares
import re

try:
    # Abre a URL especificada e armazena a resposta na variável 'html'
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")

    # Lê o conteúdo da resposta (de codificação UTF-8) e armazena na variável 'html_content'
    html_content = html.read().decode("utf-8")
except HTTPError as e:
    # Trata erros HTTP e imprime a mensagem de erro
    print(e)
except URLError as e:
    # Trata erros de URL (como servidor não encontrado) e imprime a mensagem de erro
    print(e)
else:
    # Converte o conteúdo HTML em um objeto BeautifulSoup usando o analisador de HTML integrado
    bs = BeautifulSoup(html_content, "html5lib")

    # Exemplo comentado de iteração sobre todos os filhos da tabela com id 'giftList'
    """
    for child in bs.find("table", {"id": "giftList"}).children:
        print(child)
    """

    # Exemplo comentado de iteração sobre todos os irmãos da primeira linha da tabela com id 'giftList'
    """
    for sibling in bs.find("table", {"id": "giftList"}).tr.next_siblings:
        print(sibling)
    """

    # Exemplo comentado de acesso ao conteúdo de um elemento
    """
    print(
        bs.find(
            "img", {"src": "../img/gifts/img4.jpg"}
        ).parent.previous_sibling.get_text()
    )
    """

    # Encontra todas as tags <img> cuja fonte coincide com a expressão regular e as armazena na variável 'images'
    images = bs.find_all("img", {"src": re.compile(r"\.\.\/img\/gifts/img.*\.jpg")})

    # Itera sobre todos os elementos encontrados e imprime o valor do atributo 'src' de cada um
    for image in images:
        print(image["src"])
