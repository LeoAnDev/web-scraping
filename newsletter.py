import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Lista de cidades para filtro
cidades = [
    "Itaperuna",
    "Bom Jesus do Itabapoana",
    "Italva",
    "Cardoso Moreira",
    "Laje do Muriaé",
    "Natividade",
    "Porciúncula",
    "Varre Sai",
    "São José de Ubá",
]

# Termos relacionados a polícia e crimes
termos_policia_crime = [
    "polícia militar",
    "polícia civil",
    "crime",
    "criminoso",
    "violência",
    "roubo",
    "assalto",
    "homicídio",
    "feminicídio",
    "sequestro",
    "drogas",
    "operação policial",
    "prisão",
    "suspeito",
    "investigação",
    "tráfico",
    "latrocínio",
    "corrupção",
    "fraude",
    "delito",
    "contravenção",
    "inquérito",
    "b.o.",
    "boletim de ocorrência",
    "denúncia",
    "penal",
    "criminal",
    "extorsão",
    "calúnia",
    "difamação",
    "injúria",
    "acidente",
    "tiroteio",
    "furtos",
    "flagrante",
    "fuga",
    "mandado de prisão",
    "procurado",
    "testemunha",
    "criminoso armado",
    "ação policial",
    "delegacia",
    "delegado",
    "escrivão",
    "agente",
    "força tática",
    "cope",
    "promotor",
    "juiz",
    "tribunal",
    "julgamento",
    "sentença",
    "pena",
    "prisão preventiva",
    "liberdade condicional",
    "crime hediondo",
    "captura",
    "investigador",
    "comissário",
    "diligência",
    "acareação",
    "tornozeleira eletrônica",
    "interrogatório",
    "confissão",
    "repressão",
    "mandado",
    "prisão domiciliar",
    "lockdown",
    "bloqueio",
    "reintegração de posse",
    "suspeita",
    "crime organizado",
    "Fraude eletrônica",
    "Hackers",
    "Cybercrime",
    "abuso de autoridade",
    "Delegacia especializada",
    "crime contra a vida",
    "lesão corporal",
    "ações penais",
    "direitos humanos",
    "vítima",
    "arma de fogo",
    "armamento",
    "colete balístico",
    "munição",
    "tiro",
    "tentativa de homicídio",
    "tentativa de roubo",
    "tentativa de furto",
    "crime de resistência",
    "obstrução",
    "fuga de local de crime",
    "depósito de drogas",
    "tráfico internacional",
    "milícia",
    "desaparecimento",
    "sequestro relâmpago",
    "perseguição policial",
    "abuso sexual",
    "pedofilia",
    "compra de votos",
    "coação",
    "descaminho",
    "contrabando",
    "explosivos",
    "perícia",
    "perito",
    "lavagem de dinheiro",
    "sonegação",
    "evasão",
    "delação",
    "fiança",
    "prisão em flagrante",
]

# URL inicial do site
base_url = "https://www.r7.com/"

# Cabeçalhos para emular um navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Conjunto para armazenar URLs visitadas e evitar loops
visited_urls = set()

# Conjunto para armazenar URLs dos artigos processados e evitar duplicações
visited_articles = set()

# Limite de profundidade para o crawling
max_depth = 4


def is_valid_url(url):
    # Verifica se a URL pertence ao domínio principal
    domain = urlparse(base_url).netloc
    return urlparse(url).netloc == domain


def scrape_page(url):
    try:
        # Faz uma requisição GET para a URL especificada com os cabeçalhos
        response = requests.get(url, headers=headers)
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()
        # Lê o conteúdo da resposta e armazena na variável 'html_content'
        return BeautifulSoup(response.text, "html5lib")
    except requests.RequestException as e:
        print("Erro ao acessar a URL:", url, e)
        return None


def artigo_relevante(titulo, conteudo):
    # Verifica se alguma das cidades está presente no título ou conteúdo
    if any(cidade in titulo or cidade in conteudo for cidade in cidades):
        # Verifica se algum dos termos relacionados a polícia e crimes está no título ou conteúdo
        if any(
            termo in titulo.lower() or termo in conteudo.lower()
            for termo in termos_policia_crime
        ):
            return True
    return False


def remove_unwanted_tags(soup, tags):
    for tag in tags:
        for item in soup.find_all(tag):
            item.decompose()


def process_article(url, bs):
    # Verifica se a URL do artigo já foi visitada
    if url in visited_articles:
        return

    # Remove conteúdo das tags indesejadas
    remove_unwanted_tags(bs, ["h1", "h5"])

    # Extrai o título da notícia
    titulo_tag = bs.find("h2", class_="entry-title")
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título não encontrado"

    # Extrai a data da notícia
    data_tag = bs.find("time", class_="entry-date published updated")
    data = data_tag.get_text(strip=True) if data_tag else "Data não encontrada"

    # Extrai o conteúdo da notícia
    conteudo_tag = bs.find("div", class_="entry-content")
    conteudo = (
        conteudo_tag.get_text(strip=True) if conteudo_tag else "Conteúdo não encontrado"
    )

    # Verifica se o artigo é relevante
    if artigo_relevante(titulo, conteudo):
        print("URL:", url)
        print("Título:", titulo)
        print("Data:", data)  # Data da publicação da notícia
        print("Conteúdo:", conteudo)
        print("=" * 80)

        # Marca o artigo como visitado
        visited_articles.add(url)


def crawl(url, depth):
    if depth > max_depth:
        return

    if url in visited_urls:
        return
    print(f"Visitando: {url} na profundidade {depth}")
    visited_urls.add(url)

    bs = scrape_page(url)
    if bs is None:
        return

    if depth == 0:
        # Busca todas as URLs de artigos na página principal
        article_links = bs.find_all("a", href=True)
        for link in article_links:
            article_url = urljoin(base_url, link["href"])
            if is_valid_url(article_url) and article_url not in visited_urls:
                article_bs = scrape_page(article_url)
                if article_bs:
                    process_article(article_url, article_bs)
                    time.sleep(1)  # Pausa de 1 segundo entre as requisições

    # Encontra e segue links para outras páginas do site (crawling)
    pagination_links = bs.find_all("a", href=True)
    for link in pagination_links:
        next_url = urljoin(base_url, link["href"])
        if is_valid_url(next_url) and next_url not in visited_urls:
            crawl(next_url, depth + 1)


# Inicia o crawling a partir da URL base
crawl(base_url, 0)
