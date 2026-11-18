#!/usr/bin/env python3
"""Gera o catálogo da Aline Goes (Dona Miau).

Uso: python3 gerar.py
Lê as capas em dados/capas/ (baixadas do Instagram dela) e as fotos em img/
(páginas de compra da Kiwify) e escreve o site pronto em docs/ (index.html,
fotos/, looks/ e fonts/), que é a pasta publicada no GitHub Pages.
Todo texto de peça vem das legendas públicas dela. Nada aqui é inventado.
"""
import html, json, os, shutil, subprocess, urllib.parse

RAIZ = os.path.dirname(os.path.abspath(__file__))
ZAP = "https://wa.me/5582981637859"
YT = "https://www.youtube.com/@Donamiiau"
IG = "https://www.instagram.com/donamiiau/"

TIPOS = {
    "aula": ("Aula completa", "Aulas completas", "Aulas pagas, com acesso pela Kiwify."),
    "gratis": ("Aula gratuita", "Aulas gratuitas", "Aulas inteiras no YouTube, sem custo."),
    "tutorial": ("Tutorial", "Tutoriais", "Passo a passo curto, em vídeo no Instagram."),
    "encomenda": ("Sob encomenda", "Sob encomenda", "Peças prontas, feitas pela Aline sob medida."),
}
FAMILIAS = {"bolsa": "Bolsas", "acessorio": "Acessórios", "vestuario": "Vestuário"}


def kiwify(cod):
    return "https://pay.kiwify.com.br/" + cod


def post(cod):
    return "https://www.instagram.com/p/" + cod + "/"


def busca_fischer(nome):
    q = urllib.parse.quote_plus("Fischer Fios " + nome + " Aline Goes")
    return "https://www.youtube.com/results?search_query=" + q


def zap(nome):
    return ZAP + "?text=" + urllib.parse.quote("Olá, Aline! Quero encomendar: " + nome)


