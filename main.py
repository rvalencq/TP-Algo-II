import pygame
import utilities
import userLogic
import lexireto
import letras

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = utilities.getDefaultScreen()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Words: THE GAME")
logIn = False

# Crear fuente para el texto
FONT = utilities.getMainFontBold(40)

# Colores
WHITE = utilities.getColor("WHITE")
BLACK = utilities.getColor("BLACK")
BLUE = utilities.getColor("BLUE")
RED = utilities.getColor("RED")
GRAY = utilities.getColor("GRAY")
GREEN = utilities.getColor("GREEN")

# Cargar imagen de fondo
redBG = utilities.getBG("MENU")
greenBG = utilities.getBG("GAME")
titleImage = pygame.image.load("assets/title.png")
titleImage = pygame.transform.scale(titleImage, (WIDTH, HEIGHT))

def firstScreen():
    running = True
    # Variables para la animación del texto
    alpha = 0
    fade_speed = 255 / 60  # Velocidad para completar en 2 segundos
    increasing = True
    
    # Primero ejecutar la animación
    utilities.animateTitle(SCREEN, redBG, WIDTH, HEIGHT, titleImage)
    # Crear y animar el texto "presione un boton"
    textSurface = FONT.render("CLIC PARA EMPEZAR", True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(WIDTH//2, HEIGHT//2 + 200))
    
    # Después de la animación, permitir interacción
    while running:
        # Dibujar fondo y título
        SCREEN.blit(redBG, (0, 0))
        SCREEN.blit(titleImage, (0, -50))
        
        # Dibujar texto con su opacidad
        textSurface.set_alpha(alpha)
        SCREEN.blit(textSurface, textRect)

        if increasing:
            alpha += fade_speed
            if alpha >= 255:
                increasing = False
        else:
            alpha -= fade_speed
            if alpha <= 50:
                increasing = True
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if userLogic.loginMenu(SCREEN, WIDTH, HEIGHT):
                    running = False
                    mainMenu()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def mainMenu():
    running = True
    selectedGame = None
    selectedDifficulty = None
    delayMenus = 0
    
    user = utilities.getUserLoggedIn()
    # Rectángulo central 
    centerRect = pygame.Rect(WIDTH//2 - 225, int(HEIGHT*0.7), 450, 150)
    shadowRect = pygame.Rect(centerRect.x, centerRect.y + 5, centerRect.width, centerRect.height)
    # Rectangulo secundario
    secondaryRect = pygame.Rect(centerRect.x + centerRect.width + 20, int(HEIGHT*0.7), 150, 150)
    secondaryShadowRect = pygame.Rect(secondaryRect.x, secondaryRect.y + 5, secondaryRect.width, secondaryRect.height)
    # Rectangulo User
    userRect = pygame.Rect(centerRect.x - 20 - 150, int(HEIGHT*0.7), 150, 150)
    userShadowRect = pygame.Rect(userRect.x, userRect.y + 5, userRect.width, userRect.height)

    # Diccionario de botones con sus rectángulos
    mainMenuButtons = {
        "JUGAR": pygame.Rect(centerRect.centerx - 100, centerRect.centery - 50, 200, 100),  # Centrado en el rectángulo
        "REGLAS": pygame.Rect(secondaryRect.x + 10, secondaryRect.y + 15, secondaryRect.width - 20, 60),  # 10px de margen
        "SALIR": pygame.Rect(secondaryRect.x + 10, secondaryRect.y + 15 + 60 + 5, secondaryRect.width - 20, 60),   # 10px de margen + altura del botón Salir + 5px de separación
        "P1": pygame.Rect(userRect.x + 10, userRect.y + 5 + 60 + 5, userRect.width - 20, 60)   # 10px de margen + altura del botón Salir + 5px de separación
    }

    # Diccionario de colores para cada botón
    buttonColors = {
        "JUGAR": BLUE,   
        "REGLAS": (66, 159, 121),    
        "SALIR": RED,
        "P1": GRAY
    }

    profileText = utilities.getMainFontBold(32).render("Profile", True, (255, 255, 255))
    profileRect = profileText.get_rect(center=(userRect.centerx, userRect.y + 40))  # Centrado en el rectángulo de usuario, 30px desde arriba

    while running:
        SCREEN.blit(redBG, (0, -0))  # Dibujar el fondo rojo
        SCREEN.blit(titleImage, (0, -50))
        MOUSE_POS = pygame.mouse.get_pos()

        # Forma central y sombra
        pygame.draw.rect(SCREEN, (30, 40, 42), shadowRect, border_radius=20)  # Color más oscuro para la sombra
        pygame.draw.rect(SCREEN, (58, 80, 84), centerRect, border_radius=20)  # Color gris oscuro
        pygame.draw.rect(SCREEN, (30, 40, 42), secondaryShadowRect, border_radius=20)  # Color más oscuro para la sombra
        pygame.draw.rect(SCREEN, (58, 80, 84), secondaryRect, border_radius=20)  # Color gris oscuro
        pygame.draw.rect(SCREEN, (30, 40, 42), userShadowRect, border_radius=20)  # Color más oscuro para la sombra
        pygame.draw.rect(SCREEN, (58, 80, 84), userRect, border_radius=20)  # Color gris oscuro

        # Dibujar texto del título
        SCREEN.blit(profileText, profileRect)

        # Dibujar botones y texto
        for text, rect in mainMenuButtons.items():
            # Crear sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            # Dibujar sombra del botón
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Dibujar rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], rect, border_radius=10)
            
            # Renderizar texto
            text_surface = FONT.render(text, True, (255, 255, 255))  # Texto blanco para mejor contraste
            text_rect = text_surface.get_rect(center=rect.center)
            
            # Dibujar texto
            SCREEN.blit(text_surface, text_rect)
        
        if selectedGame and selectedDifficulty:
            if delayMenus == 15:
                delayMenus += 1
                if utilities.hasSavedGame(user, selectedGame):
                    loadGameChoice = loadGameSubmenu(selectedGame, SCREEN, WIDTH, HEIGHT)
                    if loadGameChoice is None:  # Si el usuario sale del submenú
                        selectedGame = None
                        selectedDifficulty = None
                        delayMenus = 0
                    elif loadGameChoice:  # Si el usuario elige cargar
                        if selectedGame == "LEXIRETO":
                            lexireto.lexiretoGame(SCREEN, greenBG, user, True)
                        else:  # LETRAS
                            letras.letrasGame(SCREEN, greenBG, user, True)
                    else:  # Si el usuario elige no cargar
                        if selectedGame == "LEXIRETO":
                            lexireto.lexiretoGame(SCREEN, greenBG, user, False, selectedDifficulty)
                        else:  # LETRAS
                            letras.letrasGame(SCREEN, greenBG, user, False, selectedDifficulty)
                else:
                    if selectedGame == "LEXIRETO":
                        lexireto.lexiretoGame(SCREEN, greenBG, user, False, selectedDifficulty)
                    else:  # LETRAS
                        letras.letrasGame(SCREEN, greenBG, user, False, selectedDifficulty)
                selectedGame = None
                selectedDifficulty = None
                delayMenus += 1
            else:
                delayMenus += 1

        if delayMenus > 15:
            delayMenus = 0
            selectedGame = None
            selectedDifficulty = None
        
        # Actualizar pantalla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mainMenuButtons["SALIR"].collidepoint(MOUSE_POS):
                    utilities.pressButton(mainMenuButtons["SALIR"], buttonColors["SALIR"], SCREEN, FONT, "SALIR")
                    pygame.quit()
                    exit()
                elif mainMenuButtons["JUGAR"].collidepoint(MOUSE_POS):
                    utilities.pressButton(mainMenuButtons["JUGAR"], buttonColors["JUGAR"], SCREEN, FONT, "JUGAR")
                    selectedGame, selectedDifficulty = gameSelectMenu()

                elif mainMenuButtons["REGLAS"].collidepoint(MOUSE_POS):
                    utilities.pressButton(mainMenuButtons["REGLAS"], buttonColors["REGLAS"], SCREEN, FONT, "REGLAS")
                    rules()
                elif mainMenuButtons["P1"].collidepoint(MOUSE_POS):
                    utilities.pressButton(mainMenuButtons["P1"], buttonColors["P1"], SCREEN, FONT, "P1")
                    profileMenu()

        pygame.display.flip()

    pygame.quit()

def profileMenu():
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 600, 550)
    
    # Crear fuentes para el texto
    titleFont = utilities.getMainFontBold(32)
    statsFont = utilities.getMainFontBold(24)
    
    # Obtener usuario actual
    user = utilities.getUserLoggedIn()
    
    # Obtener estadísticas
    letras_stats = utilities.getStats(user, 'letras')
    lexireto_stats = utilities.getStats(user, 'lexireto')
    
    while running:   
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenu(submenuRect, background, blurSurface, SCREEN)
        
        # Dibujar título
        titleSurface = titleFont.render(f"PERFIL DE {user.upper()}", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(submenuRect.centerx, submenuRect.y + 40))
        SCREEN.blit(titleSurface, titleRect)
        
        # Dibujar estadísticas de Letras
        letras_title = statsFont.render("LETRAS:", True, (255, 255, 255))
        letras_rect = letras_title.get_rect(center=(submenuRect.centerx, submenuRect.y + 100))
        SCREEN.blit(letras_title, letras_rect)
        
        y_offset = submenuRect.y + 140
        if letras_stats:
            stats = [
                f"Palabras acertadas: {letras_stats['palabras_acertadas']}",
                f"Victorias: {letras_stats['victorias']}",
                f"Tiempo jugado: {utilities.formatTime(letras_stats['tiempo_jugado'])}",
                f"Tiempo promedio por victoria: {utilities.formatTime(int(letras_stats['tiempo_promedio_victoria']))}"
            ]
            for stat in stats:
                text_surface = statsFont.render(stat, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(submenuRect.centerx, y_offset))
                SCREEN.blit(text_surface, text_rect)
                y_offset += 35
        
        # Dibujar estadísticas de Lexireto
        lexireto_title = statsFont.render("LEXIRETO:", True, (255, 255, 255))
        lexireto_rect = lexireto_title.get_rect(center=(submenuRect.centerx, y_offset + 20))
        SCREEN.blit(lexireto_title, lexireto_rect)
        
        y_offset += 60
        if lexireto_stats:
            stats = [
                f"Palabras acertadas: {lexireto_stats['palabras_acertadas']}",
                f"Victorias: {lexireto_stats['victorias']}",
                f"Tiempo jugado: {utilities.formatTime(lexireto_stats['tiempo_jugado'])}",
                f"Tiempo promedio por victoria: {utilities.formatTime(int(lexireto_stats['tiempo_promedio_victoria']))}",
                f"Heptacracks: {lexireto_stats['heptacracks']}"
            ]
            for stat in stats:
                text_surface = statsFont.render(stat, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(submenuRect.centerx, y_offset))
                SCREEN.blit(text_surface, text_rect)
                y_offset += 35

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
                    return
        pygame.display.flip()

