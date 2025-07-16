import utilities
import pygame
from utilities import HexagonButton
import math
import winScreen

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 147, 254)
GRAY = (112, 131, 134)
WIDTH = 1280 
HEIGHT = 720

def lexiretoGame(SCREEN, bg, user, loadGame, Dificultad = "NORMAL"):
    running = True
    palabra = ""
    retornoOpciones = None

    if loadGame:
        savedGame = utilities.loadGame(user, "lexireto")  # Especificar el tipo de juego
        if savedGame:
            letras = savedGame['letras']
            letraCentral = savedGame['letraCentral']
            palabrasObjetivo = savedGame['palabrasObjetivo']
            palabrasInicial = savedGame['palabrasInicial']
            cantidadPalabrasEncontradas = savedGame['cantidadPalabrasEncontradas']
            palabrasEncontradas = savedGame['palabrasEncontradas']
            palabrasHeptacrack = savedGame['palabrasHeptacrack']
            heptacrackEncontrados = savedGame['heptacrackEncontrados']
            cantidadHeptacrack = len(palabrasHeptacrack)
            cantidadEncontradas = len(palabrasEncontradas)
            start_time = pygame.time.get_ticks() - (savedGame['tiempo'] * 1000)  # Ajustar el tiempo inicial
            ultimo_tiempo_guardado = savedGame['ultimo_tiempo_guardado']
            cantPalabras = len(palabrasObjetivo)
        else:
            letras, letraCentral, palabrasObjetivo, palabrasInicial = utilities.getLexiretoMatrix(Dificultad)
            cantidadEncontradas = 0
            start_time = pygame.time.get_ticks()
            cantidadPalabrasEncontradas = {letra: 0 for letra in palabrasInicial.keys()}
            cantPalabras = len(palabrasObjetivo)
            palabrasEncontradas = []
            palabrasHeptacrack = []
            cantidadHeptacrack = 0
            heptacrackEncontrados = 0
            ultimo_tiempo_guardado = 0
            for word in palabrasObjetivo:
                if len(set(word)) == 7 and letraCentral in word and all(letra in word for letra in letras):
                    cantidadHeptacrack += 1
                    palabrasHeptacrack.append(word)

    else:
        letras, letraCentral, palabrasObjetivo, palabrasInicial = utilities.getLexiretoMatrix(Dificultad)
        cantidadEncontradas = 0
        start_time = pygame.time.get_ticks()
        cantidadPalabrasEncontradas = {letra: 0 for letra in palabrasInicial.keys()}
        cantPalabras = len(palabrasObjetivo)
        palabrasEncontradas = []
        palabrasHeptacrack = []
        cantidadHeptacrack = 0
        heptacrackEncontrados = 0
        ultimo_tiempo_guardado = 0
        for word in palabrasObjetivo:
            if len(set(word)) == 7 and letraCentral in word and all(letra in word for letra in letras):
                cantidadHeptacrack += 1
                palabrasHeptacrack.append(word)

    mainRect = pygame.Rect(50, 0, 350, HEIGHT)
    # Intentar cargar una partida guardada

    utilities.printLexireto(letras, letraCentral, palabrasObjetivo, palabrasInicial)
    # Cuadro para mostrar la palabra (arriba del centro)
    wordBox = pygame.Rect(WIDTH - 330, HEIGHT//2 - 95, 310, 50)

    # Diccionario de botones con sus rectángulos (centrados verticalmente)
    letrasButtons = {
        "BORRAR": pygame.Rect(WIDTH - 330, HEIGHT//2 - 25, 310, 50),  # En el centro
        "APLICAR": pygame.Rect(WIDTH - 330, wordBox.y + 140, 310, 50),  # Abajo
        "REGLAS": pygame.Rect(mainRect.x + 20, WIDTH//2 - 100, 310, 50),
        "OPCIONES": pygame.Rect(mainRect.x + 20, WIDTH//2 - 40, 310, 50)
    }

    # Diccionario de colores para cada botón
    buttonColors = {
        "BORRAR": (245, 77, 64),    # Rojo
        "APLICAR": (66, 159, 121),   # Verde
        "REGLAS": (66, 159, 121),
        "OPCIONES": (50, 147, 254)
    }

    # Tamaño y posición del botón central
    hex_size = 60
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Crear botón central
    centralButton = HexagonButton(
        center_x=center_x,
        center_y=center_y,
        size=hex_size,
        color=BLUE,
        text=letraCentral,
        text_color=WHITE
    )

    # Calcular posiciones para los botones periféricos
    peripheralButtons = []
    # La distancia entre centros es 2 * hex_size * cos(30°) + separación
    # cos(30°) ≈ 0.866, y agregamos una separación de 15 píxeles
    distance = 2 * hex_size * 0.866 + 15
    
    for i in range(6):
        angle = math.pi / 3 * i  # 60 grados entre cada botón
        offset_x = math.cos(angle) * distance
        offset_y = math.sin(angle) * distance
        
        button = HexagonButton(
            center_x=center_x + offset_x,
            center_y=center_y + offset_y,
            size=hex_size,
            color=GRAY,
            text=letras[i],
            text_color=WHITE
        )
        peripheralButtons.append(button)

    # Inicializar el tiempo
    paused_time = 0
    is_paused = False
    font = utilities.getMainFontBold(32)
    wordFont = utilities.getMainFontBold(40)
    listFont = utilities.getMainFontBold(30)
    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(bg, (0, 0))

        # Dibujar rectángulo principal
        pygame.draw.rect(SCREEN, (58, 80, 84), mainRect)

        # Dibujar título de la lista
        strLista = f"Palabras Totales ({cantidadEncontradas}/{cantPalabras})"
        tituloLista = listFont.render(strLista, True, WHITE)
        SCREEN.blit(tituloLista, (mainRect.x + 20, 20))
        y_offset = 60
        subtitulo = listFont.render(f"HEPTACRACKS ({heptacrackEncontrados}/{cantidadHeptacrack})", True, WHITE)
        SCREEN.blit(subtitulo, (mainRect.x + 20, y_offset))
        # Dibujar lista de palabras por letra
        for letra, palabras in sorted(palabrasInicial.items()):
            y_offset += 40
            texto = f"{letra} ({cantidadPalabrasEncontradas[letra]}/{len(palabras)})"
            texto_surface = listFont.render(texto, True, WHITE)
            SCREEN.blit(texto_surface, (mainRect.x + 20, y_offset))

        # Dibujar cuadro de la palabra
        # Sombra del cuadro
        shadow_box = pygame.Rect(wordBox.x, wordBox.y + 3, wordBox.width, wordBox.height)
        pygame.draw.rect(SCREEN, (30, 40, 42), shadow_box, border_radius=10)
        # Cuadro principal
        pygame.draw.rect(SCREEN, (58, 80, 84), wordBox, border_radius=10)
        
        # Dibujar la palabra centrada en el cuadro
        wordText = wordFont.render(palabra, True, WHITE)
        wordRect = wordText.get_rect(center=wordBox.center)
        SCREEN.blit(wordText, wordRect)

        # Dibujar botones y texto
        for text, rect in letrasButtons.items():
            # Crear sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            # Dibujar sombra del botón
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Dibujar rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], rect, border_radius=10)
            
            # Renderizar texto
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            
            # Dibujar texto
            SCREEN.blit(text_surface, text_rect)

        # Calcular tiempo transcurrido
        current_time = pygame.time.get_ticks()
        if not is_paused:
            elapsed_time = (current_time - start_time - paused_time) // 1000  # Convertir a segundos
        else:
            elapsed_time = (pause_start_time - start_time - paused_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        # Crear texto del tiempo
        timeText = f"Tiempo: {minutes:02d}:{seconds:02d}"
        timeSurface = font.render(timeText, True, WHITE)
        timeRect = timeSurface.get_rect(topright=(WIDTH - 20, 20))
        
        # Dibujar fondo para el texto del tiempo
        pygame.draw.rect(SCREEN, (30, 40, 42), timeRect.inflate(20, 10), border_radius=10)
        SCREEN.blit(timeSurface, timeRect)

        # Dibujar botones periféricos primero
        for button in peripheralButtons:
            button.draw(SCREEN)

        # Dibujar botón central último para que esté por encima
        centralButton.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clic en botones
                if letrasButtons["BORRAR"].collidepoint(MOUSE_POS):
                    utilities.pressButton(letrasButtons["BORRAR"], buttonColors["BORRAR"], SCREEN, font, "BORRAR")
                    palabra = ""  # Borrar la palabra
                elif letrasButtons["APLICAR"].collidepoint(MOUSE_POS):
                    utilities.pressButton(letrasButtons["APLICAR"], buttonColors["APLICAR"], SCREEN, font, "APLICAR")
                    # Aquí iría la lógica para verificar la palabra
                    if palabra in palabrasObjetivo and palabra not in palabrasEncontradas:
                        letra_inicial = palabra[0]
                        if letra_inicial in cantidadPalabrasEncontradas:
                            cantidadPalabrasEncontradas[letra_inicial] += 1
                            cantidadEncontradas += 1
                            palabrasEncontradas.append(palabra)
                            if palabra in palabrasHeptacrack:
                                heptacrackEncontrados += 1
                                utilities.updateStats(user, 'lexireto', 'heptacracks')
                            if cantidadEncontradas == cantPalabras:
                                winScreen.showWinScreen(SCREEN)
                                running = False

                            utilities.updateStats(user, 'lexireto', 'palabras_acertadas')
                            # Actualizar tiempo jugado al acertar una palabra
                            tiempo_actual = (pygame.time.get_ticks() - start_time - paused_time) // 1000
                            tiempo_diferencia = tiempo_actual - ultimo_tiempo_guardado
                            utilities.updateStats(user, 'lexireto', 'tiempo_jugado', tiempo_diferencia)
                            ultimo_tiempo_guardado = tiempo_actual
                    palabra = ""
                elif letrasButtons["REGLAS"].collidepoint(MOUSE_POS):
                    utilities.pressButton(letrasButtons["REGLAS"], buttonColors["REGLAS"], SCREEN, font, "REGLAS")
                    is_paused = True
                    pause_start_time = pygame.time.get_ticks()
                    lexiretoRules(SCREEN)
                    is_paused = False
                    paused_time += pygame.time.get_ticks() - pause_start_time
                elif letrasButtons["OPCIONES"].collidepoint(MOUSE_POS):
                    utilities.pressButton(letrasButtons["OPCIONES"], buttonColors["OPCIONES"], SCREEN, font, "OPCIONES")
                    is_paused = True
                    pause_start_time = pygame.time.get_ticks()
                    retornoOpciones = optionsMenu(SCREEN, letras, letraCentral, palabrasObjetivo, palabrasInicial, cantidadEncontradas, cantidadPalabrasEncontradas, elapsed_time, palabrasEncontradas, palabrasHeptacrack, heptacrackEncontrados, ultimo_tiempo_guardado)
                    if retornoOpciones == 0:
                        running = False
                        lexiretoGame(SCREEN, bg, user, False, Dificultad)
                    elif retornoOpciones == 1:
                        running = False
                        lexiretoGame(SCREEN, bg, user, True)
                    elif retornoOpciones == 2:
                        running = False
                        return
                    elif type(retornoOpciones) is str:
                        ultimo_tiempo_guardado = int(retornoOpciones)
                    retornoOpciones = None
                    is_paused = False
                    paused_time += pygame.time.get_ticks() - pause_start_time
                
                # Verificar clic en botón central
                if centralButton.is_clicked(MOUSE_POS, event.button == 1):
                    utilities.pressHexButton(
                        button=centralButton,
                        SCREEN=SCREEN,
                        press_offset=3,
                        darken_factor=60,
                        press_duration=150,
                        return_duration=50
                    )
                    if len(palabra) < 14:
                        palabra += letraCentral

                # Verificar clic en botones periféricos
                for i, button in enumerate(peripheralButtons):
                    if button.is_clicked(MOUSE_POS, event.button == 1):
                        utilities.pressHexButton(
                            button=button,
                            SCREEN=SCREEN,
                            press_offset=3,
                            darken_factor=60,
                            press_duration=150,
                            return_duration=50
                        )
                        if len(palabra) < 14:
                            palabra += letras[i]

        if cantidadEncontradas == cantPalabras:
            # Actualizar estadísticas
            running = False
            tiempo_actual = (pygame.time.get_ticks() - start_time - paused_time) // 1000
            tiempo_diferencia = tiempo_actual - ultimo_tiempo_guardado
            utilities.updateStats(user, 'lexireto', 'tiempo_jugado', tiempo_diferencia)
            ultimo_tiempo_guardado = tiempo_actual
            utilities.updateStats(user, 'lexireto', 'victorias', elapsed_time)  # Pasamos el tiempo total como valor
            winScreen.showWinScreen(SCREEN)
            return
        pygame.display.flip()

def optionsMenu(SCREEN, letras, letraCentral, palabrasObjetivo, palabrasInicial, cantidadEncontradas, cantidadPalabrasEncontradas, elapsed_time, palabrasEncontradas, palabrasHeptacrack, heptacrackEncontrados, ultimo_tiempo_guardado):
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 400, 450)  # Aumentado altura para nuevos botones
    currentUser = utilities.getUserLoggedIn()
    
    # Crear fuente para el texto
    titleFont = utilities.getMainFontBold(32)
    buttonFont = utilities.getMainFontBold(24)
    
    # Verificar si hay una partida guardada
    has_saved_game = utilities.hasSavedGame(currentUser, "lexireto")
    
    # Diccionario de botones base
    base_buttons = {
        "NUEVA PARTIDA": pygame.Rect(submenuRect.x + 50, submenuRect.y + 100, 300, 50),
        "GUARDAR PARTIDA": pygame.Rect(submenuRect.x + 50, submenuRect.y + 170, 300, 50),
        "MENÚ PRINCIPAL": pygame.Rect(submenuRect.x + 50, submenuRect.y + 240, 300, 50),
        "SALIR": pygame.Rect(submenuRect.x + 50, submenuRect.y + 310, 300, 50)
    }
    
    # Si hay una partida guardada, agregar el botón de cargar partida
    if has_saved_game:
        base_buttons["CARGAR PARTIDA"] = pygame.Rect(submenuRect.x + 50, submenuRect.y + 170, 300, 50)
        # Ajustar las posiciones de los botones siguientes
        base_buttons["GUARDAR PARTIDA"] = pygame.Rect(submenuRect.x + 50, submenuRect.y + 240, 300, 50)
        base_buttons["MENÚ PRINCIPAL"] = pygame.Rect(submenuRect.x + 50, submenuRect.y + 310, 300, 50)
        base_buttons["SALIR"] = pygame.Rect(submenuRect.x + 50, submenuRect.y + 380, 300, 50)
    
    # Colores de los botones
    buttonColors = {
        "NUEVA PARTIDA": (50, 147, 254),   # Azul
        "CARGAR PARTIDA": (50, 147, 254),  # Azul
        "GUARDAR PARTIDA": (50, 147, 254),  # Verde
        "MENÚ PRINCIPAL": (66, 159, 121),   # Azul
        "SALIR": (245, 77, 64)  # Rojo
    }
    
    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenu(submenuRect, background, blurSurface, SCREEN)
        
        # Dibujar título
        titleSurface = titleFont.render("OPCIONES", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(submenuRect.centerx, submenuRect.y + 50))
        SCREEN.blit(titleSurface, titleRect)
        
        # Dibujar botones
        for text, rect in base_buttons.items():
            # Sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], rect, border_radius=10)
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
                elif base_buttons["NUEVA PARTIDA"].collidepoint(MOUSE_POS):
                    utilities.pressButton(base_buttons["NUEVA PARTIDA"], buttonColors["NUEVA PARTIDA"], SCREEN, buttonFont, "NUEVA PARTIDA")
                    running = False
                    return 0  # Retornar 0 para indicar que se debe iniciar una nueva partida
                elif has_saved_game and base_buttons["CARGAR PARTIDA"].collidepoint(MOUSE_POS):
                    utilities.pressButton(base_buttons["CARGAR PARTIDA"], buttonColors["CARGAR PARTIDA"], SCREEN, buttonFont, "CARGAR PARTIDA")
                    running = False
                    return 1  # Retornar 1 para indicar que se debe cargar una partida
                elif base_buttons["GUARDAR PARTIDA"].collidepoint(MOUSE_POS):
                    utilities.pressButton(base_buttons["GUARDAR PARTIDA"], buttonColors["GUARDAR PARTIDA"], SCREEN, buttonFont, "GUARDAR PARTIDA")
                    # Guardar el estado actual del juego
                    gameState = {
                        'letras': letras,
                        'letraCentral': letraCentral,
                        'palabrasObjetivo': list(palabrasObjetivo),
                        'palabrasInicial': palabrasInicial,
                        'cantidadEncontradas': cantidadEncontradas,
                        'cantidadPalabrasEncontradas': cantidadPalabrasEncontradas,
                        'palabrasEncontradas': palabrasEncontradas,
                        'palabrasHeptacrack': palabrasHeptacrack,
                        'heptacrackEncontrados': heptacrackEncontrados,
                        'tiempo': elapsed_time,
                        'ultimo_tiempo_guardado': ultimo_tiempo_guardado
                    }
                    utilities.saveGame(currentUser, gameState, "lexireto")
                    # Actualizar tiempo jugado al guardar el juego
                    user = utilities.getUserLoggedIn()
                    tiempo_actual = elapsed_time
                    tiempo_diferencia = tiempo_actual - ultimo_tiempo_guardado
                    utilities.updateStats(user, 'lexireto', 'tiempo_jugado', tiempo_diferencia)
                    ultimo_tiempo_guardado = tiempo_actual
                    return str(ultimo_tiempo_guardado)
                elif base_buttons["MENÚ PRINCIPAL"].collidepoint(MOUSE_POS):
                    utilities.pressButton(base_buttons["MENÚ PRINCIPAL"], buttonColors["MENÚ PRINCIPAL"], SCREEN, buttonFont, "MENÚ PRINCIPAL")
                    running = False
                    return 2 # Indicar menu principal
                elif base_buttons["SALIR"].collidepoint(MOUSE_POS):
                    utilities.pressButton(base_buttons["SALIR"], buttonColors["SALIR"], SCREEN, buttonFont, "SALIR")
                    running = False
                    pygame.quit()
                    exit()
        
        pygame.display.flip()

def lexiretoRules(SCREEN):
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 750, 350)
    
    # Crear fuentes para el texto
    titleFont = utilities.getMainFontBold(32)
    rulesFont = utilities.getMainFontBold(24)
    
    # Texto de las reglas
    rules = [
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
        y_offset = submenuRect.y + 100
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
        
        pygame.display.flip()