# (id, nome, tipo, família, foto de origem, código do post ou None, descrição, materiais, extra)
PECAS = [
    # ---- Aulas completas (Kiwify)
    ("renda-do-mar", "Bolsa Renda do Mar", "aula", "bolsa", "img/renda-do-mar.jpg", "DMyhUsAJ64d",
     "O design que chamou atenção na Mega Artesanal. Feita com fio Poli da Fischer Fios.", [], "lbtPq6Y"),
    ("renda", "Bolsa Renda", "aula", "bolsa", "img/renda.jpg", "DcHHAK0FsFn",
     "Clássica, versátil e 100% autoral. Aula completa, com acesso vitalício, para aprender no seu ritmo.", [], "K7ZrxZI"),
    ("miauzinha", "Bolsa Miauzinha", "aula", "bolsa", "img/miauzinha.jpg", "DKXxgippxDZ",
     "A bolsa das gatas. A aula traz PDF com gráfico e receita, dicas de fios e a explicação para duas bases diferentes.", [], "sLcFo8O"),
    ("anastacia-bag", "Anastácia Bag", "aula", "bolsa", "dados/capas/DRaEfa2ic9v.jpg", "DRaEfa2ic9v",
     "Duas versões de trama para escolher o seu estilo, fechamento invisível de carreira e uso de diferentes tipos de fio.", [], "RqMRiBT"),
    ("carteira-lorena", "Carteira Lorena", "aula", "bolsa", "img/lorena.jpg", "DPcGCdJiQ9r",
     "Pontos diferenciados e troca de cores que fazem a diferença. Acessório da Couramor.", [], "KbKF6MK"),
    ("maresia", "Bolsa Maresia", "aula", "bolsa", "img/maresia.jpg", None, "", [], "BEK52jO"),
    # ---- Aulas gratuitas no canal da Aline
    ("sandalia-duna", "Sandália Duna", "gratis", "acessorio", "dados/capas/DVElvj3AYbH.jpg", "DWMuiXHgUV1",
     "A sandália que viralizou ganhou aula completa e gratuita no canal da Aline. Feita com fio Opaque.",
     ["Sandália da sua escolha", "Fio Opaque", "Agulha 2,5 mm", "Agulha de tapeceiro", "Tesoura, isqueiro e marcadores"], "canal"),
    ("mini-lorena", "Carteira Mini Lorena", "gratis", "bolsa", "dados/capas/DPKQYeEgfbH.jpg", "DPKQYeEgfbH",
     "Uma carteira de mão em crochê, com passo a passo em aula gratuita no canal da Aline.", [], "canal"),
    ("bolsa-luize", "Bolsa Luize", "gratis", "bolsa", "dados/capas/DKxdy-2JxO6.jpg", "DKxdy-2JxO6",
     "Aula completa no canal da Aline. O acessório da bolsa é da Couramor.", [], "canal"),
    ("bolsa-karen", "Bolsa Karen", "gratis", "bolsa", "dados/capas/DIZkYPZJbjy.jpg", "DIZkYPZJbjy",
     "Trama em duas cores, fecho boca de lobo com ímã, fundo quadrado e alça dupla. Aula gratuita no canal da Aline.", [], "canal"),
    ("colar-agata", "Colar Ágata", "gratis", "acessorio", "dados/capas/DIwpsG-pALe.jpg", "DIwpsG-pALe",
     "Colar feito com vários fios, que traz textura e leveza. Aula detalhada no canal da Aline.", [], "canal"),
    # ---- Aulas gratuitas no canal da Fischer Fios
    ("blusa-perola", "Blusa Pérola", "gratis", "vestuario", "dados/capas/DeE5GesT33X.jpg", "DeE5GesT33X",
     "A versão da Aline para uma tendência em alta, feita com fio de algodão agulhado. Aula gratuita no canal da Fischer Fios.", [], "fischer"),
    ("blusa-mega", "Blusa Mega", "gratis", "vestuario", "dados/capas/DdPXQgDTpqY.jpg", "DdPXQgDTpqY",
     "A blusa que fez sucesso na Mega Artesanal. A aula mostra a construção da peça e dicas de modelagem sob medida.", [], "fischer"),
    ("blusa-siena", "Blusa Siena", "gratis", "vestuario", "dados/capas/DXm3a1Yk7e0.jpg", "DXm3a1Yk7e0",
     "Design moderno e fácil de fazer, com o fio Opaque. Aula gratuita no canal da Fischer Fios.", [], "fischer"),
    ("blusa-onda", "Blusa Onda", "gratis", "vestuario", "dados/capas/DSQUmI8AQAu.jpg", "DSQUmI8AQAu",
     "Aula com dicas de modelagem e de como adaptar a blusa para vários tamanhos.", [], "fischer"),
    ("bolsa-valentina", "Bolsa Valentina", "gratis", "bolsa", "dados/capas/DNQy1pCuF8h.jpg", "DNQy1pCuF8h",
     "Clássica e versátil, em bege, caramelo e preto. Feita com o fio Lume, com alça, base e fecho da Couramor.", [], "fischer"),
    ("bolsa-marina", "Bolsa Marina", "gratis", "bolsa", "dados/capas/DJPueI0JyUH.jpg", "DJZd7fBuOp_",
     "Feita em triângulos com a técnica de fio conduzido, em três cores. A aula tem gráfico para facilitar.", [], "fischer"),
    ("bolsa-leticia", "Bolsa Letícia", "gratis", "bolsa", "dados/capas/DIOx2SuJijF.jpg", "DIOx2SuJijF",
     "Feita com o fio Poli em duas cores, com o kit de acessórios da Couramor: fundo, fecho em zíper, forro e alça.", [], "fischer"),
    # ---- Tutoriais no Instagram
    ("bolsa-giselle", "Bolsa Giselle", "tutorial", "bolsa", "dados/capas/DS0fBTMAagQ.jpg", "DS0fBTMAagQ",
     "Bolsa grande, com trama simples e resultado diferente. Fio de poliéster na cor gergelim e kit de acessórios com base quadrada, alças de ombro e zíper.", [], None),
    ("mochila-zaya", "Mochila e Bolsa Zaya", "tutorial", "bolsa", "dados/capas/De5A7RdBYoU.jpg", "De5A7RdBYoU",
     "Uma peça, duas formas de usar: a mochila vira bolsa tiracolo com o kit Zaya, da Couramor.",
     ["Agulha 5 mm", "Fio de poliéster de 5 mm (ou fio de malha)", "Marcadores de pontos", "Agulha e linha de costura", "Isqueiro para acabamento"], None),
    ("bolsa-brasileirinha", "Bolsa Brasileirinha", "tutorial", "bolsa", "dados/capas/DXVDgUnkz43.jpg", "DXVDgUnkz43",
     "Feita com o fio Policromia na cor Brasilidade. Pode ser usada dos dois lados.",
     ["Agulha 6 mm", "Tesoura", "Isqueiro para arremate", "Marcadores de ponto", "Fecho de ímã"], None),
    ("mini-bag-miau", "Mini Bag Miau", "tutorial", "bolsa", "dados/capas/DLfrywOJnZp.jpg", "DLfrywOJnZp",
     "Uma minibag delicada, para dar um toque especial à bolsa maior.",
     ["Fio de malha de 15 mm", "Agulha 4 mm", "Cola para acabamento", "Miçangas"], None),
    ("multi-pouch", "Multi Pouch", "tutorial", "bolsa", "dados/capas/DfS48BQzm0l.jpg", "DfS48BQzm0l",
     "Bolsinha para organizar: serve de porta-lápis, porta-óculos e mais.",
     ["Fio de crochê da sua preferência", "Agulha 3 mm", "Agulha 2,5 mm para costura", "Tesoura e cola para arremate", "Marcadores", "1 botão"], None),
    ("porta-celular-classic", "Porta-celular Classic", "tutorial", "bolsa", "dados/capas/DVovzH7gV2n.jpg", "DVovzH7gV2n",
     "Feito com o fio Plissé, de 10 mm e dupla face. Pontos que você já conhece, com um efeito bonito na trama.", [], None),
    ("porta-celular-duo", "Porta-celular Duo", "tutorial", "bolsa", "dados/capas/DUyw8KRge3x.jpg", "DUyw8KRge3x",
     "Celular na frente, garrafinha atrás. O acessório é da Couramor.", [], None),
    ("cinto-siena", "Cinto Siena", "tutorial", "acessorio", "dados/capas/Ddy3EcqThlT.jpg", "Ddy3EcqThlT",
     "Trama delicada com o fio Fhyno, de 2 mm, e fivela dourada. No fim do vídeo há um card com materiais, trama e sequência dos pontos.", [], None),
    ("colar-essencial", "Colar Essencial", "tutorial", "acessorio", "dados/capas/Dc4CWWZzeg_.jpg", "Dc4CWWZzeg_",
     "Um colar delicado e versátil, com acessórios Altero e fio Fischer.", [], None),
    ("colar-nautico", "Colar Náutico", "tutorial", "acessorio", "dados/capas/DTbK-f2geub.jpg", "DTbK-f2geub",
     "Fácil e rápido de fazer. Leva entremeio, pingente e dois finalizadores.",
     ["Fio Jardim, da Meliah", "Agulha 5 mm", "Tesoura", "Fita métrica"], None),
    ("colar-brasil-core", "Colar Brasil Core", "tutorial", "acessorio", "dados/capas/DWCoZzpAQc1.jpg", "DWCoZzpAQc1",
     "Em duas versões: de uma cor só ou com o toque de amarelo. Feito com fio de malha de 25 mm.", [], None),
    ("pulseira-berloques", "Pulseira de berloques", "tutorial", "acessorio", "dados/capas/DUOh6HuAcBQ.jpg", "DUOh6HuAcBQ",
     "Simples e rápida de fazer, boa para usar, vender ou presentear.",
     ["Fio Perla, cor pérola", "Berloques, pingentes e passadores", "Fecho de ímã quadrado de 20 mm"], None),
    ("xuxinha", "Xuxinha de crochê", "tutorial", "acessorio", "dados/capas/DWe5sLgAQrb.jpg", "DWe5sLgAQrb",
     "Fácil de fazer e muito vendável. Nesta versão, com o fio Flora.", [], None),
    ("faixa-duas-cores", "Faixa de duas cores", "tutorial", "acessorio", "dados/capas/DWwmGruE5hV.jpg", "DWwmGruE5hV",
     "Duas tiras entrelaçadas. A sequência é 4 pontos altos, 1 diminuição de 3 pontos, 4 pontos altos e 1 aumento de 3 pontos.",
     ["Fio Opaque em duas cores", "Agulha 3 mm", "Cerca de 12 cm de elástico", "Agulha e linha de costura", "Tesoura e isqueiro"], None),
    ("laco-charme", "Laço Charme", "tutorial", "acessorio", "dados/capas/DK74QuIpBmF.jpg", "DK74QuIpBmF",
     "Laço de cabelo em duas cores. A sequência de pontos está na legenda do vídeo.",
     ["Fio Opaque, bege e preto", "Agulha 4 mm", "Tesoura", "Isqueiro para o acabamento"], None),
    ("luva-outono", "Luva de Outono", "tutorial", "acessorio", "dados/capas/DLGJrkMJnva.jpg", "DLGJrkMJnva",
     "Aquece as mãos sem impedir os movimentos. O passo a passo completo está na legenda do vídeo.",
     ["Fio Opaque, cor bege", "Agulha 3 mm", "Marcadores", "Tesoura e isqueiro", "Fita métrica"], None),
    ("bata-soul", "Bata Soul", "tutorial", "vestuario", "dados/capas/DUgaZZPgTSc.jpg", "DUgaZZPgTSc",
     "Simples de fazer. Comece com 33 correntinhas no P, 43 no M, 53 no G e 63 no GG. O tamanho M leva cerca de um rolo e meio de fio.",
     ["Fio Soul, da Meliah", "Agulha 3,5 mm", "Agulha de tapeceiro", "Marcadores", "Tesoura"], None),
    ("blusa-glamour", "Blusa Glamour", "tutorial", "vestuario", "dados/capas/DS752PrkRNp.jpg", "DS752PrkRNp",
     "Para quem gosta de brilho. Feita com o cordão Glimmer, da Fischer Fios.", [], None),
    # ---- Sob encomenda
    ("enc-blusa-perola", "Blusa Pérola", "encomenda", "vestuario", "dados/capas/DeP9jNrFkFP.jpg", "DeP9jNrFkFP",
     "Feita com o fio Origem, de algodão. Peça feita sob encomenda.", [], None),
    ("enc-zaya", "Mochila Zaya", "encomenda", "bolsa", "dados/capas/DfAsHzPgVJC.jpg", "DfAsHzPgVJC",
     "Nos tamanhos P e M. Com alças ajustáveis, a mochila vira bolsa.", [], None),
    ("enc-vestido-jade", "Vestido Jade", "encomenda", "vestuario", "dados/capas/DT3s7MJgR1O.jpg", "DT3s7MJgR1O",
     "Vestido de crochê feito sob medida.", [], None),
    ("enc-blusa-aline", "Blusa modelo Aline", "encomenda", "vestuario", "dados/capas/DQW7c0kkXtF.jpg", "DQW7c0kkXtF",
     "Feita sob medida, com mescla de fios de algodão. Entrega para todo o Brasil.", [], None),
    ("enc-blusa-bata", "Blusa modelo Bata", "encomenda", "vestuario", "dados/capas/DPuZMkUgV5w.jpg", "DPuZMkUgV5w",
     "Blusa de crochê feita sob medida.", [], None),
    ("enc-serena", "Conjunto Serena Gold", "encomenda", "vestuario", "dados/capas/DSI0bzsgYA0.jpg", "DSI0bzsgYA0",
     "Conjunto com brilho na medida certa, feito sob encomenda.", [], None),
]