def infoMenu():
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 300, 150)
    buttons = {
        "LETRAS": pygame.Rect(submenuRect.x + 15, submenuRect.y + 20, 270, 50),  # Centrado en el rectángulo
        "LEXIRETO": pygame.Rect(submenuRect.x + 15, submenuRect.y + 10 + 20 + 50, 270, 50)  # Centrado en el rectángulo
    }
    buttonColors = {
        "LETRAS": GRAY,
        "LEXIRETO": GRAY
    }
    buttonFont = utilities.getMainFontBold(36)
    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenu(submenuRect, background, blurSurface, SCREEN) 

        for text, rect in buttons.items():
            # Sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, GRAY, rect, border_radius=10)
            # Texto
            text_surface = buttonFont.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            SCREEN.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
                elif buttons["LETRAS"].collidepoint(MOUSE_POS):
                    utilities.pressButton(buttons["LETRAS"], buttonColors["LETRAS"], SCREEN, buttonFont, "LETRAS")
                elif buttons["LEXIRETO"].collidepoint(MOUSE_POS):
                    utilities.pressButton(buttons["LEXIRETO"], buttonColors["LEXIRETO"], SCREEN, buttonFont, "LEXIRETO")

        pygame.display.flip()

def gameSelectMenu():
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 400, 530)

    # Crear fuentes para el texto
    titleFont = utilities.getMainFontBold(28)
    buttonFont = utilities.getMainFontBold(24)
    subtitleFont = utilities.getMainFontBold(28)

    # Diccionario de botones de juego
    gameButtons = {
        "LETRAS": pygame.Rect(submenuRect.x + 50, submenuRect.y + 60, 300, 50),
        "LEXIRETO": pygame.Rect(submenuRect.x + 50, submenuRect.y + 130, 300, 50)
    }

    # Diccionario de botones de dificultad
    difficultyButtons = {
        "DIFICIL": pygame.Rect(submenuRect.x + 50, submenuRect.y + 230, 300, 50),
        "NORMAL": pygame.Rect(submenuRect.x + 50, submenuRect.y + 300, 300, 50),
        "FACIL": pygame.Rect(submenuRect.x + 50, submenuRect.y + 370, 300, 50)
    }

    # Botón de jugar
    jugarButton = pygame.Rect(submenuRect.x + 50, submenuRect.y + 450, 300, 50)

    # Colores de los botones
    buttonColors = {
        "DIFICIL": BLUE,    # Azul
        "NORMAL": BLUE,     # Azul
        "FACIL": BLUE,      # Azul
        "LETRAS": BLUE,     # Azul
        "LEXIRETO": BLUE,   # Azul
        "JUGAR": GREEN       # Verde
    }

    # Variables para rastrear botones seleccionados
    selectedGame = None
    selectedDifficulty = None

    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenu(submenuRect, background, blurSurface, SCREEN)

        # Dibujar título
        titleSurface = titleFont.render("SELECCIONAR JUEGO", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(submenuRect.centerx, submenuRect.y + 30))
        SCREEN.blit(titleSurface, titleRect)

        # Dibujar botones de juego
        for text, rect in gameButtons.items():
            # Sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], rect, border_radius=10)
            # Texto
            text_surface = buttonFont.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            SCREEN.blit(text_surface, text_rect)

        # Dibujar subtítulo de dificultad
        subtitleSurface = subtitleFont.render("SELECCIONAR DIFICULTAD", True, (255, 255, 255))
        subtitleRect = subtitleSurface.get_rect(center=(submenuRect.centerx, submenuRect.y + 205))
        SCREEN.blit(subtitleSurface, subtitleRect)

        # Dibujar botones de dificultad
        for text, rect in difficultyButtons.items():
            # Sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], rect, border_radius=10)
            # Texto
            text_surface = buttonFont.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            SCREEN.blit(text_surface, text_rect)

        # Dibujar botón de jugar
        shadow_button = pygame.Rect(jugarButton.x, jugarButton.y + 3, jugarButton.width, jugarButton.height)
        pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
        pygame.draw.rect(SCREEN, buttonColors["JUGAR"], jugarButton, border_radius=10)
        text_surface = buttonFont.render("JUGAR", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=jugarButton.center)
        SCREEN.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return None, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
                    return None, None
                # Verificar clics en botones de juego
                for text, rect in gameButtons.items():
                    if rect.collidepoint(MOUSE_POS):
                        if selectedGame:
                            gameButtons[selectedGame], buttonColors[selectedGame] = utilities.unpressButton(gameButtons[selectedGame], buttonColors[selectedGame])
                        selectedGame = text
                        gameButtons[selectedGame], buttonColors[selectedGame] = utilities.keepButton(gameButtons[selectedGame], buttonColors[selectedGame])

                for text, rect in difficultyButtons.items():
                    if rect.collidepoint(MOUSE_POS):
                        if selectedDifficulty:
                            difficultyButtons[selectedDifficulty], buttonColors[selectedDifficulty] = utilities.unpressButton(difficultyButtons[selectedDifficulty], buttonColors[selectedDifficulty])
                        selectedDifficulty = text
                        difficultyButtons[selectedDifficulty], buttonColors[selectedDifficulty] = utilities.keepButton(difficultyButtons[selectedDifficulty], buttonColors[selectedDifficulty])

                # Verificar clic en botón de jugar
                if jugarButton.collidepoint(MOUSE_POS):
                    utilities.pressButton(jugarButton, buttonColors["JUGAR"], SCREEN, buttonFont, "JUGAR")
                    if selectedGame and selectedDifficulty:
                        running = False
                        return selectedGame, selectedDifficulty

        pygame.display.flip()

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
        "SI": GREEN,    # Verde
        "NO": RED      # Rojo
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

