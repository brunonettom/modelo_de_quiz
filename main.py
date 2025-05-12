import pygame  # importa a biblioteca pygame para criação de jogos e interfaces gráficas
import pygame.freetype  # importa o módulo freetype do pygame para renderizar fontes
import sys  # importa o módulo sys para interagir com o sistema (encerrar o programa)
import time  # importa o módulo time para controlar delays e temporizações
import unicodedata  # importa o módulo unicodedata para normalização de textos
import os  # importa o módulo os para manipulação de caminho de arquivos e diretórios
import asyncio
import traceback  # importa módulo para rastreamento de erros

# Variáveis para debug
DEBUG_MODE = True  # ativa/desativa mensagens de debug
DEBUG_MESSAGES = []  # lista para armazenar mensagens de debug
FRAME_COUNT = 0  # contador de frames para medir FPS
LAST_TIME = 0  # último tempo para cálculo de FPS
BROWSER_MODE = True  # flag para indicar execução no navegador

# Diferente configuração de tela para navegador
LARGURA, ALTURA = 800, 600  # tamanho fixo para ambiente web

# Função para adicionar mensagens de debug
def debug_print(message):
    if DEBUG_MODE:
        print(message)
        DEBUG_MESSAGES.append(str(message))
        # Manter apenas as últimas 10 mensagens
        if len(DEBUG_MESSAGES) > 10:
            DEBUG_MESSAGES.pop(0)

# Inicializa todos os módulos do pygame
try:
    pygame.init()  # inicia o pygame, preparando os módulos internos para uso
    debug_print("Pygame inicializado com sucesso!")
except Exception as e:
    debug_print(f"Erro ao inicializar pygame: {e}")

# Configura a janela em modo normal (não fullscreen)
try:
    tela = pygame.display.set_mode((LARGURA, ALTURA))  # cria janela dimensionada para web
    debug_print("Tela criada com sucesso!")
except Exception as e:
    debug_print(f"Erro ao configurar janela: {e}")

# Define o título da janela
pygame.display.set_caption("Quiz Game")  # ajusta o texto que aparece na barra de título do jogo

# Cores em RGB
BRANCO = (255, 255, 255)  # define a cor branca
PRETO = (0, 0, 0)  # define a cor preta
VERMELHO = (255, 50, 50)  # define um tom de vermelho
VERDE = (50, 255, 50)  # define um tom de verde
AZUL = (50, 50, 255)  # define um tom de azul
AMARELO = (255, 255, 50)  # define um tom de amarelo
CINZA = (200, 200, 200)  # define um tom de cinza

# Fontes com tamanhos diferentes
try:
    fonte_pequena = pygame.freetype.SysFont("Arial", 20)  # fonte Arial tamanho 20
    fonte_media = pygame.freetype.SysFont("Arial", 28)  # fonte Arial tamanho 28
    fonte_larga = pygame.freetype.SysFont("Arial", 36)  # fonte Arial tamanho 36
    fonte_titulo = pygame.freetype.SysFont("Arial", 48)  # fonte Arial tamanho 48
    debug_print("Fontes carregadas com sucesso")
except Exception as e:
    debug_print(f"Erro ao carregar fontes: {e}")

# Função para exibir mensagens de debug na tela
def show_debug_info(surface):
    if not DEBUG_MODE:
        return
    
    global FRAME_COUNT, LAST_TIME
    current_time = pygame.time.get_ticks()
    
    # Calcular FPS a cada segundo
    if current_time - LAST_TIME > 1000:
        debug_print(f"FPS: {FRAME_COUNT}")
        LAST_TIME = current_time
        FRAME_COUNT = 0
    else:
        FRAME_COUNT += 1
    
    y = 10
    for i, message in enumerate(DEBUG_MESSAGES):
        try:
            debug_text, debug_rect = fonte_pequena.render(message, VERDE)
            debug_rect.topleft = (10, y)
            surface.blit(debug_text, debug_rect)
            y += fonte_pequena.get_sized_height() + 2
        except Exception as e:
            # Se falhar ao renderizar uma mensagem, pule para a próxima
            continue

# === 1) Placeholder para dicas em imagem ===
imagem_placeholder = pygame.Surface((200, 120))  # cria superfície cinza para placeholder
imagem_placeholder.fill(CINZA)  # preenche a superfície com cor cinza
pygame.draw.rect(imagem_placeholder, PRETO, imagem_placeholder.get_rect(), 2)  # contorna o retângulo em preto
texto_surf, texto_rect = fonte_pequena.render("Imagem Aqui", PRETO)  # renderiza texto para placeholder
texto_rect.center = imagem_placeholder.get_rect().center  # centraliza o texto na superfície
imagem_placeholder.blit(texto_surf, texto_rect)  # desenha o texto na superfície

# Usar apenas placeholder para simplificar (evitar problemas de carregamento de arquivos)
debug_print("Usando placeholder para imagens")
imagem_dna = imagem_placeholder

