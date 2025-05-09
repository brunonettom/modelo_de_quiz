import pygame  # importa a biblioteca pygame para criação de jogos e interfaces gráficas
import pygame.freetype  # importa o módulo freetype do pygame para renderizar fontes
import sys  # importa o módulo sys para interagir com o sistema (encerrar o programa)
import time  # importa o módulo time para controlar delays e temporizações
import unicodedata  # importa o módulo unicodedata para normalização de textos
import os  # importa o módulo os para manipulação de caminho de arquivos e diretórios

# Inicializa todos os módulos do pygame
pygame.init()  # inicia o pygame, preparando os módulos internos para uso

# Obtém informações da tela (resolução atual)
info_tela = pygame.display.Info()  # pega objeto com dados da tela
LARGURA, ALTURA = int(info_tela.current_w * 0.9), int(info_tela.current_h * 0.9)  # define largura e altura da janela como 90% da resolução
# Configura a janela em modo normal (não fullscreen) mas com tamanho próximo à tela
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)  # cria janela dimensionada e redimensionável
# Centraliza a janela na tela
os.environ['SDL_VIDEO_CENTERED'] = '1'  # configura ambiente para centralizar janela

# Atualiza largura e altura após criar a janela
LARGURA, ALTURA = tela.get_size()  # redefine largura e altura com base no tamanho real da tela

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
fonte_pequena = pygame.freetype.SysFont("Arial", 20)  # fonte Arial tamanho 20
fonte_media = pygame.freetype.SysFont("Arial", 28)  # fonte Arial tamanho 28
fonte_larga = pygame.freetype.SysFont("Arial", 36)  # fonte Arial tamanho 36
fonte_titulo = pygame.freetype.SysFont("Arial", 48)  # fonte Arial tamanho 48

# === 1) Placeholder para dicas em imagem ===
imagem_placeholder = pygame.Surface((200, 120))  # cria superfície cinza para placeholder
imagem_placeholder.fill(CINZA)  # preenche a superfície com cor cinza
pygame.draw.rect(imagem_placeholder, PRETO, imagem_placeholder.get_rect(), 2)  # contorna o retângulo em preto
texto_surf, texto_rect = fonte_pequena.render("Imagem Aqui", PRETO)  # renderiza texto para placeholder
texto_rect.center = imagem_placeholder.get_rect().center  # centraliza o texto na superfície
imagem_placeholder.blit(texto_surf, texto_rect)  # desenha o texto na superfície

# Carrega uma imagem real de dica
imagem_dna = pygame.image.load(os.path.join('jogo-genetico', 'img', 'dna.png')).convert_alpha()  # carrega PNG com canal alpha
imagem_dna = pygame.transform.smoothscale(imagem_dna, (500, 120 * 500 / 200))  # redimensiona suavemente a imagem