def e(t):
    return html.escape(t, quote=True)


SAIDA = os.path.join(RAIZ, "docs")

# As seis aulas pagas abrem a página como "looks" em tela cheia.
# (id, foto de origem, recorte do ffmpeg ou None, composição, nome em linhas)
LOOKS = [
    ("renda-do-mar", "img/renda-do-mar.jpg", None, "esq", ["Renda", "do Mar"]),
    ("renda", "img/renda.jpg", "crop=900:1010:0:590", "dir", ["Bolsa", "Renda"]),
    ("miauzinha", "img/miauzinha.jpg", None, "esq", ["Miauzinha"]),
    ("maresia", "img/maresia.jpg", None, "larga", ["Maresia"]),
    ("carteira-lorena", "img/lorena.jpg", None, "dir", ["Carteira", "Lorena"]),
    ("anastacia-bag", "dados/capas/DRaEfa2ic9v.jpg", "crop=iw:ih*0.47:0:0", "larga", ["Anastácia", "Bag"]),
]


def ffmpeg(origem, destino, filtro):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(RAIZ, origem),
                    "-vf", filtro, "-q:v", "3", destino], check=True)


def prepara_foto(origem, pid):
    ffmpeg(origem, os.path.join(SAIDA, "fotos", pid + ".jpg"), "scale='min(800,iw)':-2")
    return "fotos/" + pid + ".jpg"


