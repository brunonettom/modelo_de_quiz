import pygame
import sys
import asyncio
import time
import unicodedata
import os

# Inicialização básica do pygame
pygame.init()

# Configurações simplificadas
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quiz Game")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 50, 50)
VERDE = (50, 255, 50)
AZUL = (50, 50, 255)
AMARELO = (255, 255, 50)
CINZA = (200, 200, 200)

# Fonte simplificada usando SysFont ao invés de freetype
fonte_pequena = pygame.font.SysFont("Arial", 20)
fonte_media = pygame.font.SysFont("Arial", 28)
fonte_larga = pygame.font.SysFont("Arial", 36)
fonte_titulo = pygame.font.SysFont("Arial", 48)

# Placeholder para imagens
imagem_placeholder = pygame.Surface((200, 120))
imagem_placeholder.fill(CINZA)
pygame.draw.rect(imagem_placeholder, PRETO, imagem_placeholder.get_rect(), 2)
superficie_texto = fonte_pequena.render("Imagem Aqui", True, PRETO)
rect_texto = superficie_texto.get_rect(center=imagem_placeholder.get_rect().center)
imagem_placeholder.blit(superficie_texto, rect_texto)

# Carrega a imagem DNA com tratamento de erro para compatibilidade com Pygbag
try:
    # Tenta carregar a imagem para ambiente web e desktop
    if sys.platform == 'emscripten':
        imagem_dna = pygame.image.load('img/dna.png').convert_alpha()
    else:
        imagem_dna = pygame.image.load(os.path.join('jogo-genetico', 'img', 'dna.png')).convert_alpha()
    # Reduzindo o tamanho da imagem para 200x120 pixels
    imagem_dna = pygame.transform.smoothscale(imagem_dna, (200, 120))
except Exception as e:
    print(f"Erro ao carregar imagem: {e}")
    # Use placeholder se falhar
    imagem_dna = imagem_placeholder