# Dados de exemplo para as rodadas (palavra certa e lista de dicas)
jogos = [  # lista de jogos, cada um é [resposta, [dica1, dica2, ...]]
    ["python", ["É uma linguagem de programação", "Tem o nome de um animal", "Começa com P e termina com N"]],
    ["brasil", ["É um país", "Está localizado na América do Sul", "Sua capital é Brasília"]],
    ["café", ["É uma bebida", "Contém cafeína", "É feito a partir de grãos torrados"]]
]

# === Função de normalização de texto ===
def normalizar(texto):  # remove acentos e converte para minúsculas
    if not texto:
        return ""
    texto_baixo = texto.lower()  # converte para minúsculas
    # remove marcas de acentuação (Mn) usando unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto_baixo) if unicodedata.category(c) != 'Mn')

# === Função para desenhar texto na tela ===
def draw_text(texto, fonte, cor, x, y, alinhar="left"):  # desenha texto com alinhamento
    try:
        superficie_texto, rect_texto = fonte.render(texto, cor)  # renderiza texto em superfície
        if alinhar == "center":
            rect_texto.center = (x, y)  # centraliza horizontal e verticalmente
        elif alinhar == "right":
            rect_texto.right, rect_texto.top = x, y  # alinha à direita
        else:  # left
            rect_texto.left, rect_texto.top = x, y  # alinha à esquerda
        tela.blit(superficie_texto, rect_texto)  # desenha na tela
        return rect_texto  # retorna rect para possíveis usos
    except Exception as e:
        debug_print(f"Erro ao desenhar texto: {e}")
        return pygame.Rect(x, y, 1, 1)  # retorna um rect mínimo em caso de erro

# === Função para desenhar um botão e detectar clique ===
def draw_button(texto, x, y, largura_botao, altura_botao, cor_inativa, cor_ativa):
    pos_mouse = pygame.mouse.get_pos()  # obtém posição atual do mouse
    botao_pressionado = pygame.mouse.get_pressed()[0]  # verifica clique esquerdo
    sobre_botao = x <= pos_mouse[0] <= x + largura_botao and y <= pos_mouse[1] <= y + altura_botao  # checa se mouse está sobre
    if sobre_botao:
        pygame.draw.rect(tela, cor_ativa, (x, y, largura_botao, altura_botao))  # desenha botão ativo
        clicou = sobre_botao and botao_pressionado  # detecta clique
    else:
        pygame.draw.rect(tela, cor_inativa, (x, y, largura_botao, altura_botao))  # desenha botão inativo
        clicou = False  # sem clique fora da área
    draw_text(texto, fonte_media, PRETO, x + largura_botao/2, y + altura_botao/2, "center")  # desenha texto centralizado
    return clicou  # retorna True se foi clicado

# === Função para desenhar caixa de input ===
def draw_input_box(x, y, largura_caixa, altura_caixa, texto, ativo):
    cor_borda = VERMELHO if ativo else CINZA  # cor da borda depende se ativo
    pygame.draw.rect(tela, cor_borda, (x, y, largura_caixa, altura_caixa), 2)  # desenha retângulo
    surf_texto, rect_texto = fonte_media.render(texto, BRANCO)  # renderiza texto dentro da caixa
    rect_texto.left = x + 5  # define margem esquerda
    rect_texto.top = y + (altura_caixa - rect_texto.height) // 2  # centraliza verticalmente
    tela.blit(surf_texto, rect_texto)  # desenha o texto na caixa

# === Função para mostrar mensagem temporária ===
async def show_message_async(mensagem, cor=AMARELO, duracao=1.5):
    tela.fill(PRETO)  # limpa tela
    draw_text(mensagem, fonte_larga, cor, LARGURA/2, ALTURA/2, "center")  # desenha mensagem centralizada
    pygame.display.flip()  # atualiza tela
    
    # Substituir time.sleep por asyncio.sleep
    await asyncio.sleep(duracao)

def show_message(mensagem, cor=AMARELO, duracao=1.5):
    tela.fill(PRETO)  # limpa tela
    draw_text(mensagem, fonte_larga, cor, LARGURA/2, ALTURA/2, "center")  # desenha mensagem centralizada
    pygame.display.flip()  # atualiza tela
    
    # Em browser precisa usar time.sleep com cuidado
    if BROWSER_MODE:
        # Apenas exibe a mensagem, sem esperar
        pass
    else:
        time.sleep(duracao)  # espera alguns segundos

# === Estados do jogo ===
STATE_INTRO = 0  # tela de introdução
STATE_GAME = 1  # estado de jogo ativo
STATE_END_ROUND = 2  # fim de rodada
STATE_END_GAME = 3  # fim do jogo

# === Tela de introdução ===
async def intro_screen_async():
    tela.fill(PRETO)  # limpa tela com cor preta
    draw_text("QUIZ GAME", fonte_titulo, AMARELO, LARGURA/2, ALTURA/4, "center")  # título do jogo
    draw_text("Tente adivinhar a resposta com o mínimo de dicas possível!", fonte_media, BRANCO, LARGURA/2, ALTURA/2, "center")  # instruções
    draw_text("Clique na tela ou pressione Enter para começar", fonte_pequena, VERDE, LARGURA/2, ALTURA*3/4, "center")  # prompt iniciar
    
    # Mostrar informações de debug
    show_debug_info(tela)
    pygame.display.flip()  # aplica mudanças na tela
    
    debug_print("Tela de introdução exibida")
    
    # No browser, avança automaticamente após um curto período
    await asyncio.sleep(1.5)
    debug_print("Avançando da introdução automaticamente")