def acoes(nome, tipo, cod, extra):
    """Lista de (rótulo, endereço, principal?)."""
    a = []
    if tipo == "aula":
        a.append(("Comprar a aula", kiwify(extra), True))
    elif tipo == "gratis" and extra == "canal":
        a.append(("Abrir o canal no YouTube", YT, True))
    elif tipo == "gratis":
        a.append(("Procurar a aula no YouTube", busca_fischer(nome), True))
    elif tipo == "encomenda":
        a.append(("Encomendar no WhatsApp", zap(nome), True))
    if cod:
        a.append(("Assistir no Instagram" if tipo == "tutorial" else "Ver no Instagram", post(cod), tipo == "tutorial"))
    return a


def onde(tipo, extra):
    if tipo == "aula":
        return "O valor e as formas de pagamento aparecem na página de compra, na Kiwify."
    if tipo == "gratis" and extra == "canal":
        return "A aula fica no canal da Aline no YouTube."
    if tipo == "gratis":
        return "A aula fica no canal da Fischer Fios no YouTube. O botão abre uma busca pelo nome da peça."
    if tipo == "tutorial":
        return "O passo a passo está no vídeo, no Instagram da Aline."
    return "Peça feita pela Aline sob encomenda. Combine medida, cor e prazo direto com ela."


