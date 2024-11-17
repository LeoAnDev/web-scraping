# datacolector.py

# Importa a função 'urlopen' do módulo 'urllib.request'
from urllib.request import urlopen

# Importa a classe 'HTTPError' do módulo 'urllib.error' para tratamento de erro HTTP
from urllib.error import HTTPError

# Importa a classe 'URLError' do módulo 'urllib.error' para tratamento de erro de URL
from urllib.error import URLError

# Importa a classe BeautifulSoup do módulo 'bs4'
from bs4 import BeautifulSoup

try:
    # Abre a URL especificada e armazena a resposta na variável 'html'
    html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")

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

    # Encontra todas as tags <span> com a classe "green" e armazena na variável 'nameList'
    nameList = bs.findAll("span", {"class": "green"})

    # Itera sobre todos os elementos encontrados e imprime o texto contido em cada um
    for name in nameList:
        print(name.get_text())
