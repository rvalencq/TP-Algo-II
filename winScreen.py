import pygame
import utilities

WIDTH = 1280
HEIGHT = 720
GREEN = (66, 159, 121)

def showWinScreen(SCREEN):
    # Crear superficie para el desenfoque
    # Aplicar efecto de desenfoque (simulado con un rectángulo semitransparente)
    blurSurface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blurSurface.fill((0, 0, 0, 128))  # Negro semitransparente para simular desenfoque
    
    # Crear superficie para el texto
    text_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    font = utilities.getMainFontBold(72)
    text = font.render("¡HAS GANADO!", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    # Variables para el fade
    alpha = 0
    fade_in = True
    fade_speed = 2
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        
        # Dibujar fondo con desenfoque
        SCREEN.blit(blurSurface, (0, 0))
        
        # Actualizar alpha para el fade
        if fade_in:
            alpha = min(alpha + fade_speed, 255)
            if alpha >= 255:
                fade_in = False
        else:
            alpha = max(alpha - fade_speed, 0)
            if alpha <= 0:
                fade_in = True
        
        # Dibujar texto con fade
        text_surface.fill((0, 0, 0, 0))
        text_surface.blit(text, text_rect)
        text_surface.set_alpha(alpha)
        SCREEN.blit(text_surface, (0, 0))
        
        pygame.display.flip()
        pygame.time.delay(16)  # Aproximadamente 60 FPS