# === Função que executa uma rodada ===
async def game_round_async(dicas, resposta_certa, pontos_totais, num_rodada):
    i_dica = 0  # índice da dica atual
    i_chute = 0  # número de chutes feitos
    pontos_ganhos = 0  # pontos obtidos nesta rodada
    input_active = False  # estado da caixa de input
    input_text = ""  # texto digitado pelo jogador
    desistir_x, pedir_dica_x, enviar_x = 50, 250, 450  # posições horizontais dos botões
    largura_botao, altura_botao = 150, 40  # tamanho dos botões
    
    # Versão simplificada para web - apenas mostra a interface por algum tempo
    for i in range(3):  # Mostrar interface por alguns ciclos
        tela.fill(PRETO)  # limpa tela
        draw_text(f"RODADA {num_rodada}", fonte_larga, AZUL, LARGURA/2, 40, "center")  # mostra número da rodada
        draw_text(f"Palavra da rodada: {resposta_certa}", fonte_media, VERDE, LARGURA/2, 150, "center")  # DEBUG
        draw_text(f"Dica: {dicas[0]}", fonte_media, AMARELO, LARGURA/2, 200, "center")  # Mostra primeira dica
        
        # Desenhar botões simplificados
        pygame.draw.rect(tela, VERDE, (LARGURA/2 - 75, ALTURA - 100, 150, 50))
        draw_text("Continuar", fonte_media, PRETO, LARGURA/2, ALTURA - 75, "center")
        
        show_debug_info(tela)
        pygame.display.flip()
        await asyncio.sleep(1)  # Atualiza a cada segundo
    
    # Simula sucesso para fins de teste
    await show_message_async("PARABÉNS! VOCÊ ACERTOU!", VERDE, 1)
    return len(dicas), False  # Retorna pontuação máxima para teste

# === Tela de fim de jogo ===
async def end_game_screen_async(total_pontos):
    tela.fill(PRETO)  # limpa tela
    draw_text("O JOGO ACABOU!", fonte_titulo, VERMELHO, LARGURA/2, ALTURA/4, "center")  # mensagem final
    draw_text("MUITO OBRIGADO POR JOGAR!!!", fonte_media, VERMELHO, LARGURA/2, ALTURA/4 + 60, "center")  # agradecimento
    point_text = "PONTO" if total_pontos == 1 else "PONTOS"  # singular/plural
    draw_text("SUA PONTUAÇÃO TOTAL FOI DE", fonte_media, VERDE, LARGURA/2, ALTURA/2, "center")  # texto auxiliar
    draw_text(f"{total_pontos}", fonte_titulo, VERDE, LARGURA/2, ALTURA/2 + 60, "center")  # mostra total
    draw_text(point_text, fonte_media, VERDE, LARGURA/2, ALTURA/2 + 120, "center")  # mostra PONTO(S)
    show_debug_info(tela)
    pygame.display.flip()  # aplica mudanças
    
    await asyncio.sleep(3)  # Exibe por 3 segundos antes de encerrar

# === Função principal que inicia o jogo ===
async def main():
    debug_print("Iniciando função principal assíncrona")
    try:
        # Inicialização clara e direta
        debug_print("Início do jogo")
        tela.fill(PRETO)
        draw_text("Carregando jogo...", fonte_media, VERDE, LARGURA/2, ALTURA/2, "center")
        pygame.display.flip()
        await asyncio.sleep(0)
        
        total_pontos = 0
        
        # Tela de inicialização
        await intro_screen_async()
        
        # Primeira rodada (simplificada)
        resposta, dicas = jogos[0]
        debug_print(f"Iniciando rodada com palavra: {resposta}")
        
        pontos, _ = await game_round_async(dicas, resposta, total_pontos, 1)
        total_pontos += pontos
        debug_print(f"Pontos ganhos: {pontos}")
        
        # Exibe tela final
        await end_game_screen_async(total_pontos)
        
        debug_print("Jogo finalizado com sucesso")
        
    except Exception as e:
        # Captura e exibe qualquer erro
        debug_print(f"ERRO: {str(e)}")
        debug_print(f"Traceback: {traceback.format_exc()}")
        tela.fill(PRETO)
        draw_text("ERRO NO JOGO", fonte_larga, VERMELHO, LARGURA/2, ALTURA/3, "center")
        draw_text(str(e), fonte_media, VERMELHO, LARGURA/2, ALTURA/2, "center")
        pygame.display.flip()
        await asyncio.sleep(3)
    
    finally:
        debug_print("Finalizando o jogo")
        # Não encerramos o Pygame no navegador

# Ponto de entrada principal
if __name__ == "__main__":
    debug_print("Iniciando o programa")
    asyncio.run(main())