# Dados de exemplo para as rodadas (palavra certa e lista de dicas)
jogos = [  # lista de jogos, cada um é [resposta, [dica1, dica2, ...]]
    ["python", ["É uma linguagem de programação", "Tem o nome de um animal", imagem_dna]],
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
    superficie_texto, rect_texto = fonte.render(texto, cor)  # renderiza texto em superfície
    if alinhar == "center":
        rect_texto.center = (x, y)  # centraliza horizontal e verticalmente
    elif alinhar == "right":
        rect_texto.right, rect_texto.top = x, y  # alinha à direita
    else:  # left
        rect_texto.left, rect_texto.top = x, y  # alinha à esquerda
    tela.blit(superficie_texto, rect_texto)  # desenha na tela
    return rect_texto  # retorna rect para possíveis usos

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
def show_message(mensagem, cor=AMARELO, duracao=1.5):
    tela.fill(PRETO)  # limpa tela
    draw_text(mensagem, fonte_larga, cor, LARGURA/2, ALTURA/2, "center")  # desenha mensagem centralizada
    pygame.display.flip()  # atualiza tela
    time.sleep(duracao)  # espera alguns segundos

# === Estados do jogo ===
STATE_INTRO = 0  # tela de introdução
STATE_GAME = 1  # estado de jogo ativo
STATE_END_ROUND = 2  # fim de rodada
STATE_END_GAME = 3  # fim do jogo

# === Tela de introdução ===
def intro_screen():
    tela.fill(PRETO)  # limpa tela com cor preta
    draw_text("QUIZ GAME", fonte_titulo, AMARELO, LARGURA/2, ALTURA/4, "center")  # título do jogo
    draw_text("Tente adivinhar a resposta com o mínimo de dicas possível!", fonte_media, BRANCO, LARGURA/2, ALTURA/2, "center")  # instruções
    draw_text("Pressione qualquer tecla para começar", fonte_pequena, VERDE, LARGURA/2, ALTURA*3/4, "center")  # prompt iniciar
    pygame.display.flip()  # aplica mudanças na tela
    esperando = True
    while esperando:
        for evento in pygame.event.get():  # itera eventos
            if evento.type == pygame.QUIT:  # se clicar fechar
                pygame.quit()  # encerra pygame
                sys.exit()  # encerra programa
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # somente se for a tecla Enter
                    esperando = False  # sai da espera

# === Função que executa uma rodada ===
def game_round(dicas, resposta_certa, pontos_totais, num_rodada):
    i_dica = 0  # índice da dica atual
    i_chute = 0  # número de chutes feitos
    pontos_ganhos = 0  # pontos obtidos nesta rodada
    input_active = False  # estado da caixa de input
    input_text = ""  # texto digitado pelo jogador
    desistir_x, pedir_dica_x, enviar_x = 50, 250, 450  # posições horizontais dos botões
    largura_botao, altura_botao = 150, 40  # tamanho dos botões
    running = True  # controle do loop da rodada
    mouse_clicked_last_frame = False  # estado anterior do clique
    while running:
        tela.fill(PRETO)  # limpa tela
        draw_text(f"RODADA {num_rodada}", fonte_larga, AZUL, LARGURA/2, 40, "center")  # mostra número da rodada
        # preparação para desenhar dicas em colunas
        cols_x = [50, LARGURA//2 + 20]  # posições iniciais X para colunas
        col_y = [100, 100]  # posições iniciais Y para colunas
        limite_inferior = ALTURA - 200  # limite para quebra de coluna
        draw_text("Suas dicas até agora:", fonte_media, AMARELO, cols_x[0], col_y[0])  # título dicas
        col_y[0] += fonte_media.get_sized_height() + 10  # avança Y após título
        for idx in range(i_dica):  # para cada dica disponível
            dica = dicas[idx]  # obtém dica da lista
            altura_dica = dica.get_height() if isinstance(dica, pygame.Surface) else fonte_pequena.get_sized_height()  # calcula altura da dica
            coluna = 0 if col_y[0] + altura_dica <= limite_inferior else 1  # escolhe coluna
            x = cols_x[coluna]  # define X
            y = col_y[coluna]  # define Y
            if isinstance(dica, pygame.Surface):
                tela.blit(dica, (x, y))  # desenha imagem
            else:
                draw_text(f"Dica {idx+1}: {dica}", fonte_pequena, AMARELO, x, y)  # desenha texto da dica
            col_y[coluna] += altura_dica + 10  # avança Y na coluna
        y_offset = max(col_y) + 20  # define espaço vertical após dicas
        pontos_possiveis = len(dicas) - i_dica + 1  # calcula pontos possíveis
        draw_text(f"Dicas restantes: {len(dicas)-i_dica}", fonte_pequena, AZUL, 50, y_offset)  # mostra dicas restantes
        draw_text(f"Pontos possíveis nesta rodada: {pontos_possiveis}", fonte_pequena, VERDE, 50, y_offset + 30)  # pontos possíveis
        draw_text(f"Total de pontos: {pontos_totais}", fonte_pequena, VERDE, 50, y_offset + 60)  # total acumulado
        draw_text(f"Qual é o seu {i_chute+1}° chute?", fonte_media, BRANCO, 50, y_offset + 100)  # prompt de chute
        draw_input_box(50, y_offset + 140, 400, 40, input_text, input_active)  # desenha caixa de input
        pos_mouse = pygame.mouse.get_pos()  # lê posição do mouse
        mouse_pressed = pygame.mouse.get_pressed()[0]  # lê estado do clique
        mouse_just_clicked = mouse_pressed and not mouse_clicked_last_frame  # detecta clique novo
        button_y = y_offset + 200  # posição vertical dos botões
        # botão Desistir
        desistir_hover = desistir_x <= pos_mouse[0] <= desistir_x + largura_botao and button_y <= pos_mouse[1] <= button_y + altura_botao
        pygame.draw.rect(tela, (255, 100, 100) if desistir_hover else VERMELHO, (desistir_x, button_y, largura_botao, altura_botao))
        draw_text("Desistir", fonte_media, PRETO, desistir_x + largura_botao/2, button_y + altura_botao/2, "center")
        # botão Pedir Dica
        if i_dica < len(dicas):
            dica_hover = pedir_dica_x <= pos_mouse[0] <= pedir_dica_x + largura_botao and  button_y <= pos_mouse[1] <= button_y + altura_botao
            pygame.draw.rect(tela, (255,255,100) if dica_hover else AMARELO, (pedir_dica_x, button_y, largura_botao, altura_botao))
            draw_text("Pedir Dica", fonte_media, PRETO, pedir_dica_x + largura_botao/2, button_y + altura_botao/2, "center")
        else:
            draw_text("Sem mais dicas!", fonte_pequena, VERMELHO, pedir_dica_x + largura_botao/2, button_y + altura_botao/2, "center")
            dica_hover = False
        # botão Enviar
        enviar_hover = enviar_x <= pos_mouse[0] <= enviar_x + largura_botao and button_y <= pos_mouse[1] <= button_y + altura_botao
        pygame.draw.rect(tela, (100,255,100) if enviar_hover else VERDE, (enviar_x, button_y, largura_botao, altura_botao))
        draw_text("Enviar", fonte_media, PRETO, enviar_x + largura_botao/2, button_y + altura_botao/2, "center")
        # trata cliques
        if mouse_just_clicked:
            if desistir_hover:
                show_message(f"A resposta correta era: {resposta_certa}", VERMELHO, 2)  # mostra resposta correta
                return 0, True  # retorna pontos 0 e desistiu=True
            elif dica_hover and i_dica < len(dicas):
                i_dica += 1  # revela próxima dica
            elif enviar_hover and input_text:
                if normalizar(input_text) == normalizar(resposta_certa):
                    pontos_ganhos = len(dicas) - i_dica + 1  # calcula pontos ganhos
                    show_message("PARABÉNS! VOCÊ ACERTOU!", VERDE, 2)  # mensagem de acerto
                    return pontos_ganhos, False  # retorna pontos e desistiu=False
                else:
                    show_message("Resposta incorreta, tente novamente!", VERMELHO, 1)  # mensagem de erro
                    i_chute += 1  # incrementa contador de chutes
                    input_text = ""  # limpa texto
        for evento in pygame.event.get():  # captura eventos
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()  # fecha jogo
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # ativa caixa de input se clicada
                if 50 <= evento.pos[0] <= 450 and y_offset + 140 <= evento.pos[1] <= y_offset + 180:
                    input_active = True
                else:
                    input_active = False
            if evento.type == pygame.KEYDOWN and input_active:
                if evento.key == pygame.K_RETURN:
                    # envia chute com Enter
                    if input_text:
                        if normalizar(input_text) == normalizar(resposta_certa):
                            pontos_ganhos = len(dicas) - i_dica + 1
                            show_message("PARABÉNS! VOCÊ ACERTOU!", VERDE, 2)
                            return pontos_ganhos, False
                        else:
                            show_message("Resposta incorreta, tente novamente!", VERMELHO, 1)
                            i_chute += 1
                            input_text = ""
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # remove última letra
                else:
                    input_text += evento.unicode  # adiciona caractere digitado
        pygame.display.flip()  # atualiza tela
        pygame.time.Clock().tick(30)  # limita a 30 FPS
        mouse_clicked_last_frame = mouse_pressed  # atualiza estado do clique

# === Tela de fim de jogo ===
def end_game_screen(total_pontos):
    tela.fill(PRETO)  # limpa tela
    draw_text("O JOGO ACABOU!", fonte_titulo, VERMELHO, LARGURA/2, ALTURA/4, "center")  # mensagem final
    draw_text("MUITO OBRIGADO POR JOGAR!!!", fonte_media, VERMELHO, LARGURA/2, ALTURA/4 + 60, "center")  # agradecimento
    point_text = "PONTO" if total_pontos == 1 else "PONTOS"  # singular/plural
    draw_text("SUA PONTUAÇÃO TOTAL FOI DE", fonte_media, VERDE, LARGURA/2, ALTURA/2, "center")  # texto auxiliar
    draw_text(f"{total_pontos}", fonte_titulo, VERDE, LARGURA/2, ALTURA/2 + 60, "center")  # mostra total
    draw_text(point_text, fonte_media, VERDE, LARGURA/2, ALTURA/2 + 120, "center")  # mostra PONTO(S)
    draw_text("Pressione qualquer tecla para sair", fonte_pequena, BRANCO, LARGURA/2, ALTURA*3/4 + 50, "center")  # prompt sair
    pygame.display.flip()  # aplica mudanças
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False

# === Pergunta para continuar jogando ===
def ask_continue():
    tela.fill(PRETO)  # limpa tela
    draw_text("Quer jogar outra rodada?", fonte_larga, BRANCO, LARGURA/2, ALTURA/3, "center")  # pergunta
    sim_x, sim_y = LARGURA/3 - 75, ALTURA/2  # posição botão Sim
    nao_x, nao_y = 2*LARGURA/3 - 75, ALTURA/2  # posição botão Não
    largura_botao, altura_botao = 150, 50  # tamanho botões
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if sim_x <= pos_mouse[0] <= sim_x + largura_botao and sim_y <= pos_mouse[1] <= sim_y + altura_botao:
                    return True  # jogador quer continuar
                elif nao_x <= pos_mouse[0] <= nao_x + largura_botao and nao_y <= pos_mouse[1] <= nao_y + altura_botao:
                    return False  # jogador não quer continuar
        tela.fill(PRETO)
        draw_text("Quer jogar outra rodada?", fonte_larga, BRANCO, LARGURA/2, ALTURA/3, "center")
        pos_mouse = pygame.mouse.get_pos()
        # desenha botão Sim com hover
        if sim_x <= pos_mouse[0] <= sim_x + largura_botao and sim_y <= pos_mouse[1] <= sim_y + altura_botao:
            pygame.draw.rect(tela, (100, 255, 100), (sim_x, sim_y, largura_botao, altura_botao))
        else:
            pygame.draw.rect(tela, VERDE, (sim_x, sim_y, largura_botao, altura_botao))
        draw_text("Sim", fonte_media, PRETO, sim_x + largura_botao/2, sim_y + altura_botao/2, "center")
        # desenha botão Não com hover
        if nao_x <= pos_mouse[0] <= nao_x + largura_botao and nao_y <= pos_mouse[1] <= nao_y + altura_botao:
            pygame.draw.rect(tela, (255, 100, 100), (nao_x, nao_y, largura_botao, altura_botao))
        else:
            pygame.draw.rect(tela, VERMELHO, (nao_x, nao_y, largura_botao, altura_botao))
        draw_text("Não", fonte_media, PRETO, nao_x + largura_botao/2, nao_y + altura_botao/2, "center")
        pygame.display.flip()
        pygame.time.Clock().tick(30)

# === Tela que mostra pontos da rodada ===
def show_points(pontos_rodada, total_pontos):
    tela.fill(PRETO)  # limpa tela
    draw_text("Você ganhou:", fonte_media, VERDE, LARGURA/2, ALTURA/3, "center")  # mensagem
    draw_text(f"{pontos_rodada}", fonte_titulo, VERDE, LARGURA/2, ALTURA/2, "center")  # mostra pontos
    ponto_texto = "ponto nessa rodada" if pontos_rodada == 1 else "pontos nessa rodada"  # singular/plural texto
    draw_text(ponto_texto, fonte_media, VERDE, LARGURA/2, ALTURA/2 + 60, "center")  # texto auxiliar
    total_text = f"Você tem o total de {total_pontos} ponto" if total_pontos == 1 else f"Você tem o total de {total_pontos} pontos"  # total
    draw_text(total_text, fonte_media, VERDE, LARGURA/2, ALTURA*3/4, "center")  # mostra total
    draw_text("Pressione qualquer tecla para continuar", fonte_pequena, BRANCO, LARGURA/2, ALTURA*3/4 + 50, "center")  # prompt
    pygame.display.flip()  # aplica mudanças
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False

# === Função principal que inicia o jogo ===
def main():
    total_pontos = 0  # pontuação acumulada
    num_rodada = 0  # índice da rodada
    intro_screen()  # exibe tela de introdução
    for jogo_atual in jogos:  # itera pelos jogos definidos
        num_rodada += 1  # incrementa número da rodada
        resposta, dicas = jogo_atual  # desempacota resposta e dicas
        pontos_ganhos, desistiu = game_round(dicas, resposta, total_pontos, num_rodada)  # executa rodada
        total_pontos += pontos_ganhos  # atualiza pontuação total
        show_points(pontos_ganhos, total_pontos)  # mostra pontos ganhos
        if num_rodada < len(jogos) and not ask_continue():  # verifica continuidade
            break  # encerra loop se jogador não quiser continuar
    end_game_screen(total_pontos)  # exibe tela final
    pygame.quit()  # encerra pygame
    sys.exit()  # encerra programa

if __name__ == "__main__":
    main()  # executa função principal se arquivo for executado diretamente