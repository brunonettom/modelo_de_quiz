import os
import pyfiglet
import time

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

os.system('cls')
print(gg("Seu froxo!", 'vermelho'))
time.sleep(2)


os.system('cls')
print(gg(f'A resposta certa era:', 'verde'))

time.sleep(2)
os.system('cls')
print(gg('RUFEM OS TAMBORES.','azul'))

time.sleep(0.6)
os.system('cls')
print(gg('RUFEM OS TAMBORES..','azul'))

time.sleep(0.6)
os.system('cls')
print(gg('RUFEM OS TAMBORES...','azul'))

time.sleep(0.6)
os.system('cls')
print(gg('RUFEM OS TAMBORES.','azul'))

time.sleep(0.6)
os.system('cls')
print(gg('RUFEM OS TAMBORES..','azul'))

time.sleep(0.6)
os.system('cls')
print(gg('RUFEM OS TAMBORES...','azul'))




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
print(gg('resposta_certa'.upper(), 'amarelo'))
time.sleep(1)