def rules():
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 750, 600)
    
    # Crear fuentes para el texto
    titleFont = utilities.getMainFontBold(32)
    rulesFont = utilities.getMainFontBold(24)
    
    # Texto de las reglas
    rules = [
        "LETRAS:",
        "Encuentra las siete palabras que hemos ocultado",
        "seleccionando casillas contiguas en todas las",
        "direcciones, no es posible el salto en diagonal. ",
        "Puedes utilizar cada letra tantas veces como quieras,",
        "pero no en una misma palabra.",
        "LEXIRETO:",
        "Forma palabras de al menos 3 letras. Puedes repetir las letras,",
        "pero siempre incluyendo la letra central.",
        "No se admiten nombres propios, plurales y formas verbales",
        "conjugadas (solo infinitivos).",
        "Encuentra palabras que incluyan las 7 letras (¡Heptacrack!)",
        "para mejorar tus estadisticas de juego"
    ]
    
    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenu(submenuRect, background, blurSurface, SCREEN)
        
        # Dibujar título
        titleSurface = titleFont.render("REGLAS", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(submenuRect.centerx, submenuRect.y + 40))
        SCREEN.blit(titleSurface, titleRect)
        
        # Dibujar reglas
        y_offset = submenuRect.y + 80
        for line in rules:
            text_surface = rulesFont.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(submenuRect.centerx, y_offset))
            SCREEN.blit(text_surface, text_rect)
            y_offset += 35
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
                    return
        
        pygame.display.flip()

firstScreen()