# Dados de exemplo para as rodadas com a imagem na terceira dica do primeiro jogo
jogos = [
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

# === Função simplificada para desenhar texto ===
def draw_text(texto, fonte, cor, x, y, alinhar="left"):
    superficie_texto = fonte.render(texto, True, cor)
    rect_texto = superficie_texto.get_rect()
    if alinhar == "center":
        rect_texto.center = (x, y)
    elif alinhar == "right":
        rect_texto.right, rect_texto.top = x, y
    else:  # left
        rect_texto.left, rect_texto.top = x, y
    tela.blit(superficie_texto, rect_texto)
    return rect_texto

# === Função para desenhar caixa de input ===
def draw_input_box(x, y, largura_caixa, altura_caixa, texto, ativo):
    cor_borda = VERMELHO if ativo else CINZA
    pygame.draw.rect(tela, cor_borda, (x, y, largura_caixa, altura_caixa), 2)
    superficie_texto = fonte_media.render(texto, True, BRANCO)
    rect_texto = superficie_texto.get_rect(left=x+5, centery=y+altura_caixa//2)
    tela.blit(superficie_texto, rect_texto)

# === Função para mostrar mensagem temporária ===
async def show_message(mensagem, cor=AMARELO, duracao=1.5):
    tela.fill(PRETO)
    draw_text(mensagem, fonte_larga, cor, LARGURA/2, ALTURA/2, "center")
    pygame.display.flip()
    
    # Abordagem não-bloqueante para aguardar
    for i in range(int(duracao * 10)):  # 10 frames por segundo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        await asyncio.sleep(0.1)

# === Tela de introdução simplificada ===
async def intro_screen():
    clock = pygame.time.Clock()
    esperando = True
    
    while esperando:
        tela.fill(PRETO)
        draw_text("QUIZ GAME", fonte_titulo, AMARELO, LARGURA/2, ALTURA/4, "center")
        draw_text("Tente adivinhar a resposta com o mínimo de dicas possível!", fonte_media, BRANCO, LARGURA/2, ALTURA/2, "center")
        draw_text("Pressione ENTER para começar", fonte_pequena, VERDE, LARGURA/2, ALTURA*3/4, "center")
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False
        
        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)

# === Função que executa uma rodada ===
async def game_round(dicas, resposta_certa, pontos_totais, num_rodada):
    i_dica = 0  # índice da dica atual
    i_chute = 0  # número de chutes feitos
    pontos_ganhos = 0  # pontos obtidos nesta rodada
    input_active = False  # estado da caixa de input
    input_text = ""  # texto digitado pelo jogador
    desistir_x, pedir_dica_x, enviar_x = 50, 250, 450  # posições horizontais dos botões
    largura_botao, altura_botao = 150, 40  # tamanho dos botões
    running = True  # controle do loop da rodada
    mouse_clicked_last_frame = False  # estado anterior do clique
    clock = pygame.time.Clock()
    
    while running:
        tela.fill(PRETO)
        draw_text(f"RODADA {num_rodada}", fonte_larga, AZUL, LARGURA/2, 50, "center")
        
        # Desenha dicas disponíveis
        draw_text("Suas dicas até agora:", fonte_media, AMARELO, 50, 80)
        y_pos = 110
        for idx in range(i_dica):
            dica = dicas[idx]
            if isinstance(dica, pygame.Surface):
                # Se a dica for uma imagem, desenha a imagem
                tela.blit(dica, (50, y_pos))
                y_pos += dica.get_height() + 10
            else:
                # Se a dica for um texto, desenha o texto
                draw_text(f"Dica {idx+1}: {dica}", fonte_pequena, AMARELO, 50, y_pos)
                y_pos += fonte_pequena.get_height() + 10
        
        # Informações da rodada
        draw_text(f"Dicas restantes: {len(dicas)-i_dica}", fonte_pequena, AZUL, 50, y_pos + 20)
        draw_text(f"Pontos possíveis nesta rodada: {len(dicas)-i_dica+1}", fonte_pequena, VERDE, 50, y_pos + 50)
        draw_text(f"Total de pontos: {pontos_totais}", fonte_pequena, VERDE, 50, y_pos + 80)
        
        # Campo de resposta
        draw_text("Digite sua resposta:", fonte_media, BRANCO, 50, y_pos + 120)
        draw_input_box(50, y_pos + 150, 400, 40, input_text, input_active)
        
        # Botões
        pygame.draw.rect(tela, VERMELHO, (50, y_pos + 220, 150, 40))
        draw_text("Desistir", fonte_media, PRETO, 50+75, y_pos+220+20, "center")
        
        if i_dica < len(dicas):
            pygame.draw.rect(tela, AMARELO, (250, y_pos + 220, 150, 40))
            draw_text("Pedir Dica", fonte_media, PRETO, 250+75, y_pos+220+20, "center")
        
        pygame.draw.rect(tela, VERDE, (450, y_pos + 220, 150, 40))
        draw_text("Enviar", fonte_media, PRETO, 450+75, y_pos+220+20, "center")
        
        # Captura estado do mouse
        pos_mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_just_clicked = mouse_pressed and not mouse_clicked_last_frame
        
        # Detecta hover nos botões
        desistir_hover = 50 <= pos_mouse[0] <= 50+150 and y_pos+220 <= pos_mouse[1] <= y_pos+220+40
        dica_hover = 250 <= pos_mouse[0] <= 250+150 and y_pos+220 <= pos_mouse[1] <= y_pos+220+40 and i_dica < len(dicas)
        enviar_hover = 450 <= pos_mouse[0] <= 450+150 and y_pos+220 <= pos_mouse[1] <= y_pos+220+40
        
        # Processar cliques nos botões
        if mouse_just_clicked:
            if desistir_hover:
                await show_message(f"A resposta correta era: {resposta_certa}", VERMELHO, 2)
                return 0, True
            elif dica_hover and i_dica < len(dicas):
                i_dica += 1
            elif enviar_hover and input_text:
                if normalizar(input_text) == normalizar(resposta_certa):
                    pontos_ganhos = len(dicas) - i_dica + 1
                    await show_message("PARABÉNS! VOCÊ ACERTOU!", VERDE, 2)
                    return pontos_ganhos, False
                else:
                    await show_message("Resposta incorreta, tente novamente!", VERMELHO, 1)
                    i_chute += 1
                    input_text = ""
        
        # Processar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clique na caixa de input
                if 50 <= evento.pos[0] <= 450 and y_pos+150 <= evento.pos[1] <= y_pos+190:
                    input_active = True
                else:
                    input_active = False
            elif evento.type == pygame.KEYDOWN and input_active:
                if evento.key == pygame.K_RETURN:
                    if input_text and normalizar(input_text) == normalizar(resposta_certa):
                        pontos_ganhos = len(dicas) - i_dica + 1
                        await show_message("PARABÉNS! VOCÊ ACERTOU!", VERDE, 2)
                        return pontos_ganhos, False
                    elif input_text:
                        await show_message("Resposta incorreta, tente novamente!", VERMELHO, 1)
                        i_chute += 1
                        input_text = ""
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += evento.unicode
        
        pygame.display.flip()
        clock.tick(30)
        mouse_clicked_last_frame = mouse_pressed
        await asyncio.sleep(0)
    
    return 0, False

# === Pergunta para continuar jogando ===
async def ask_continue():
    clock = pygame.time.Clock()
    tela.fill(PRETO)
    draw_text("Quer jogar outra rodada?", fonte_larga, BRANCO, LARGURA/2, ALTURA/3, "center")
    
    pygame.draw.rect(tela, VERDE, (LARGURA/3-75, ALTURA/2, 150, 50))
    draw_text("Sim", fonte_media, PRETO, LARGURA/3, ALTURA/2+25, "center")
    
    pygame.draw.rect(tela, VERMELHO, (2*LARGURA/3-75, ALTURA/2, 150, 50))
    draw_text("Não", fonte_media, PRETO, 2*LARGURA/3, ALTURA/2+25, "center")
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if LARGURA/3-75 <= pos[0] <= LARGURA/3+75 and ALTURA/2 <= pos[1] <= ALTURA/2+50:
                    return True
                elif 2*LARGURA/3-75 <= pos[0] <= 2*LARGURA/3+75 and ALTURA/2 <= pos[1] <= ALTURA/2+50:
                    return False
        clock.tick(30)
        await asyncio.sleep(0)
    return True

# === Tela que mostra pontos da rodada ===
async def show_points(pontos_rodada, total_pontos):
    clock = pygame.time.Clock()
    tela.fill(PRETO)
    draw_text("Você ganhou:", fonte_media, VERDE, LARGURA/2, ALTURA/3, "center")
    draw_text(f"{pontos_rodada}", fonte_titulo, VERDE, LARGURA/2, ALTURA/2, "center")
    
    ponto_texto = "ponto nessa rodada" if pontos_rodada == 1 else "pontos nessa rodada"
    draw_text(ponto_texto, fonte_media, VERDE, LARGURA/2, ALTURA/2+60, "center")
    
    total_text = f"Você tem o total de {total_pontos} ponto" if total_pontos == 1 else f"Você tem o total de {total_pontos} pontos"
    draw_text(total_text, fonte_media, VERDE, LARGURA/2, ALTURA*3/4, "center")
    draw_text("Pressione qualquer tecla para continuar", fonte_pequena, BRANCO, LARGURA/2, ALTURA*3/4+50, "center")
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False
        clock.tick(30)
        await asyncio.sleep(0)

# === Tela de fim de jogo ===
async def end_game_screen(total_pontos):
    clock = pygame.time.Clock()
    tela.fill(PRETO)
    draw_text("O JOGO ACABOU!", fonte_titulo, VERMELHO, LARGURA/2, ALTURA/4, "center")
    draw_text("MUITO OBRIGADO POR JOGAR!!!", fonte_media, VERMELHO, LARGURA/2, ALTURA/4+60, "center")
    
    point_text = "PONTO" if total_pontos == 1 else "PONTOS"
    draw_text("SUA PONTUAÇÃO TOTAL FOI DE", fonte_media, VERDE, LARGURA/2, ALTURA/2, "center")
    draw_text(f"{total_pontos}", fonte_titulo, VERDE, LARGURA/2, ALTURA/2+60, "center")
    draw_text(point_text, fonte_media, VERDE, LARGURA/2, ALTURA/2+120, "center")
    
    draw_text("Pressione qualquer tecla para sair", fonte_pequena, BRANCO, LARGURA/2, ALTURA*3/4+50, "center")
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False
        clock.tick(30)
        await asyncio.sleep(0)

# === Função principal que inicia o jogo ===
async def main():
    total_pontos = 0
    num_rodada = 0
    await intro_screen()
    
    for jogo_atual in jogos:
        num_rodada += 1
        resposta, dicas = jogo_atual
        pontos_ganhos, desistiu = await game_round(dicas, resposta, total_pontos, num_rodada)
        total_pontos += pontos_ganhos
        await show_points(pontos_ganhos, total_pontos)
        if num_rodada < len(jogos) and not await ask_continue():
            break
    
    await end_game_screen(total_pontos)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())