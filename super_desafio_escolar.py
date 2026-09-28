# -*- coding: utf-8 -*-
"""
SUPER DESAFIO ESCOLAR  |  Educação Física, Geografia, Matemática, História e Português
Jogo educativo feito com Python + Pygame.

Como rodar:
    pip install pygame
    python super_desafio_escolar.py

Como jogar:
    Uma pergunta aparece no alto e 4 bolhas com respostas descem.
    Mova seu personagem (mouse OU setas / A e D) e PEGUE A BOLHA CERTA!
    Também dá para clicar direto na bolha. ESC encerra a partida.

Pontuação:
    acerto = +10 pontos (+2 de bônus por acerto seguido, até +10)
    erro (bolha errada ou deixar a certa passar) = -5 pontos e perde 1 vida
    a cada 5 acertos seguidos = 1 vida extra
    Sem limite de perguntas: o jogo só termina quando as vidas acabam!
    A cada 4 acertos o NÍVEL sobe e as bolhas descem mais rápido.
"""
import pygame
import random
import sys
import math
import colorsys

# ======================= CONFIGURAÇÕES (edite aqui) =======================
JOGO = "Super Desafio Escolar"
EQUIPE = ["Aline Lima", "Aline Conceição", "Maria Eduarda Alves"]   # <- nomes da equipe
VIDAS_INICIAIS = 3
VIDAS_MAX = 5
FEEDBACK_MS = 1200
LARGURA, ALTURA = 960, 620

# ============================ BANCOS DE PERGUNTAS ============================
# ---------- EDUCAÇÃO FÍSICA ----------
# (pergunta, [alternativas], índice da correta)
BANCO_EDF = [
    ("Quantos jogadores formam uma equipe de futebol em campo?", ["9", "10", "11", "12"], 2),
    ("Em qual esporte se pontua com uma cesta?", ["Vôlei", "Basquete", "Futebol", "Tênis"], 1),
    ("Quanto tempo dura uma partida oficial de futebol (tempo normal)?", ["80 minutos", "90 minutos", "100 minutos", "120 minutos"], 1),
    ("Quantos jogadores de uma equipe de vôlei ficam em quadra?", ["5", "6", "7", "8"], 1),
    ("Em que país foram realizados os Jogos Olímpicos de 2016?", ["China", "Reino Unido", "Brasil", "Japão"], 2),
    ("Como é chamado o golpe de ataque mais forte do vôlei?", ["Toque", "Saque", "Cortada", "Manchete"], 2),
    ("Quantos anéis tem a bandeira olímpica?", ["4", "5", "6", "7"], 1),
    ("Qual é a distância oficial de uma maratona?", ["21 km", "30 km", "42 km", "50 km"], 2),
    ("Em qual esporte se usa o termo nocaute?", ["Judô", "Boxe", "Natação", "Tênis"], 1),
    ("Qual seleção é a maior campeã de Copas do Mundo masculinas?", ["Alemanha", "Argentina", "Brasil", "Itália"], 2),
    ("Quantos toques cada equipe pode dar na bola antes de devolvê-la no vôlei?", ["2", "3", "4", "5"], 1),
    ("Quantos jogadores tem uma equipe de handebol em quadra?", ["5", "6", "7", "8"], 2),
    ("Qual é a principal fonte de energia do corpo durante o exercício?", ["Carboidratos", "Vitaminas", "Sais minerais", "Água"], 0),
    ("Quantos minutos de atividade física por semana a OMS recomenda para adultos?", ["30", "60", "150", "500"], 2),
    ("Qual é a unidade que mede os batimentos do coração?", ["kg", "bpm", "km/h", "cal"], 1),
    ("Para que serve o aquecimento antes do exercício?", ["Preparar o corpo e evitar lesões", "Cansar o corpo", "Ganhar peso", "Dormir melhor"], 0),
    ("Qual esporte é jogado com raquetes e uma peteca (volante) sobre uma rede?", ["Badminton", "Squash", "Vôlei", "Golfe"], 0),
    ("Em qual modalidade o atleta salta uma barra com ajuda de uma vara?", ["Salto em altura", "Salto com vara", "Salto triplo", "Arremesso de peso"], 1),
    ("Qual esporte tem as posições de goleiro, zagueiro, meia e atacante?", ["Futebol", "Basquete", "Natação", "Judô"], 0),
    ("Quantos pontos vale uma cesta de fora do arco de três pontos no basquete?", ["1", "2", "3", "4"], 2),
    ("Qual arte marcial japonesa tem o kimono e as faixas coloridas como marca?", ["Capoeira", "Judô", "Boxe", "Esgrima"], 1),
    ("O que é a capoeira?", ["Luta, dança e jogo criados no Brasil", "Um esporte de raquete", "Um tipo de corrida", "Um jogo de tabuleiro"], 0),
    ("Qual destes é um esporte aquático?", ["Polo aquático", "Hóquei", "Rúgbi", "Beisebol"], 0),
    ("Em qual esporte se usa o termo ace (saque que o adversário não toca)?", ["Tênis", "Futebol", "Natação", "Ciclismo"], 0),
    ("Beber água durante o exercício ajuda a:", ["Hidratar e regular a temperatura do corpo", "Diminuir a força", "Evitar o suor completamente", "Nada, é desnecessário"], 0),
    ("Quantos jogadores tem um time de basquete em quadra?", ["4", "5", "6", "7"], 1),
]

_fila_edf = []