def monta():
    fichas, cards, conta = {}, [], {t: 0 for t in TIPOS}
    for pid, nome, tipo, fam, origem, cod, desc, mat, extra in PECAS:
        foto = prepara_foto(origem, pid)
        ac = acoes(nome, tipo, cod, extra)
        conta[tipo] += 1
        fichas[pid] = {"nome": nome, "tipo": TIPOS[tipo][0], "familia": FAMILIAS[fam], "foto": foto,
                       "desc": desc, "mat": mat, "onde": onde(tipo, extra),
                       "acoes": [{"r": r, "u": u, "p": p} for r, u, p in ac]}
        busca = " ".join([nome, TIPOS[tipo][0], FAMILIAS[fam], desc]).lower()
        cards.append(
            f'<li class="peca" data-id="{pid}" data-tipo="{tipo}" data-familia="{fam}" data-busca="{e(busca)}">'
            f'<a href="{e(ac[0][1])}" target="_blank" rel="noopener" data-ficha="{pid}">'
            f'<span class="quadro"><img src="{foto}" alt="" loading="lazy" width="800" height="1000"></span>'
            f'<span class="nome">{e(nome)}</span>'
            f'<span class="dado">{e(TIPOS[tipo][0])}</span></a></li>')
    looks = []
    for i, (pid, origem, recorte, comp, linhas) in enumerate(LOOKS):
        filtro = (recorte + "," if recorte else "") + "scale='min(1500,iw)':-2"
        ffmpeg(origem, os.path.join(SAIDA, "looks", pid + ".jpg"), filtro)
        f = fichas[pid]
        compra = f["acoes"][0]["u"]
        desc = f'<p class="look-desc">{e(f["desc"])}</p>' if f["desc"] else ""
        carga = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
        looks.append(
            f'<section class="look look-{comp}" aria-label="{e(f["nome"])}">'
            f'<div class="look-foto"><img src="looks/{pid}.jpg" alt="{e(f["nome"])}, peça de crochê de Aline Goes" {carga}></div>'
            f'<div class="look-texto">'
            f'<h2 class="look-nome">{"<br>".join(e(l) for l in linhas)}</h2>'
            f'<p class="look-dado">Aula completa</p>{desc}'
            f'<p class="look-links"><a class="ir" href="{e(compra)}" target="_blank" rel="noopener">Comprar a aula</a>'
            f'<a class="ir leve" href="#indice" data-ficha="{pid}">Ver detalhes</a></p></div></section>')
    filtros_tipo = '<button type="button" class="palavra" data-tipo="" aria-pressed="true">Tudo<sup>' + str(len(PECAS)) + '</sup></button>' + "".join(
        f'<button type="button" class="palavra" data-tipo="{t}" aria-pressed="false">{e(TIPOS[t][1])}<sup>{conta[t]}</sup></button>'
        for t in TIPOS)
    filtros_fam = "".join(
        f'<button type="button" class="palavra menor" data-familia="{f}" aria-pressed="false">{e(n)}</button>'
        for f, n in FAMILIAS.items())
    return fichas, "".join(looks), "".join(cards), filtros_tipo, filtros_fam


