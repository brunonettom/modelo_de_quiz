import os
import pyfiglet
import time
import unicodedata

#FUNÇÕES

def pintador(texto, cor):
    cores = {
        "preto": "30",
        "vermelho": "31",
        "verde": "32",
        "amarelo": "33",
        "azul": "34",
        "magenta": "35",
        "ciano": "36",
        "branco": "37",
        "cinza": "90",
        "vermelho_claro": "91",
        "verde_claro": "92",
        "amarelo_claro": "93",
        "azul_claro": "94",
        "magenta_claro": "95",
        "ciano_claro": "96",
        "branco_claro": "97"
    }
    codigo = cores.get(cor.lower())
    if codigo:
        return f"\033[{codigo}m{texto}\033[0m"
    else:
        return texto  # se a cor não existir, retorna sem cor

def gg(txt, cor):
    return pintador(pyfiglet.figlet_format(txt), cor)


def normalizar(palavra):
    norm_txt = unicodedata.normalize('NFKD', palavra).lower()
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)




######################INTERFACE

#INÍCIO
def inicio():
    enter='(Aperte enter para continuar)'
    print(enter)
    _ = input(gg("OLAAAAAA!!", 'amarelo'))
    os.system('cls')
    print(enter)
    _ = input(gg("VOCE  ESTA  PRONTO  PARA  O  NOSSO  JOGO?", 'verde'))
    os.system('cls')
    print(enter)
    _ = input(gg("ENTAO  VAMOS  COMECAR!!!", 'amarelo'))
    os.system('cls')
    print(enter)
    _ = input(gg("ESSAS SAO AS REGRAS DO JOGO:", 'vermelho'))
    _ = input(f'- Para ganhar pontos, você vai precisa acertar qual é a parte do corpo da qual estamos falando\n')
    _ = input(f'- Se você precisar, você pode pedir por uma ajudinha nossa...\n')
    _ = input(f'- Mas é CLAAAAAROO que não é de graça')
    _ = input(gg("MUAHAHA!!!", 'vermelho'))
    _ = input(f'- Pra cada dica que você pedir, é um ponto a menos que você vai poder ganhar caso acerte\n')
    _ = input(f'- Em cada tentativa, você será atualizado de quantos pontos você poderá receber\n\n')
    print(f'*O número de dicas restantes é o número de pontos que você poderá receber')
    os.system('cls')
    print(enter)

#DESISTÊNCIA
def desistencia(resposta_certa):
    os.system('cls')
    print(gg("Seu froxo!", 'vermelho'))
    time.sleep(2)


    os.system('cls')
    print(gg(f'A resposta certa era:', 'verde'))

    time.sleep(2)
    os.system('cls')
    print(gg('RUFEM  OS TAMBORES.','azul'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('RUFEM  OS TAMBORES..','azul'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('RUFEM  OS TAMBORES...','azul'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('RUFEM  OS TAMBORES.','azul'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('RUFEM  OS TAMBORES..','azul'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('RUFEM  OS TAMBORES...','azul'))




    time.sleep(0.7)
    os.system('cls')
    print(gg('IMAGINE OS TAMBORES RUFANDO.','verde'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('IMAGINE OS TAMBORES RUFANDO..','verde'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('IMAGINE OS TAMBORES RUFANDO...','verde'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('IMAGINE OS TAMBORES RUFANDO.','verde'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('IMAGINE OS TAMBORES RUFANDO..','verde'))

    time.sleep(0.6)
    os.system('cls')
    print(gg('IMAGINE OS TAMBORES RUFANDO...','verde'))


    time.sleep(0.8)
    os.system('cls')
    print(gg(resposta_certa.upper(), 'amarelo'))
    time.sleep(1)



#QUESTÕES:

games = [
    ['Bulbo', [
        'Sou a parte mais inferior do tronco encefálico',
        'Controlo funções vitais como respiração e frequência cardíaca',
        'Faço a comunicação entre o cérebro e a medula espinhal',
        'Regulo reflexos como tosse, deglutição e vômito',
        'Lesões graves em mim podem ser fatais',
        'Estou diretamente conectado à medula oblonga',
        'Recebo informações dos nervos cranianos inferiores'
    ]],
    ['Corpo caloso', [
        'Sou uma estrutura de fibras nervosas que conecta os dois hemisférios cerebrais',
        'Permito a troca de informações entre os lados esquerdo e direito do cérebro',
        'Minha integridade é essencial para a coordenação inter-hemisférica',
        'Sou formado por substância branca',
        'Sou a maior comissura cerebral',
        'Alterações em mim estão associadas a distúrbios de aprendizagem',
        'Lesões podem causar o chamado “cérebro dividido”'
    ]],
    ['Ínsula', [
        'Estou escondida no interior do sulco lateral do cérebro',
        'Sou importante para a percepção de emoções viscerais',
        'Participo do processamento da dor e do nojo',
        'Tenho papel na autoconsciência e empatia',
        'Sou considerada uma parte do córtex cerebral',
        'Ativo em situações de tomada de decisão emocional complexa',
        'Estou envolvida na experiência subjetiva das emoções'
    ]],
    ['Núcleo accumbens', [
        'Sou uma estrutura chave no circuito de recompensa',
        'Estou associado ao prazer e à motivação',
        'Sou ativado em comportamentos relacionados a vícios',
        'Recebo dopamina da área tegmental ventral',
        'Sou parte do corpo estriado ventral',
        'Minha ativação reforça comportamentos repetitivos',
        'Desempenho papel central na busca por recompensas'
    ]],
    ['Giro do cíngulo', [
        'Sou uma parte do cérebro localizada acima do corpo caloso',
        'Tenho papel na regulação das emoções e comportamento',
        'Participo na formação da memória e atenção',
        'Sou considerado parte do sistema límbico',
        'Ajudo na avaliação de conflitos e controle da dor',
        'Lesões em mim podem causar apatia ou impulsividade',
        'Sou importante na tomada de decisões com base emocional'
    ]]
]