def perg_edf(nivel=0):
    """Sorteia perguntas sem parar: quando o banco acaba, ele é embaralhado de novo."""
    global _fila_edf
    if not _fila_edf:
        _fila_edf = BANCO_EDF[:]
        random.shuffle(_fila_edf)
    enunciado, alts, c = _fila_edf.pop()
    certa = alts[c]
    alts = alts[:]
    random.shuffle(alts)
    return enunciado, alts, alts.index(certa)

# ---------- GEOGRAFIA ----------
ESTADOS_GEO = {
    "Acre": "Rio Branco", "Alagoas": "Maceió", "Amapá": "Macapá", "Amazonas": "Manaus",
    "Bahia": "Salvador", "Ceará": "Fortaleza", "Distrito Federal": "Brasília",
    "Espírito Santo": "Vitória", "Goiás": "Goiânia", "Maranhão": "São Luís",
    "Mato Grosso": "Cuiabá", "Mato Grosso do Sul": "Campo Grande", "Minas Gerais": "Belo Horizonte",
    "Pará": "Belém", "Paraíba": "João Pessoa", "Paraná": "Curitiba", "Pernambuco": "Recife",
    "Piauí": "Teresina", "Rio de Janeiro": "Rio de Janeiro", "Rio Grande do Norte": "Natal",
    "Rio Grande do Sul": "Porto Alegre", "Rondônia": "Porto Velho", "Roraima": "Boa Vista",
    "Santa Catarina": "Florianópolis", "São Paulo": "São Paulo", "Sergipe": "Aracaju",
    "Tocantins": "Palmas",
}
PAISES_GEO = {
    "Argentina": "Buenos Aires", "Chile": "Santiago", "Uruguai": "Montevidéu", "Paraguai": "Assunção",
    "Peru": "Lima", "Colômbia": "Bogotá", "Venezuela": "Caracas", "Equador": "Quito",
    "Portugal": "Lisboa", "Espanha": "Madri", "França": "Paris", "Itália": "Roma",
    "Alemanha": "Berlim", "Reino Unido": "Londres", "Japão": "Tóquio", "China": "Pequim",
    "Índia": "Nova Délhi", "Egito": "Cairo", "México": "Cidade do México", "Canadá": "Ottawa",
    "Estados Unidos": "Washington D.C.", "Austrália": "Camberra", "Rússia": "Moscou", "Turquia": "Ancara",
}
_fila_geo = []


def perg_geo(nivel=0):
    """Sorteia estados e países sem parar (o baralho é embaralhado de novo quando acaba)."""
    global _fila_geo
    if not _fila_geo:
        _fila_geo = [("estado", k) for k in ESTADOS_GEO] + [("pais", k) for k in PAISES_GEO]
        random.shuffle(_fila_geo)
    tipo, nome = _fila_geo.pop()
    base = ESTADOS_GEO if tipo == "estado" else PAISES_GEO
    certa = base[nome]
    outras = list(set(base.values()) - {certa})
    alts = random.sample(outras, 3) + [certa]
    random.shuffle(alts)
    rotulo = "Estado" if tipo == "estado" else "País"
    return rotulo + ": " + nome + " - qual é a sua capital?", alts, alts.index(certa)

