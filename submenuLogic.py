import pygame
import utilities

def loadGameSubmenu(gameType, SCREEN, WIDTH, HEIGHT):
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 550, 200)
    
    # Crear botones
    button_width = 150
    button_height = 50
    button_spacing = 50
    
    # Calcular posiciones de los botones
    button_y = submenuRect.centery + 20
    si_button = pygame.Rect(
        submenuRect.centerx - button_width - button_spacing//2,
        button_y,
        button_width,
        button_height
    )
    no_button = pygame.Rect(
        submenuRect.centerx + button_spacing//2,
        button_y,
        button_width,
        button_height
    )
    
    # Colores de los botones
    buttonColors = {
        "SI": (66, 159, 121),    # Verde
        "NO": (245, 77, 64)      # Rojo
    }
    
    # Fuente para el texto
    font = utilities.getMainFontBold(24)
    title_font = utilities.getMainFontBold(32)
    
    while running:   
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenu(submenuRect, background, blurSurface, SCREEN)
        
        # Dibujar texto
        title_text = f"Hay un juego guardado de {gameType.capitalize()}"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(submenuRect.centerx, submenuRect.centery - 50))
        SCREEN.blit(title_surface, title_rect)
        
        subtitle_text = "¿Deseas cargarlo?"
        subtitle_surface = font.render(subtitle_text, True, (255, 255, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(submenuRect.centerx, submenuRect.centery - 15))
        SCREEN.blit(subtitle_surface, subtitle_rect)
        
        # Dibujar botones
        for text, button in [("SI", si_button), ("NO", no_button)]:
            # Crear sombra del botón
            shadow_button = pygame.Rect(button.x, button.y + 3, button.width, button.height)
            # Dibujar sombra del botón
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Dibujar rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], button, border_radius=10)
            # Texto
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            SCREEN.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
                    return None
                elif si_button.collidepoint(MOUSE_POS):
                    utilities.pressButton(si_button, buttonColors["SI"], SCREEN, font, "SI")
                    return True
                elif no_button.collidepoint(MOUSE_POS):
                    utilities.pressButton(no_button, buttonColors["NO"], SCREEN, font, "NO")
                    return False
        pygame.display.flip()
    
    return None
    