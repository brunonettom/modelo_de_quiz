import pygame
import sys
import asyncio

# Inicialização básica do pygame
pygame.init()

# Configurações simplificadas
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quiz Game - Simplificado")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Fonte simples
fonte = pygame.font.SysFont('Arial', 36) if pygame.font else None

# Função simplificada para desenhar texto
def desenhar_texto(texto, cor, x, y):
    if fonte:
        superficie = fonte.render(texto, True, cor)
        retangulo = superficie.get_rect(center=(x, y))
        tela.blit(superficie, retangulo)

# Função principal assíncrona
async def main():
    executando = True
    contador = 0
    clock = pygame.time.Clock()
    
    while executando:
        # Limpa a tela
        tela.fill(PRETO)
        
        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
        
        # Desenha algo simples
        desenhar_texto(f"Quiz Game - Contador: {contador}", BRANCO, LARGURA//2, ALTURA//4)
        desenhar_texto("Clique para iniciar o jogo", VERDE, LARGURA//2, ALTURA//2)
        
        # Atualiza o contador
        contador += 1
        
        # Atualiza a tela
        pygame.display.flip()
        
        # Essencial para Pygbag - permite que o navegador processe eventos
        await asyncio.sleep(0)
        
        # Limita a taxa de quadros
        clock.tick(30)
    
    # Finalização
    pygame.quit()
    sys.exit()

# Inicialização padrão para Pygbag
if __name__ == "__main__":
    asyncio.run(main())