# ---------- MATEMÁTICA (perguntas geradas sem parar) ----------
def _opcoes_mat(certa):
    s = {certa}
    while len(s) < 4:
        v = certa + random.choice([-1, 1]) * random.randint(1, max(3, abs(certa) // 5 + 2))
        if v >= 0:
            s.add(v)
    alts = list(s)
    random.shuffle(alts)
    return [str(a) for a in alts], alts.index(certa)


def perg_mat(nivel=0):
    """Gera contas NOVAS o tempo todo: sem limite de perguntas! A dificuldade sobe com os pontos."""
    n = min(nivel // 60, 4)
    tipos = ["soma", "sub", "mult"]
    if n >= 1:
        tipos.append("div")
    if n >= 2:
        tipos.append("perc")
    if n >= 3:
        tipos.append("eq")
    tipo = random.choice(tipos)
    if tipo == "soma":
        a, b = random.randint(10, 50 + n * 60), random.randint(10, 50 + n * 60)
        enun, certa = "Quanto é " + str(a) + " + " + str(b) + "?", a + b
    elif tipo == "sub":
        a = random.randint(30, 100 + n * 80)
        b = random.randint(5, a - 1)
        enun, certa = "Quanto é " + str(a) + " - " + str(b) + "?", a - b
    elif tipo == "mult":
        a, b = random.randint(2, 10 + n * 3), random.randint(2, 10 + n * 2)
        enun, certa = "Quanto é " + str(a) + " × " + str(b) + "?", a * b
    elif tipo == "div":
        b, r = random.randint(2, 9 + n), random.randint(2, 12)
        enun, certa = "Quanto é " + str(b * r) + " ÷ " + str(b) + "?", r
    elif tipo == "perc":
        p = random.choice([10, 20, 25, 50])
        base = random.choice([40, 80, 120, 200, 240, 360, 500])
        enun, certa = "Quanto é " + str(p) + "% de " + str(base) + "?", p * base // 100
    else:
        a, x, b = random.randint(2, 9), random.randint(1, 12), random.randint(1, 20)
        enun, certa = "Resolva: " + str(a) + "x + " + str(b) + " = " + str(a * x + b) + ".  Quanto vale x?", x
    alts, idx = _opcoes_mat(certa)
    return enun, alts, idx

# ---------- HISTÓRIA ----------
# (pergunta, [alternativas], índice da correta)
BANCO_HIS = [
    ("Em que ano ocorreu a Proclamação da República no Brasil?", ["1500", "1822", "1889", "1930"], 2),
    ("Em que ano os portugueses chegaram ao Brasil?", ["1492", "1500", "1530", "1822"], 1),
    ("Quem comandou a esquadra que chegou ao Brasil em 1500?", ["Pedro Álvares Cabral", "Cristóvão Colombo", "Vasco da Gama", "Américo Vespúcio"], 0),
    ("Em que ano o Brasil declarou sua Independência?", ["1808", "1822", "1889", "1888"], 1),
    ("Quem proclamou a Independência do Brasil?", ["D. Pedro I", "D. João VI", "Tiradentes", "Getúlio Vargas"], 0),
    ("Qual lei aboliu a escravidão no Brasil, em 1888?", ["Lei do Ventre Livre", "Lei Áurea", "Lei Eusébio de Queirós", "Lei dos Sexagenários"], 1),
    ("Quem assinou a Lei Áurea?", ["Princesa Isabel", "D. Pedro I", "Deodoro da Fonseca", "Zumbi"], 0),
    ("Quem foi o primeiro presidente do Brasil?", ["Getúlio Vargas", "Deodoro da Fonseca", "Juscelino Kubitschek", "Floriano Peixoto"], 1),
    ("Qual movimento de 1789 em Minas Gerais tinha Tiradentes como líder?", ["Inconfidência Mineira", "Farroupilha", "Cabanagem", "Guerra de Canudos"], 0),
    ("Em que ano a família real portuguesa chegou ao Brasil?", ["1500", "1808", "1822", "1889"], 1),
    ("Quem foi o líder do Quilombo dos Palmares?", ["Zumbi dos Palmares", "Tiradentes", "Dom Pedro II", "Antônio Conselheiro"], 0),
    ("Qual tratado dividiu as terras da América entre Portugal e Espanha em 1494?", ["Tratado de Versalhes", "Tratado de Tordesilhas", "Tratado de Madri", "Tratado de Utrecht"], 1),
    ("Em que ano começou a Primeira Guerra Mundial?", ["1905", "1914", "1939", "1945"], 1),
    ("Em que ano começou a Segunda Guerra Mundial?", ["1914", "1929", "1939", "1945"], 2),
    ("Em que ano terminou a Segunda Guerra Mundial?", ["1939", "1942", "1945", "1950"], 2),
    ("Em que ano foi promulgada a Constituição Cidadã do Brasil?", ["1946", "1967", "1988", "2000"], 2),
    ("Em que ano ocorreu o golpe militar no Brasil?", ["1930", "1945", "1964", "1985"], 2),
    ("Qual período do governo de Getúlio Vargas começou em 1937?", ["Estado Novo", "República Velha", "Ditadura Militar", "Segundo Reinado"], 0),
    ("Em que ano foi inaugurada Brasília?", ["1950", "1960", "1970", "1985"], 1),
    ("Qual era a capital do Brasil antes de Brasília?", ["Salvador", "São Paulo", "Rio de Janeiro", "Recife"], 2),
    ("Em que ano começou a Revolução Francesa?", ["1689", "1776", "1789", "1815"], 2),
    ("Em que ano os Estados Unidos declararam sua independência?", ["1776", "1789", "1822", "1500"], 0),
    ("Qual civilização antiga construiu as pirâmides de Gizé?", ["Grega", "Egípcia", "Romana", "Maia"], 1),
    ("Em que ano caiu o Muro de Berlim?", ["1961", "1975", "1989", "2001"], 2),
    ("Qual país foi o principal rival dos EUA na Guerra Fria?", ["China", "URSS", "Alemanha", "Japão"], 1),
    ("Onde começou a Revolução Industrial?", ["Inglaterra", "Brasil", "Japão", "Egito"], 0),
    ("Qual foi a primeira capital do Brasil?", ["Salvador", "Rio de Janeiro", "Brasília", "Olinda"], 0),
]

_fila_his = []


def perg_his(nivel=0):
    """Sorteia perguntas sem parar: quando o banco acaba, ele é embaralhado de novo."""
    global _fila_his
    if not _fila_his:
        _fila_his = BANCO_HIS[:]
        random.shuffle(_fila_his)
    enunciado, alts, c = _fila_his.pop()
    certa = alts[c]
    alts = alts[:]
    random.shuffle(alts)
    return enunciado, alts, alts.index(certa)

# ---------- PORTUGUÊS ----------
# (pergunta, [alternativas], índice da correta)
BANCO_POR = [
    ("Qual alternativa apresenta a palavra escrita corretamente?", ["Exessão", "Excessão", "Exceção", "Esceção"], 2),
    ("Qual palavra está escrita corretamente?", ["Beneficiente", "Beneficente", "Benefisente", "Beneficiênte"], 1),
    ("Qual é o plural de cidadão?", ["Cidadões", "Cidadãos", "Cidadães", "Cidadans"], 1),
    ("Qual é o plural de pão?", ["Pãos", "Pões", "Pães", "Pãezes"], 2),
    ("Qual frase está correta?", ["Houveram muitos erros.", "Houve muitos erros.", "Haveram muitos erros.", "Houverão muitos erros."], 1),
    ("Qual é um sinônimo de efêmero?", ["Duradouro", "Passageiro", "Eterno", "Sólido"], 1),
    ("Qual é o antônimo de generoso?", ["Bondoso", "Egoísta", "Gentil", "Nobre"], 1),
    ("Qual destas palavras é proparoxítona?", ["Café", "Árvore", "Amor", "Lápis"], 1),
    ("Na frase Os alunos estudaram, qual é o sujeito?", ["Estudaram", "Os alunos", "Os", "Não há sujeito"], 1),
    ("Qual é a classe gramatical de rapidamente?", ["Adjetivo", "Advérbio", "Substantivo", "Verbo"], 1),
    ("Qual é o coletivo de abelhas?", ["Cardume", "Enxame", "Manada", "Alcateia"], 1),
    ("Qual é o coletivo de lobos?", ["Alcateia", "Rebanho", "Bando", "Cardume"], 0),
    ("Qual é a forma correta?", ["Concerteza", "Com certeza", "Com serteza", "Conserteza"], 1),
    ("Complete: Ele é um ___ aluno, sempre atrapalha a aula.", ["mal", "mau", "mais", "maul"], 1),
    ("Complete: Eu ___ à escola ontem.", ["foi", "fui", "fomos", "vou"], 1),
    ("Seus olhos são duas estrelas. Que figura de linguagem é essa?", ["Metáfora", "Antítese", "Onomatopeia", "Eufemismo"], 0),
    ("Chorei um rio de lágrimas. Que figura de linguagem é essa?", ["Antítese", "Hipérbole", "Eufemismo", "Onomatopeia"], 1),
    ("Tic-tac é um exemplo de:", ["Metáfora", "Onomatopeia", "Antítese", "Ironia"], 1),
    ("Qual é o aumentativo de casa?", ["Casinha", "Casarão", "Casebre", "Casota"], 1),
    ("Qual é o feminino de ator?", ["Atora", "Atriz", "Atoriz", "Atrizes"], 1),
    ("Qual palavra está escrita corretamente?", ["Analize", "Análize", "Análise", "Anális"], 2),
    ("Qual palavra possui um dígrafo?", ["Casa", "Chuva", "Bola", "Sapo"], 1),
    ("Quantas sílabas tem a palavra borboleta?", ["3", "4", "5", "6"], 1),
    ("Qual palavra possui um hiato?", ["Saída", "Pai", "Muito", "Fauna"], 0),
    ("Qual palavra está escrita corretamente?", ["Obrigatório", "Obrigatorio", "Obrigatóreo", "Obrigatôrio"], 0),
    ("Qual é a forma correta do verbo: Nós ___ na praia.", ["vai", "vamos", "vão", "vou"], 1),
    ("Qual palavra é um substantivo?", ["Correr", "Felicidade", "Rapidamente", "Bonito"], 1),
    ("Qual é o antônimo de alegria?", ["Felicidade", "Tristeza", "Euforia", "Contentamento"], 1),
]

_fila_por = []


def perg_por(nivel=0):
    """Sorteia perguntas sem parar: quando o banco acaba, ele é embaralhado de novo."""
    global _fila_por
    if not _fila_por:
        _fila_por = BANCO_POR[:]
        random.shuffle(_fila_por)
    enunciado, alts, c = _fila_por.pop()
    certa = alts[c]
    alts = alts[:]
    random.shuffle(alts)
    return enunciado, alts, alts.index(certa)

# (nome, cor, ícone, função que sorteia a pergunta)
DISC = [
    ("Educação Física", (255, 0, 110), "bola", perg_edf),
    ("Geografia", (0, 150, 255), "globo", perg_geo),
    ("Matemática", (255, 145, 0), "calc", perg_mat),
    ("História", (150, 70, 255), "ampulheta", perg_his),
    ("Português", (0, 200, 120), "letra", perg_por),
]

# ============================ INICIALIZAÇÃO ============================
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(JOGO)
relogio = pygame.time.Clock()


def fonte(tam, negrito=True):
    return pygame.font.SysFont("arial,helvetica,dejavusans", tam, bold=negrito)


F_TIT = fonte(56)
F_GRD = fonte(34)
F_MED = fonte(26)
F_BOL = fonte(22)
F_PEQ = fonte(20, False)

CORES = [(255, 0, 110), (255, 190, 11), (58, 134, 255), (6, 214, 160), (131, 56, 236), (251, 86, 7)]
BRANCO = (255, 255, 255)
ESCURO = (25, 20, 50)
VERDE = (0, 230, 118)
VERMELHO = (255, 23, 68)
CINZA = (120, 115, 140)
AMARELO = (255, 235, 59)

Y_JOGADOR = 545
BTN_FIM1 = pygame.Rect(150, 540, 300, 60)
BTN_FIM2 = pygame.Rect(510, 540, 300, 60)
CARTOES = []   # (rect, índice ou None para modo misto)
for k in range(6):
    CARTOES.append((pygame.Rect(40 + (k % 3) * 300, 235 + (k // 3) * 150, 280, 130), k if k < 5 else None))

J = {}
particulas = []
popups = []
bolas = [[random.uniform(0, LARGURA), random.uniform(0, ALTURA),
          random.uniform(-1.6, 1.6), random.uniform(-1.6, 1.6),
          random.randint(18, 70), random.random()] for _ in range(22)]


# ============================ FUNÇÕES AUXILIARES ============================
def hsv(h, s=1.0, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(h % 1, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def texto(s, fnt, cor, centro=None, topo_esq=None, sombra=True):
    img = fnt.render(s, True, cor)
    r = img.get_rect()
    if centro:
        r.center = centro
    if topo_esq:
        r.topleft = topo_esq
    if sombra:
        tela.blit(fnt.render(s, True, (0, 0, 0)), r.move(2, 3))
    tela.blit(img, r)
    return r


def texto_arco_iris(s, fnt, centro, t):
    larg = sum(fnt.size(c)[0] for c in s)
    x = centro[0] - larg // 2
    for i, c in enumerate(s):
        y = centro[1] + math.sin(t * 3 + i * 0.5) * 6
        texto(c, fnt, hsv(t * 0.3 + i * 0.05, 0.85, 1), centro=(x + fnt.size(c)[0] // 2, y))
        x += fnt.size(c)[0]


def quebrar(s, fnt, largura):
    linhas, atual = [], ""
    for palavra in s.split():
        teste = (atual + " " + palavra).strip()
        if fnt.size(teste)[0] <= largura:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    linhas.append(atual)
    return linhas


def texto_centralizado(s, fnt, cor, rect, sombra=True, margem=24):
    linhas = quebrar(s, fnt, rect.width - margem)
    alt = fnt.get_height()
    y0 = rect.centery - alt * len(linhas) // 2 + alt // 2
    for i, ln in enumerate(linhas):
        texto(ln, fnt, cor, centro=(rect.centerx, y0 + i * alt), sombra=sombra)


def explodir(x, y, cor=None, n=45):
    for _ in range(n):
        a = random.uniform(0, 6.283)
        v = random.uniform(2, 9)
        particulas.append([x, y, math.cos(a) * v, math.sin(a) * v, random.randint(25, 55),
                           random.choice(CORES) if cor is None else cor])


def desenhar_particulas():
    for p in particulas[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.25
        p[4] -= 1
        if p[4] <= 0:
            particulas.remove(p)
            continue
        pygame.draw.circle(tela, p[5], (int(p[0]), int(p[1])), max(2, p[4] // 7))


def desenhar_popups():
    for p in popups[:]:
        p[2] -= 1.5
        p[3] -= 1
        if p[3] <= 0:
            popups.remove(p)
            continue
        texto(p[0], F_GRD, p[4], centro=(int(p[1]), int(p[2])))


def fundo(t):
    faixas = 50
    h = ALTURA // faixas + 1
    for i in range(faixas):
        cor = hsv(t * 0.04 + i / faixas * 0.35, 0.8, 0.55 + 0.12 * math.sin(t * 1.5 + i * 0.2))
        pygame.draw.rect(tela, cor, (0, i * ALTURA // faixas, LARGURA, h))
    ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    for b in bolas:
        b[0] += b[2]
        b[1] += b[3]
        if b[0] < 0 or b[0] > LARGURA:
            b[2] *= -1
        if b[1] < 0 or b[1] > ALTURA:
            b[3] *= -1
        pygame.draw.circle(ov, hsv(b[5] + t * 0.1) + (80,), (int(b[0]), int(b[1])), b[4])
    tela.blit(ov, (0, 0))


def botao(rect, rotulo, cor, fnt=None):
    fnt = fnt or F_MED
    r = rect.copy()
    if rect.collidepoint(pygame.mouse.get_pos()):
        r = r.inflate(16, 8)
    pygame.draw.rect(tela, (0, 0, 0), r.move(4, 7), border_radius=20)
    pygame.draw.rect(tela, cor, r, border_radius=20)
    pygame.draw.rect(tela, BRANCO, r, 4, border_radius=20)
    texto_centralizado(rotulo, fnt, BRANCO, r)


def coracao(x, y, s, cor):
    pygame.draw.circle(tela, cor, (x - s // 2, y), s // 2 + 1)
    pygame.draw.circle(tela, cor, (x + s // 2, y), s // 2 + 1)
    pygame.draw.polygon(tela, cor, [(x - s - 1, y + 3), (x + s + 1, y + 3), (x, y + s + s // 2)])


def desenhar_icone(cx, cy, r, t, icone):
    """Elementos gráficos de cada disciplina (desenhados com formas do Pygame)."""
    if icone == "bola":
        pygame.draw.circle(tela, BRANCO, (cx, cy), r)
        pts = [(cx + math.cos(t + k * 1.2566) * r * 0.42, cy + math.sin(t + k * 1.2566) * r * 0.42) for k in range(5)]
        pygame.draw.polygon(tela, ESCURO, pts)
        for k in range(5):
            x2 = cx + math.cos(t + k * 1.2566) * r * 0.95
            y2 = cy + math.sin(t + k * 1.2566) * r * 0.95
            pygame.draw.line(tela, ESCURO, pts[k], (x2, y2), max(2, r // 18))
        pygame.draw.circle(tela, ESCURO, (cx, cy), r, max(2, r // 14))
    elif icone == "globo":
        pygame.draw.circle(tela, (30, 144, 255), (cx, cy), r)
        pygame.draw.ellipse(tela, (0, 200, 83), (int(cx - r * 0.65), int(cy - r * 0.55), int(r * 0.7), int(r * 0.8)))
        pygame.draw.ellipse(tela, (0, 200, 83), (int(cx + r * 0.1), int(cy - r * 0.1), int(r * 0.6), int(r * 0.7)))
        w = max(4, int(abs(math.cos(t)) * r))
        pygame.draw.ellipse(tela, BRANCO, (cx - w, cy - r, 2 * w, 2 * r), 2)
        pygame.draw.line(tela, BRANCO, (cx - r, cy), (cx + r, cy), 2)
        pygame.draw.circle(tela, BRANCO, (cx, cy), r, max(2, r // 14))
    elif icone == "calc":
        corpo = pygame.Rect(0, 0, int(r * 1.5), int(r * 2))
        corpo.center = (cx, cy)
        pygame.draw.rect(tela, ESCURO, corpo, border_radius=10)
        pygame.draw.rect(tela, BRANCO, corpo, 3, border_radius=10)
        pygame.draw.rect(tela, (150, 255, 200), (corpo.x + 6, corpo.y + 6, corpo.w - 12, r // 2 - 2), border_radius=4)
        for i in range(3):
            for j in range(3):
                c = CORES[(i + j + int(t * 2)) % len(CORES)]
                pygame.draw.circle(tela, c, (corpo.x + corpo.w // 6 + i * corpo.w // 3, corpo.y + r // 2 + r // 4 + j * (r // 2)), max(3, r // 8))
    elif icone == "ampulheta":
        w = int(r * 0.9)
        pygame.draw.polygon(tela, (255, 213, 79), [(cx - w, cy - r), (cx + w, cy - r), (cx, cy)])
        pygame.draw.polygon(tela, (255, 213, 79), [(cx - w, cy + r), (cx + w, cy + r), (cx, cy)])
        pygame.draw.polygon(tela, (255, 112, 67), [(cx - w // 2, cy + r), (cx + w // 2, cy + r), (cx, cy + r - int(r * 0.6 * abs(math.sin(t))) - 4)])
        pygame.draw.rect(tela, ESCURO, (cx - w - 6, cy - r - 8, 2 * w + 12, 9), border_radius=4)
        pygame.draw.rect(tela, ESCURO, (cx - w - 6, cy + r - 1, 2 * w + 12, 9), border_radius=4)
    else:
        pygame.draw.circle(tela, (0, 160, 100), (cx, cy), r)
        pygame.draw.circle(tela, BRANCO, (cx, cy), r, max(2, r // 14))
        texto("Aa", fonte(int(r * 0.95)), BRANCO, centro=(cx, cy + int(math.sin(t * 3) * 3)))


def desenhar_jogador(px, t):
    """Personagem que o jogador controla."""
    y = Y_JOGADOR + 28 + int(math.sin(t * 6) * 3)
    pygame.draw.ellipse(tela, (0, 0, 0), (px - 42, y + 24, 84, 14))
    pygame.draw.circle(tela, AMARELO, (int(px), y), 38)
    pygame.draw.circle(tela, ESCURO, (int(px), y), 38, 4)
    mx = pygame.mouse.get_pos()[0]
    olhar = max(-4, min(4, (mx - px) / 60))
    for dx in (-14, 14):
        pygame.draw.circle(tela, BRANCO, (int(px + dx), y - 8), 10)
        pygame.draw.circle(tela, ESCURO, (int(px + dx + olhar), y - 8), 5)
    pygame.draw.arc(tela, ESCURO, (int(px - 16), y - 2, 32, 24), 3.4, 6.0, 4)
    pygame.draw.line(tela, ESCURO, (px, y - 38), (px, y - 54), 4)
    pygame.draw.circle(tela, CORES[int(t * 4) % len(CORES)], (int(px), y - 56), 8)


# ============================ LÓGICA DO JOGO ============================
def novo_jogo(modo):
    J.update(estado="jogo", modo=modo, pontos=0, acertos=0, erros=0, vidas=VIDAS_INICIAIS,
             seq=0, melhor=0, total=0, msg="", msg_cor=BRANCO, px=LARGURA / 2, alvo=LARGURA / 2,
             disc=-1, t=0.0, st={d[0]: [0, 0] for d in DISC})
    proxima()


def nivel():
    return 1 + J["acertos"] // 4


def proxima():
    if J["modo"] is None:
        d = random.choice([i for i in range(len(DISC)) if i != J["disc"]])
    else:
        d = J["modo"]
    enun, alts, c = DISC[d][3](J["pontos"])
    J.update(disc=d, q=enun, alts=alts, certa=c, y=205.0, escolhido=-1, tempo_fb=0,
             fase=random.random() * 6)


def rect_bolha(i):
    cx = 120 + 240 * i + math.sin(J["t"] * 1.6 + i * 1.7 + J["fase"]) * 16
    r = pygame.Rect(0, 0, 220, 92)
    r.center = (cx, J["y"] + 46 + (i % 2) * 26)
    return r


def resolver(i):
    """i = bolha pegada (0-3) ou 4 se a resposta certa passou sem ser pega."""
    if J["escolhido"] != -1:
        return
    J["escolhido"] = i
    J["tempo_fb"] = pygame.time.get_ticks()
    J["total"] += 1
    nome = DISC[J["disc"]][0]
    pos = rect_bolha(i).center if i < 4 else (int(J["px"]), 480)
    if i == J["certa"]:
        J["acertos"] += 1
        J["seq"] += 1
        J["melhor"] = max(J["melhor"], J["seq"])
        J["st"][nome][0] += 1
        ganho = 10 + min(J["seq"] - 1, 5) * 2
        J["pontos"] += ganho
        J["msg"], J["msg_cor"] = "Correto! +" + str(ganho) + " pontos", VERDE
        popups.append(["+" + str(ganho), pos[0], pos[1], 50, VERDE])
        explodir(pos[0], pos[1], None, 55)
        if J["seq"] % 5 == 0 and J["vidas"] < VIDAS_MAX:
            J["vidas"] += 1
            popups.append(["+1 VIDA!", LARGURA // 2, 250, 70, (255, 105, 180)])
        if J["acertos"] % 4 == 0:
            popups.append(["NÍVEL " + str(nivel()) + "!", LARGURA // 2, 300, 70, AMARELO])
    else:
        J["erros"] += 1
        J["seq"] = 0
        J["st"][nome][1] += 1
        J["pontos"] = max(0, J["pontos"] - 5)
        J["vidas"] -= 1
        J["msg"], J["msg_cor"] = "Ops! -5 pontos. Resposta certa: " + J["alts"][J["certa"]], VERMELHO
        popups.append(["-5", pos[0], pos[1], 50, VERMELHO])
        explodir(pos[0], pos[1], VERMELHO, 30)


def terminar():
    J["estado"] = "fim"
    if J.get("acertos", 0) > 0:
        for _ in range(6):
            explodir(random.randint(100, LARGURA - 100), random.randint(80, 300), None, 40)


def tratar_evento(e):
    est = J["estado"]
    if e.type == pygame.KEYDOWN:
        if est == "menu":
            teclas = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4}
            if e.key in teclas:
                novo_jogo(teclas[e.key])
            elif e.key in (pygame.K_6, pygame.K_RETURN, pygame.K_SPACE):
                novo_jogo(None)
            elif e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif est == "jogo" and e.key == pygame.K_ESCAPE:
            terminar()
        elif est == "fim":
            if e.key == pygame.K_RETURN:
                J["estado"] = "menu"
            elif e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    elif e.type == pygame.MOUSEMOTION and est == "jogo":
        J["alvo"] = e.pos[0]
    elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        if est == "menu":
            for r, modo in CARTOES:
                if r.collidepoint(e.pos):
                    novo_jogo(modo)
        elif est == "jogo" and J["escolhido"] == -1:
            for i in range(4):
                if rect_bolha(i).collidepoint(e.pos):
                    resolver(i)
        elif est == "fim":
            if BTN_FIM1.collidepoint(e.pos):
                J["estado"] = "menu"
            elif BTN_FIM2.collidepoint(e.pos):
                pygame.quit()
                sys.exit()


def atualizar(t):
    if J["estado"] != "jogo":
        return
    J["t"] = t
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        J["alvo"] = J["px"] - 14
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        J["alvo"] = J["px"] + 14
    J["alvo"] = max(50, min(LARGURA - 50, J["alvo"]))
    J["px"] += (J["alvo"] - J["px"]) * 0.3
    if J["escolhido"] == -1:
        J["y"] += min(0.9 + 0.12 * (nivel() - 1), 2.4)
        jog = pygame.Rect(int(J["px"]) - 45, Y_JOGADOR, 90, 60)
        for i in range(4):
            if rect_bolha(i).colliderect(jog):
                resolver(i)
                break
        if J["escolhido"] == -1 and J["y"] > 520:
            resolver(4)
    elif pygame.time.get_ticks() - J["tempo_fb"] > FEEDBACK_MS:
        if J["vidas"] <= 0:
            terminar()
        else:
            proxima()


# ============================ TELAS ============================
def tela_menu(t):
    texto_arco_iris(JOGO.upper(), F_TIT, (LARGURA // 2, 60), t)
    texto("Educação Física  •  Geografia  •  Matemática  •  História  •  Português", F_PEQ, BRANCO,
          centro=(LARGURA // 2, 118), sombra=False)
    caixa = pygame.Surface((760, 70), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (20, 10, 60, 170), caixa.get_rect(), border_radius=20)
    tela.blit(caixa, (LARGURA // 2 - 380, 140))
    texto("EQUIPE: " + "  |  ".join(EQUIPE), F_MED, AMARELO, centro=(LARGURA // 2, 165))
    texto("Pegue a bolha com a resposta certa!  Mouse ou setas movem o personagem.", F_PEQ, BRANCO,
          centro=(LARGURA // 2, 195), sombra=False)
    for k, (r, modo) in enumerate(CARTOES):
        if modo is None:
            cor, nome, ic = CORES[int(t * 2) % len(CORES)], "MODO MISTO (todas)", None
        else:
            cor, nome, ic = DISC[modo][1], DISC[modo][0], DISC[modo][2]
        rr = r.inflate(14, 8) if r.collidepoint(pygame.mouse.get_pos()) else r
        pygame.draw.rect(tela, (0, 0, 0), rr.move(4, 7), border_radius=22)
        pygame.draw.rect(tela, cor, rr, border_radius=22)
        pygame.draw.rect(tela, BRANCO, rr, 4, border_radius=22)
        if ic:
            desenhar_icone(rr.x + 55, rr.centery, 36, t + k, ic)
        else:
            for n in range(5):
                desenhar_icone(rr.x + 32 + (n % 2) * 44, rr.y + 40 + (n // 2) * 32 + (n % 2) * 6, 16, t + n, DISC[n][2])
        texto_centralizado(nome, F_MED, BRANCO, pygame.Rect(rr.x + 100, rr.y, rr.w - 110, rr.h))
        texto(str(k + 1), F_PEQ, BRANCO, topo_esq=(rr.right - 22, rr.y + 8), sombra=False)
    texto("Clique numa disciplina (ou tecla 1-6) para começar  |  ESC sai", F_PEQ, BRANCO,
          centro=(LARGURA // 2, 570), sombra=False)


def tela_jogo(t):
    nome, cor_d, ic, _ = DISC[J["disc"]]
    texto("Pontos: " + str(J["pontos"]), F_GRD, AMARELO, topo_esq=(25, 10))
    texto("Nível " + str(nivel()) + "  |  Sequência " + str(J["seq"]), F_MED, BRANCO, centro=(LARGURA // 2, 30))
    for i in range(VIDAS_MAX):
        c = (255, 45, 85) if i < J["vidas"] else (90, 80, 110)
        coracao(LARGURA - 35 - i * 44, 26, 15, c)
    # painel da pergunta
    caixa = pygame.Surface((900, 120), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (255, 255, 255, 240), caixa.get_rect(), border_radius=24)
    pygame.draw.rect(caixa, cor_d, caixa.get_rect(), 6, border_radius=24)
    tela.blit(caixa, (30, 65))
    etiqueta = pygame.Rect(48, 58, 230, 30)
    pygame.draw.rect(tela, cor_d, etiqueta, border_radius=15)
    pygame.draw.rect(tela, BRANCO, etiqueta, 2, border_radius=15)
    texto(nome, F_PEQ, BRANCO, centro=etiqueta.center, sombra=False)
    desenhar_icone(895, 125, 26, t, ic)
    fnt = F_MED
    linhas = quebrar(J["q"], fnt, 780)
    if len(linhas) > 2:
        fnt = F_BOL
    texto_centralizado(J["q"], fnt, ESCURO, pygame.Rect(45, 88, 800, 88), sombra=False, margem=10)
    # linha de chegada
    pygame.draw.line(tela, (255, 255, 255), (0, Y_JOGADOR - 6), (LARGURA, Y_JOGADOR - 6), 2)
    # bolhas
    for i in range(4):
        r = rect_bolha(i)
        cor = CORES[i]
        if J["escolhido"] != -1:
            if i == J["certa"]:
                cor = VERDE
            elif i == J["escolhido"]:
                cor = VERMELHO
            else:
                cor = CINZA
        pygame.draw.rect(tela, (0, 0, 0), r.move(4, 6), border_radius=44)
        pygame.draw.rect(tela, cor, r, border_radius=44)
        pygame.draw.rect(tela, BRANCO, r, 4, border_radius=44)
        pygame.draw.ellipse(tela, (255, 255, 255), (r.x + 22, r.y + 8, 56, 14))
        texto_centralizado(J["alts"][i], F_BOL, BRANCO, r, margem=40)
    desenhar_jogador(J["px"], t)
    if J["escolhido"] != -1:
        texto(J["msg"], F_MED, J["msg_cor"], centro=(LARGURA // 2, 195))


def tela_fim(t):
    total = J["total"]
    pct = J["acertos"] * 100 // total if total else 0
    if pct >= 80:
        msg = "Incrível! Você domina o assunto!"
    elif pct >= 50:
        msg = "Muito bem! Continue praticando!"
    else:
        msg = "Bom esforço! Tente de novo e melhore!"
    texto_arco_iris("Parabéns!", F_TIT, (LARGURA // 2, 55), t)
    texto("Você concluiu o Super Desafio Escolar!", F_GRD, BRANCO, centro=(LARGURA // 2, 110))
    caixa = pygame.Surface((820, 330), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (20, 10, 60, 190), caixa.get_rect(), border_radius=26)
    tela.blit(caixa, (70, 150))
    linhas = [("Pontuação final: " + str(J["pontos"]) + " pontos", AMARELO),
              ("Acertos: " + str(J["acertos"]) + "/" + str(total) + "     Erros: " + str(J["erros"]), VERDE),
              ("Maior sequência: " + str(J["melhor"]) + "     Nível: " + str(nivel()), (130, 200, 255))]
    for i, (s, c) in enumerate(linhas):
        texto(s, F_GRD, c, centro=(LARGURA // 2, 190 + i * 42))
    for i, d in enumerate(DISC):
        a, e = J["st"][d[0]]
        x = 110 + (i % 3) * 260
        y = 340 + (i // 3) * 60
        pygame.draw.rect(tela, d[1], (x, y, 240, 48), border_radius=16)
        pygame.draw.rect(tela, BRANCO, (x, y, 240, 48), 3, border_radius=16)
        texto(d[0], F_PEQ, BRANCO, centro=(x + 120, y + 14), sombra=False)
        texto(str(a) + " certas / " + str(e) + " erradas", F_PEQ, BRANCO, centro=(x + 120, y + 34), sombra=False)
    texto(msg, F_MED, BRANCO, centro=(LARGURA // 2, 505))
    botao(BTN_FIM1, "MENU (ENTER)", CORES[3], F_MED)
    botao(BTN_FIM2, "SAIR (ESC)", CORES[0], F_MED)


def desenhar(t):
    fundo(t)
    if J["estado"] == "menu":
        tela_menu(t)
    elif J["estado"] == "jogo":
        tela_jogo(t)
    else:
        tela_fim(t)
    desenhar_particulas()
    desenhar_popups()


def main():
    J.update(estado="menu")
    t0 = pygame.time.get_ticks()
    while True:
        t = (pygame.time.get_ticks() - t0) / 1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            tratar_evento(e)
        atualizar(t)
        desenhar(t)
        pygame.display.flip()
        relogio.tick(60)


if __name__ == "__main__":
    main()
