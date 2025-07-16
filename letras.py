import utilities
import pygame
import time
import winScreen

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 147, 254)
GRAY = (112, 131, 134)
GREEN = (66, 159, 121)
WIDTH = 1280 
HEIGHT = 720

class LetterButton:
    def __init__(self, x, y, size, letter, color=GRAY, row=0, col=0):
        self.rect = pygame.Rect(x, y, size, size)
        self.letter = letter
        self.color = color
        self.original_color = color
        self.is_pressed = False
        self.row = row
        self.col = col

    def draw(self, screen):
        # Dibujar sombra
        shadow_rect = pygame.Rect(self.rect.x, self.rect.y + 3, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, (30, 40, 42), shadow_rect, border_radius=10)
        
        # Dibujar botón
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        
        # Dibujar letra
        font = utilities.getMainFontBold(32)
        text = font.render(self.letter, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, pos, is_left_click):
        return self.rect.collidepoint(pos) and is_left_click

    def reset_color(self):
        self.color = self.original_color

def is_adjacent(button1, button2):
    # Verificar si dos botones son adyacentes (arriba, abajo, izquierda, derecha)
    row_diff = abs(button1.row - button2.row)
    col_diff = abs(button1.col - button2.col)
    return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

def letrasGame(SCREEN, bg, user, loadGame, Dificultad = "NORMAL"):
    running = True
    palabraActual = ""
    retornoOpciones = None
    
    # Inicializar matriz 8x8
    matriz_size = 6
    button_size = 50
    spacing = 5
    
    # Determinar cantidad de palabras según dificultad
    match Dificultad:
        case "FACIL":
            cantidad_palabras = 5
        case "NORMAL":
            cantidad_palabras = 10
        case "DIFICIL":
            cantidad_palabras = 15
    
    juegoCargado = False
    if loadGame:
        savedGame = utilities.loadLetrasGame(user)
        if savedGame:
            matriz = savedGame['matriz']
            palabrasSeleccionadas = savedGame['palabrasSeleccionadas']
            palabrasLongitud = savedGame['palabrasLongitud']
            totalPalabras = len(palabrasSeleccionadas)
            palabrasEncontradas = savedGame['palabrasEncontradas'] if isinstance(savedGame['palabrasEncontradas'], list) else []
            palabras_por_longitud = savedGame['palabrasPorLongitud']
            contadorPalabras = len(palabrasEncontradas)
            start_time = pygame.time.get_ticks() - (savedGame['tiempo'] * 1000)
            ultimo_tiempo_guardado = savedGame['ultimo_tiempo_guardado']
            juegoCargado = True
        else:
            matriz, palabrasSeleccionadas, palabrasLongitud, totalPalabras = utilities.generarLetrasMatrix(cantidad_palabras, matriz_size, matriz_size, 10)
            totalPalabras = len(palabrasSeleccionadas)  # Aseguramos que totalPalabras sea la longitud de palabrasSeleccionadas
            palabrasEncontradas = []
            palabras_por_longitud = {longitud: 0 for longitud in palabrasLongitud.keys()}
            contadorPalabras = 0
            start_time = pygame.time.get_ticks()
            ultimo_tiempo_guardado = 0
    else:
        matriz, palabrasSeleccionadas, palabrasLongitud, totalPalabras = utilities.generarLetrasMatrix(cantidad_palabras, matriz_size, matriz_size, 10)
        totalPalabras = len(palabrasSeleccionadas)  # Aseguramos que totalPalabras sea la longitud de palabrasSeleccionadas
        palabrasEncontradas = []
        palabras_por_longitud = {longitud: 0 for longitud in palabrasLongitud.keys()}
        contadorPalabras = 0
        start_time = pygame.time.get_ticks()
        ultimo_tiempo_guardado = 0
    
    utilities.printLetras(palabrasSeleccionadas, palabrasLongitud, totalPalabras)
    # Calcular el área total de la matriz
    total_width = matriz_size * (button_size + spacing) - spacing
    total_height = matriz_size * (button_size + spacing) - spacing
    
    # Calcular la posición inicial para centrar la matriz
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - total_height) // 2
    
    # Crear matriz de botones
    letter_buttons = []
    for i in range(matriz_size):
        row = []
        for j in range(matriz_size):
            x = start_x + j * (button_size + spacing)
            y = start_y + i * (button_size + spacing)
            letter = matriz[i][j]
            button = LetterButton(x, y, button_size, letter, row=i, col=j)
            row.append(button)
        letter_buttons.append(row)

    # Rectángulo principal para la interfaz
    mainRect = pygame.Rect(50, 0, 350, HEIGHT)
    listFont = utilities.getMainFontBold(30)
    
    # Cuadro para mostrar la palabra
    wordBox = pygame.Rect(WIDTH - 330, HEIGHT//2 - 95, 310, 50)
    
    # Calcular la posición de los botones de control debajo de la matriz
    matriz_bottom = start_y + total_height
    button_y = matriz_bottom + 20  # 20 píxeles de separación
    button_spacing = 20  # Espacio entre botones
    
    # Calcular el ancho de cada botón para que ocupen el ancho total de la matriz
    button_width = (total_width - button_spacing) // 2
    
    # Botones de control
    control_buttons = {
        "BORRAR": pygame.Rect(WIDTH - 330, HEIGHT//2 - 25, 310, 50),
        "APLICAR": pygame.Rect(WIDTH - 330, wordBox.y + 140, 310, 50),
        "REGLAS": pygame.Rect(start_x, button_y, button_width, 50),
        "OPCIONES": pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, 50)
    }
    
    # Colores de los botones
    button_colors = {
        "BORRAR": (245, 77, 64),    # Rojo
        "APLICAR": (66, 159, 121),   # Verde
        "REGLAS": (66, 159, 121),
        "OPCIONES": (50, 147, 254)
    }

    # Inicializar tiempo y contadores
    paused_time = 0
    is_paused = False
    
    # Lista para mantener registro de los botones presionados
    pressed_buttons = []
    
    # Diccionario para mantener registro de palabras encontradas por longitud
    palabras_encontradas_por_longitud = {longitud: [] for longitud in palabrasLongitud.keys()}
    
    # Fuentes
    font = utilities.getMainFontBold(32)
    wordFont = utilities.getMainFontBold(40)

    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(bg, (0, 0))

        # Dibujar rectángulo principal
        pygame.draw.rect(SCREEN, (58, 80, 84), mainRect)

        # Dibujar título y contador
        strLista = f"Total Palabras ({contadorPalabras}/{totalPalabras})"
        tituloLista = listFont.render(strLista, True, WHITE)
        SCREEN.blit(tituloLista, (mainRect.x + 20, 20))

        # Dibujar palabras por longitud
        y_offset = 60
        for longitud, palabras in palabrasLongitud.items():
            texto = f"{longitud} letras: {palabras_por_longitud[longitud]}/{len(palabras)}"
            texto_surface = listFont.render(texto, True, WHITE)
            SCREEN.blit(texto_surface, (mainRect.x + 20, y_offset))
            y_offset += 40
            
            # Calcular el número de palabras por columna
            total_palabras = len(palabras)
            palabras_por_columna = (total_palabras + 1) // 2
            
            # Dibujar todas las palabras
            for i, palabra in enumerate(palabras):
                columna = i // palabras_por_columna
                fila = i % palabras_por_columna
                x_pos = mainRect.x + 20 + (columna * (mainRect.width // 2))
                y_pos = y_offset + (fila * 30)
                
                if palabra in palabrasEncontradas:
                    # Si la palabra está encontrada, mostrarla completa en verde
                    texto = palabra
                    texto_surface = listFont.render(texto, True, GREEN)
                else:
                    # Si no está encontrada, mostrar solo la inicial
                    texto = palabra[0] + " _" * (len(palabra) - 1)
                    texto_surface = listFont.render(texto, True, WHITE)
                
                SCREEN.blit(texto_surface, (x_pos, y_pos))
            
            # Actualizar y_offset para el siguiente grupo con más separación
            y_offset += max(len(palabras) // 2, 1) * 30 + 30  # Aumentado de 20 a 40

        # Dibujar matriz de letras
        for row in letter_buttons:
            for button in row:
                button.draw(SCREEN)

        # Dibujar cuadro de la palabra
        shadow_box = pygame.Rect(wordBox.x, wordBox.y + 3, wordBox.width, wordBox.height)
        pygame.draw.rect(SCREEN, (30, 40, 42), shadow_box, border_radius=10)
        pygame.draw.rect(SCREEN, (58, 80, 84), wordBox, border_radius=10)
        
        wordText = wordFont.render(palabraActual, True, WHITE)
        wordRect = wordText.get_rect(center=wordBox.center)
        SCREEN.blit(wordText, wordRect)

        # Dibujar botones de control
        for text, rect in control_buttons.items():
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            pygame.draw.rect(SCREEN, button_colors[text], rect, border_radius=10)
            
            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            SCREEN.blit(text_surface, text_rect)

        # Mostrar tiempo
        current_time = pygame.time.get_ticks()
        if not is_paused:
            elapsed_time = (current_time - start_time - paused_time) // 1000
        else:
            elapsed_time = (pause_start_time - start_time - paused_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        timeText = f"Tiempo: {minutes:02d}:{seconds:02d}"
        timeSurface = font.render(timeText, True, WHITE)
        timeRect = timeSurface.get_rect(topright=(WIDTH - 20, 20))
        pygame.draw.rect(SCREEN, (30, 40, 42), timeRect.inflate(20, 10), border_radius=10)
        SCREEN.blit(timeSurface, timeRect)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clic en botones de control
                if control_buttons["BORRAR"].collidepoint(MOUSE_POS):
                    utilities.pressButton(control_buttons["BORRAR"], button_colors["BORRAR"], SCREEN, font, "BORRAR")
                    palabraActual = ""
                    # Resetear colores de los botones presionados
                    for button in pressed_buttons:
                        button.reset_color()
                    pressed_buttons.clear()
                if control_buttons["APLICAR"].collidepoint(MOUSE_POS):
                    utilities.pressButton(control_buttons["APLICAR"], button_colors["APLICAR"], SCREEN, font, "APLICAR")
                    if palabraActual in palabrasSeleccionadas and palabraActual not in palabrasEncontradas:
                        if juegoCargado:
                            longitud = str(len(palabraActual))
                        else:
                            longitud = len(palabraActual)
                        if longitud not in palabras_por_longitud:
                            palabras_por_longitud[longitud] = 0
                        if palabras_por_longitud[longitud] < len(palabrasLongitud[longitud]):
                            palabras_por_longitud[longitud] += 1
                            contadorPalabras += 1
                            palabrasEncontradas.append(palabraActual)
                            palabras_encontradas_por_longitud[longitud].append(palabraActual)
                            utilities.updateStats(user, 'letras', 'palabras_acertadas')
                            # Actualizar tiempo jugado al acertar una palabra
                            tiempo_actual = (pygame.time.get_ticks() - start_time - paused_time) // 1000
                            tiempo_diferencia = tiempo_actual - ultimo_tiempo_guardado
                            utilities.updateStats(user, 'letras', 'tiempo_jugado', tiempo_diferencia)
                            ultimo_tiempo_guardado = tiempo_actual
                    palabraActual = ""
                    # Resetear colores de los botones presionados
                    for button in pressed_buttons:
                        button.reset_color()
                    pressed_buttons.clear()
                elif control_buttons["REGLAS"].collidepoint(MOUSE_POS):
                    utilities.pressButton(control_buttons["REGLAS"], button_colors["REGLAS"], SCREEN, font, "REGLAS")
                    is_paused = True
                    pause_start_time = pygame.time.get_ticks()
                    letrasRules(SCREEN)
                    is_paused = False
                    paused_time += pygame.time.get_ticks() - pause_start_time
                elif control_buttons["OPCIONES"].collidepoint(MOUSE_POS):
                    utilities.pressButton(control_buttons["OPCIONES"], button_colors["OPCIONES"], SCREEN, font, "OPCIONES")
                    is_paused = True
                    pause_start_time = pygame.time.get_ticks()
                    retornoOpciones = optionsMenu(SCREEN, matriz, palabrasSeleccionadas, palabrasLongitud, palabrasEncontradas, palabras_por_longitud, elapsed_time, ultimo_tiempo_guardado)
                    if retornoOpciones == 0:
                        running = False
                        letrasGame(SCREEN, bg, user, False, Dificultad)
                    elif retornoOpciones == 1:
                        running = False
                        letrasGame(SCREEN, bg, user, True)
                    elif retornoOpciones == 2:
                        running = False
                        return
                    elif type(retornoOpciones) is str:
                        ultimo_tiempo_guardado = int(retornoOpciones)

                    retornoOpciones = None
                    is_paused = False
                    paused_time += pygame.time.get_ticks() - pause_start_time

                
                # Verificar clic en botones de letras
                for row in letter_buttons:
                    for button in row:
                        if button.is_clicked(MOUSE_POS, event.button == 1):
                            if len(palabraActual) < 11 and button not in pressed_buttons:
                                # Si es la primera letra o es adyacente a la última letra presionada
                                if not pressed_buttons or is_adjacent(pressed_buttons[-1], button):
                                    utilities.pressButton(button.rect, button.color, SCREEN, font, button.letter)
                                    button.color = GREEN
                                    pressed_buttons.append(button)
                                    palabraActual += button.letter

        # Cuando se gana el juego
        if contadorPalabras == totalPalabras:
            # Actualizar estadísticas
            running = False
            tiempo_actual = (pygame.time.get_ticks() - start_time - paused_time) // 1000
            tiempo_diferencia = tiempo_actual - ultimo_tiempo_guardado
            utilities.updateStats(user, 'letras', 'tiempo_jugado', tiempo_diferencia)
            ultimo_tiempo_guardado = tiempo_actual
            utilities.updateStats(user, 'letras', 'victorias', elapsed_time)  # Pasamos el tiempo total como valor
            winScreen.showWinScreen(SCREEN)
            return

        pygame.display.flip()

    return retornoOpciones

def letrasRules(SCREEN):
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 750, 300)
    
    # Crear fuentes para el texto
    titleFont = utilities.getMainFontBold(32)
    rulesFont = utilities.getMainFontBold(24)
    
    # Texto de las reglas
    rules = [
        "Encuentra las siete palabras que hemos ocultado",
        "seleccionando casillas contiguas en todas las",
        "direcciones, no es posible el salto en diagonal. ",
        "Puedes utilizar cada letra tantas veces como quieras,",
        "pero no en una misma palabra."
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

def optionsMenu(SCREEN, matriz, palabrasSeleccionadas, palabrasLongitud, palabrasEncontradas, palabras_por_longitud, elapsed_time, ultimo_tiempo_guardado):
    user = utilities.getUserLoggedIn()

    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 400, 450)
    currentUser = utilities.getUserLoggedIn()
    
    # Crear fuente para el texto
    titleFont = utilities.getMainFontBold(32)
    buttonFont = utilities.getMainFontBold(24)
    
    # Verificar si hay una partida guardada
    has_saved_game = utilities.hasSavedGame(currentUser, "letras")
    
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
                        'matriz': matriz,
                        'palabrasSeleccionadas': palabrasSeleccionadas,
                        'palabrasLongitud': palabrasLongitud,
                        'palabrasEncontradas': palabrasEncontradas,
                        'palabrasPorLongitud': palabras_por_longitud,
                        'tiempo': elapsed_time,
                        'ultimo_tiempo_guardado': ultimo_tiempo_guardado
                    }
                    utilities.saveLetrasGame(currentUser, gameState)
                    # Actualizar tiempo jugado al guardar el juego
                    tiempo_actual = elapsed_time
                    tiempo_diferencia = tiempo_actual - ultimo_tiempo_guardado
                    utilities.updateStats(user, 'letras', 'tiempo_jugado', tiempo_diferencia)
                    ultimo_tiempo_guardado = str(tiempo_actual)
                    return ultimo_tiempo_guardado
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