def destaques(fichas):
    """As seis aulas pagas como receitas em destaque, para o modelo de revista."""
    out = []
    for i, (pid, _o, _r, _c, _l) in enumerate(LOOKS):
        f = fichas[pid]
        desc = f'<p class="r-desc">{e(f["desc"])}</p>' if f["desc"] else ""
        out.append(
            f'<article class="receita {"r-g" if i % 3 == 0 else "r-p"}">'
            f'<a class="r-foto" href="{e(f["acoes"][0]["u"])}" target="_blank" rel="noopener" data-ficha="{pid}">'
            f'<img src="looks/{pid}.jpg" alt="{e(f["nome"])}" loading="lazy"></a>'
            f'<div class="r-texto"><h3>{e(f["nome"])}</h3>{desc}'
            f'<dl class="r-ficha"><div><dt>Tipo</dt><dd>Aula completa</dd></div>'
            f'<div><dt>Categoria</dt><dd>{e(f["familia"])}</dd></div>'
            f'<div><dt>Onde</dt><dd>Kiwify</dd></div></dl>'
            f'<p class="r-acoes"><a class="botao" href="{e(f["acoes"][0]["u"])}" target="_blank" rel="noopener">Comprar a aula</a>'
            f'<a class="elo" href="#sumario" data-ficha="{pid}">Ver a receita</a></p></div></article>')
    return "".join(out)


def grava(modelo_nome, pasta, prefixo, partes):
    modelo = open(os.path.join(RAIZ, modelo_nome), encoding="utf-8").read()
    pagina = modelo
    for chave, valor in partes.items():
        pagina = pagina.replace("{{" + chave + "}}", valor)
    assert "{{" not in pagina, "sobrou marcador em " + modelo_nome
    if prefixo:
        for d in ("fotos/", "looks/", "fonts/"):
            pagina = pagina.replace('"' + d, '"' + prefixo + d).replace("(\"" + d, "(\"" + prefixo + d)
    destino = os.path.join(SAIDA, pasta)
    os.makedirs(destino, exist_ok=True)
    open(os.path.join(destino, "index.html"), "w", encoding="utf-8").write(pagina)


def main():
    fichas, looks, cards, f_tipo, f_fam = monta()
    conta = {t: sum(1 for p in PECAS if p[2] == t) for t in TIPOS}
    partes = {"LOOKS": looks, "PECAS": cards, "FILTROS_TIPO": f_tipo, "FILTROS_FAM": f_fam,
              "TOTAL": str(len(PECAS)), "DESTAQUES": destaques(fichas),
              "N_AULA": str(conta["aula"]), "N_GRATIS": str(conta["gratis"]),
              "N_TUTORIAL": str(conta["tutorial"]), "N_ENCOMENDA": str(conta["encomenda"]),
              "FICHAS": json.dumps(fichas, ensure_ascii=False).replace("</", "<\\/")}
    os.makedirs(os.path.join(SAIDA, "fonts"), exist_ok=True)
    for f in os.listdir(os.path.join(RAIZ, "fonts")):
        if f != "Outfit-normal.woff2":
            shutil.copy(os.path.join(RAIZ, "fonts", f), os.path.join(SAIDA, "fonts", f))
    grava("modelo-lookbook.html", "", "", partes)
    grava("modelo-revista.html", "revista", "../", partes)
    open(os.path.join(SAIDA, ".nojekyll"), "w").write("")
    print(len(PECAS), "peças;", conta)


if __name__ == "__main__":
    main()
