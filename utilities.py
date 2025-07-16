import pygame
import os
import json
import math
import copy
import random

WIDTH, HEIGHT = 1280, 720
userLoggedIn = "elpepe"
redBG = pygame.image.load("assets/redBG.webp")
redBG = pygame.transform.scale(redBG, (WIDTH, HEIGHT))
greenBG = pygame.image.load("assets/greenBG.jpg")
greenBG = pygame.transform.scale(greenBG, (WIDTH, HEIGHT))
diccionaryRoute = "assets/diccionario.txt"

def getDefaultScreen():
    return WIDTH, HEIGHT

def getDiccionaryRoute():
    return diccionaryRoute

def getBG(gameStatus):
    gameStatus.upper()
    match gameStatus:
        case "MENU":
            return redBG
        case "GAME":
            return greenBG

def getColor(color):
    color.upper()
    match color:
        case "WHITE":
            return (255, 255, 255)
        case "BLACK":
            return (0, 0, 0)
        case "BLUE":
            return (50, 147, 254)
        case "RED":
            return (245, 77, 64)
        case "GRAY":
            return (112, 131, 134)
        case "GREEN":
            return (66, 159, 121)

def setUserLoggedIn(user):
    global userLoggedIn
    userLoggedIn = user

def getUserLoggedIn():
    return userLoggedIn

def animateTitle(SCREEN, bg, WIDTH, HEIGHT, titleImage):
    alpha = 0  # Comenzamos con transparencia total
    fade_speed = 255 / 120  
    clock = pygame.time.Clock()
    
    while alpha < 255:
        SCREEN.blit(bg, (0, 0))
        
        # Crear una superficie temporal para el título con transparencia
        title_surface = titleImage.copy()
        title_surface.set_alpha(alpha)
        SCREEN.blit(title_surface, (0, -50))
        
        # Aumentar la transparencia gradualmente
        alpha = min(alpha + fade_speed, 255)
        
        pygame.display.flip()
        clock.tick(60)  # Mantener 60 FPS

    pygame.time.wait(200)

def getMainFont(size):
    return pygame.font.Font("assets/pixel_operator/PixelOperator.ttf", size)

def getMainFontBold(size):
    return pygame.font.Font("assets/pixel_operator/PixelOperator-Bold.ttf", size)

def pressButton(button, buttonColors, SCREEN, FONT, text):            
    # Efecto de presión para el botón SALIR
    pressed_rect = pygame.Rect(button.x, button.y, 
                            button.width, button.height + 3)
    unpressedRect = pygame.Rect(button.x, button.y, 
                            button.width, button.height)
    # Color más oscuro para el botón presionado
    darker_color = (max(0, buttonColors[0] - 40), 
                    max(0, buttonColors[1] - 40), 
                    max(0, buttonColors[2] - 40))
    pygame.draw.rect(SCREEN, darker_color, pressed_rect, border_radius=10)
    
    # Dibujar el texto en la nueva posición
    textSurface = FONT.render(text, True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(pressed_rect.centerx, pressed_rect.centery))
    SCREEN.blit(textSurface, textRect)
    
    pygame.display.flip()
    pygame.time.delay(200)  # Pequeña pausa para ver el efecto

    pygame.draw.rect(SCREEN, buttonColors, unpressedRect, border_radius=10)
    textRect = textSurface.get_rect(center=(unpressedRect.centerx, unpressedRect.centery))
    SCREEN.blit(textSurface, textRect)
    pygame.display.flip()
    pygame.time.delay(100)  # Pequeña pausa para ver el efecto

def keepButton(button, buttonColors):
    # Efecto de presión para el botón SALIR
    PressedRect = pygame.Rect(button.x, button.y, 
                            button.width, button.height + 3)
    # Color más oscuro para el botón presionado
    darkerColor = (max(0, buttonColors[0] - 40), 
                    max(0, buttonColors[1] - 40), 
                    max(0, buttonColors[2] - 40))    
    return PressedRect, darkerColor

def unpressButton( button, buttonColors):
    unpressedRect = pygame.Rect(button.x, button.y, 
                            button.width, button.height - 3)
    # Color más oscuro para el botón presionado
    undarkerColor = (max(0, buttonColors[0] + 40), 
                    max(0, buttonColors[1] + 40), 
                    max(0, buttonColors[2] + 40))    
    return unpressedRect, undarkerColor

def createSubmenu(width, height, screen, submenuWidth, submenuHeight):
    submenuRect = pygame.Rect((width - submenuWidth) // 2, (height - submenuHeight) // 2, submenuWidth, submenuHeight)
    background = pygame.Surface((width, height))
    background.blit(screen, (0, 0))
    
    # Aplicar efecto de desenfoque (simulado con un rectángulo semitransparente)
    blurSurface = pygame.Surface((width, height), pygame.SRCALPHA)
    blurSurface.fill((255, 255, 255, 128))  # Negro semitransparente para simular desenfoque

    pygame.draw.rect(screen, (53, 77, 85), submenuRect, border_radius=20)
    pygame.draw.rect(screen, (175, 183, 197), submenuRect, 5, border_radius=20)
    return submenuRect, background, blurSurface

def createSubmenuWithoutBlur(width, height, screen, submenuWidth, submenuHeight):
    submenuRect = pygame.Rect((width - submenuWidth) // 2, (height - submenuHeight) // 2, submenuWidth, submenuHeight)
    background = pygame.Surface((width, height))
    background.blit(screen, (0, 0))
    return submenuRect, background

def blitSubmenu(submenuRect, background, blurSurface, screen):
    screen.blit(background, (0, 0))
    screen.blit(blurSurface, (0, 0))
    pygame.draw.rect(screen, (53, 77, 85), submenuRect, border_radius=20)
    pygame.draw.rect(screen, (175, 183, 197), submenuRect, 5, border_radius=20)

def blitSubmenuWithoutBlur(submenuRect, background, screen):
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (53, 77, 85), submenuRect, border_radius=20)
    pygame.draw.rect(screen, (175, 183, 197), submenuRect, 5, border_radius=20)

def logInUser(username, password):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
            
        # Verificar si el usuario existe y la contraseña coincide
        if username in users and users[username]["password"] == password:
            setUserLoggedIn(username)
            return True
        return False
    except Exception as e:
        print(f"Error al verificar credenciales: {e}")
        return False

def initializeUsersFile():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as file:
            json.dump({}, file)

def registerUser(username, password):
    try:
        # Asegurarse de que el archivo users.json existe
        initializeUsersFile()
        
        # Leer usuarios existentes
        with open("users.json", "r") as file:
            users = json.load(file)
        
        # Verificar si el usuario ya existe
        if username in users:
            return False
        
        # Agregar nuevo usuario con estadísticas inicializadas
        users[username] = {
            "password": password,
            "stats": {
                "letras": {
                    "palabras_acertadas": 0,
                    "victorias": 0,
                    "tiempo_jugado": 0,
                    "tiempo_promedio_victoria": 0,
                    "total_tiempo_victorias": 0
                },
                "lexireto": {
                    "palabras_acertadas": 0,
                    "victorias": 0,
                    "tiempo_jugado": 0,
                    "tiempo_promedio_victoria": 0,
                    "total_tiempo_victorias": 0,
                    "heptacracks": 0,
                }
            }
        }
        
        # Guardar usuarios actualizados
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
        
        setUserLoggedIn(username)
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False

class HexagonButton:
    def __init__(self, center_x, center_y, size, color=(0, 100, 255), shadow_color=(30, 40, 42), 
                 text="", text_color=(255, 255, 255), shadow_offset=5):
        """
        Crea un botón hexagonal con sombra y sin borde
        
        Args:
            center_x (int): Posición X del centro
            center_y (int): Posición Y del centro
            size (int): Radio del hexágono
            color (tuple): Color RGB del botón
            shadow_color (tuple): Color RGB de la sombra
            text (str): Texto a mostrar
            text_color (tuple): Color RGB del texto
            shadow_offset (int): Desplazamiento de la sombra
        """
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.color = color
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.text = text
        self.text_color = text_color
        self.points = self._calculate_hexagon_points()
        self.shadow_points = self._calculate_shadow_points()
        
    def _calculate_hexagon_points(self):
        """Calcula los 6 puntos del hexágono principal"""
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            x = self.center_x + self.size * math.cos(angle_rad)
            y = self.center_y + self.size * math.sin(angle_rad)
            points.append((x, y))
        return points
    
    def _calculate_shadow_points(self):
        """Calcula los puntos del hexágono de sombra con desplazamiento vertical +3"""
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            x = self.center_x + self.size * math.cos(angle_rad)  # Misma X que el original
            y = self.center_y + 3 + self.size * math.sin(angle_rad)  # Y desplazada +3
            points.append((x, y))
        return points
    
    def draw(self, surface):
        """Dibuja el botón con sombra vertical, sin borde y con tu fuente"""
        # Dibuja sombra (y +3)
        pygame.draw.polygon(surface, self.shadow_color, self.shadow_points)
        
        # Dibuja hexágono principal
        pygame.draw.polygon(surface, self.color, self.points)
        
        # Dibuja texto con tu fuente personalizada
        if self.text:
            # Usa tu función getMainFont existente
            font = getMainFontBold(int(self.size))  # Ajusté el divisor para mejor proporción
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.center_x, self.center_y))
            surface.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        """Verifica si el botón fue clickeado"""
        if not mouse_clicked:
            return False
        return self._point_in_hexagon(mouse_pos)
    
    def _point_in_hexagon(self, point):
        """Determina si un punto está dentro del hexágono"""
        x, y = point
        n = len(self.points)
        inside = False
        
        # Algoritmo de ray casting
        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside

    def __deepcopy__(self, memo):
        new_button = HexagonButton(
            center_x=self.center_x,
            center_y=self.center_y,
            size=self.size,
            color=copy.deepcopy(self.color, memo),
            shadow_color=copy.deepcopy(self.shadow_color, memo),
            text=self.text,  # Strings son inmutables, no necesitan deepcopy
            text_color=copy.deepcopy(self.text_color, memo)
        )
        return new_button
    
def pressHexButton(button, SCREEN, press_offset=3, press_duration=200, 
                  return_duration=100, darken_factor=40):
    """
    Efecto de presión mejorado para botón hexagonal
    
    Args:
        button: Instancia de HexagonButton
        SCREEN: Superficie donde dibujar
        press_offset: Desplazamiento vertical al presionar (píxeles)
        press_duration: Duración estado presionado (ms)
        return_duration: Duración transición de regreso (ms)
        darken_factor: Cuánto oscurecer el color (0-255)
    """
    originalButton = copy.deepcopy(button)
    # Guardar estado original
    original_properties = {
        'color': button.color,
        'points': button.points.copy(),
        'text_color': button.text_color,
        'center_y': button.center_y
    }
    
    # Aplicar efecto presionado
    button.color = (
        max(0, button.color[0] - darken_factor),
        max(0, button.color[1] - darken_factor),
        max(0, button.color[2] - darken_factor)
    )

    originalButton.color = (
        max(0, originalButton.color[0] - darken_factor),
        max(0, originalButton.color[1] - darken_factor),
        max(0, originalButton.color[2] - darken_factor)
    )
    originalButton.text = ""
    
    # Desplazar verticalmente
    button.center_y += press_offset
    button.points = button._calculate_hexagon_points()  # Recalcular puntos
    
    # Opcional: aclarar texto durante el press
    button.text_color = (
        min(255, button.text_color[0] + 30),
        min(255, button.text_color[1] + 30),
        min(255, button.text_color[2] + 30)
    )
    
    # Dibujar y mostrar
    originalButton.draw(SCREEN)
    button.draw(SCREEN)
    pygame.display.flip()
    pygame.time.delay(press_duration)
    
    # Restaurar estado original
    button.color = original_properties['color']
    button.center_y = original_properties['center_y']
    button.points = original_properties['points']
    button.text_color = original_properties['text_color']
    
    button.draw(SCREEN)
    pygame.display.flip()
    pygame.time.delay(return_duration)

def cargarDiccionario():
    with open(diccionaryRoute, "r", encoding="utf-8") as f:
        palabras = [linea.strip().upper() for linea in f if len(linea.strip()) >= 4 and linea.strip().isalpha()]
    
    print(f"Cantidad de palabras cargadas: {len(palabras)}")
    return palabras


def seleccionarPalabras(diccionario, max_palabras):
    intentos = 1000
    for _ in range(intentos):
        
        base = random.choice(diccionario)
        if len(base) != len(set(base)):
            continue  
        
        letras = set(base)
        if len(letras) == 7:
            letra_central = random.choice(list(letras))
            palabras_validas = [
                palabra for palabra in diccionario
                if set(palabra).issubset(letras) and letra_central in palabra
            ]
            if base not in palabras_validas:
                palabras_validas.append(base)
            
            letras.remove(letra_central)
            if 10 <= len(palabras_validas) <= max_palabras:
                return sorted(letras), letra_central, palabras_validas
            
            elif len(palabras_validas) > max_palabras:
                random.shuffle(palabras_validas)
                ind = palabras_validas.index(base)
                palabras_validas[0], palabras_validas[ind] = palabras_validas[ind], palabras_validas[0]
                return sorted(letras), letra_central, palabras_validas[:max_palabras]

    print("No se pudo encontrar un conjunto válido de letras.")
    return [], "", []

def clasificarPalabras(palabras_objetivo):
    clasificacion = {}
    for palabra in palabras_objetivo:
        letra_inicial = palabra[0]
        if letra_inicial not in clasificacion:
            clasificacion[letra_inicial] = []
        clasificacion[letra_inicial].append(palabra)
    return clasificacion

def getLexiretoMatrix(Dificultad):
    diccionario = cargarDiccionario()
    match Dificultad:
        case "FACIL":
            cantPalabras = 15
        case "NORMAL":
            cantPalabras = 30
        case "DIFICIL":
            cantPalabras = 45
    letras, letraCentral, palabrasObjetivo = seleccionarPalabras(diccionario, cantPalabras)
    palabrasInicial = clasificarPalabras(palabrasObjetivo)
    return letras, letraCentral, palabrasObjetivo, palabrasInicial

def saveGame(username, gameState, gameType):
    """
    Guarda el estado del juego en un archivo JSON
    
    Args:
        username (str): Nombre del usuario
        gameState (dict): Estado del juego a guardar
        gameType (str): Tipo de juego ("lexireto" o "letras")
    """
    # Crear el directorio saves si no existe
    if not os.path.exists('saves'):
        os.makedirs('saves')
    
    # Ruta del archivo de guardado
    savePath = f'saves/{username}_{gameType}.json'
    
    # Convertir el estado del juego a un formato serializable
    saveData = {
        'gameType': gameType,
        'letras': gameState['letras'],
        'letraCentral': gameState['letraCentral'],
        'palabrasObjetivo': list(gameState['palabrasObjetivo']) if 'palabrasObjetivo' in gameState else None,
        'palabrasInicial': gameState['palabrasInicial'],
        'cantidadPalabrasEncontradas': gameState['cantidadPalabrasEncontradas'],
        'palabrasEncontradas': gameState['palabrasEncontradas'],
        'palabrasHeptacrack': gameState['palabrasHeptacrack'],
        'heptacrackEncontrados': gameState['heptacrackEncontrados'],
        'tiempo': gameState['tiempo'],
        'ultimo_tiempo_guardado': gameState['ultimo_tiempo_guardado']
    }
    
    # Guardar en el archivo JSON
    with open(savePath, 'w', encoding='utf-8') as f:
        json.dump(saveData, f, ensure_ascii=False, indent=4)

def loadGame(username, gameType):
    """
    Carga el estado del juego desde un archivo JSON
    
    Args:
        username (str): Nombre del usuario
        gameType (str): Tipo de juego ("lexireto" o "letras")
    
    Returns:
        dict: Estado del juego cargado o None si no existe
    """
    savePath = f'saves/{username}_{gameType}.json'
    
    if not os.path.exists(savePath):
        return None
    
    try:
        with open(savePath, 'r', encoding='utf-8') as f:
            saveData = json.load(f)
        
        # Convertir la lista de palabras objetivo de vuelta a un set si existe
        if saveData.get('palabrasObjetivo'):
            saveData['palabrasObjetivo'] = set(saveData['palabrasObjetivo'])
        
        return saveData
    except Exception as e:
        print(f"Error al cargar la partida: {e}")
        return None

def hasSavedGame(username, gameType):
    """
    Verifica si existe un juego guardado para el usuario y tipo de juego especificados
    
    Args:
        username (str): Nombre del usuario
        gameType (str): Tipo de juego ("lexireto" o "letras")
    
    Returns:
        bool: True si existe un juego guardado, False en caso contrario
    """
    savePath = f'saves/{username}_{gameType}.json'
    return os.path.exists(savePath)

def printLexireto(letras, letraCentral, palabrasObjetivo, palabrasInicial):
    print(palabrasObjetivo)
    print(letras)
    print(letraCentral)
    print(palabrasInicial)

def generarLetrasMatrix(cantidad_palabras=None, filas=10, columnas=10, max_intentos=10):
    """
    Genera una sopa de letras con las palabras proporcionadas y devuelve:
    - Matriz de la sopa de letras.
    - Lista de palabras a buscar.
    - Diccionario de palabras agrupadas por longitud.
    - Cantidad total de palabras colocadas.

    Args:
        palabras (list): Lista de palabras a incluir.
        cantidad_palabras (int): Número de palabras a colocar. Si es None, usa todas.
        filas (int): Filas de la matriz. Default: 10.
        columnas (int): Columnas de la matriz. Default: 10.
        max_intentos (int): Intentos máximos por palabra antes de reemplazarla. Default: 10.

    Returns:
        tuple: (matriz, palabras_seleccionadas, palabras_por_longitud, total_palabras)
    """
    palabras = cargarDiccionario()
    if not cantidad_palabras:
        cantidad_palabras = len(palabras)
    
    palabras = [p.upper() for p in palabras if len(p) <= max(filas, columnas)]
    if len(palabras) < cantidad_palabras:
        raise ValueError(f"No hay suficientes palabras válidas (necesitas {cantidad_palabras}).")

    matriz = [[" " for _ in range(columnas)] for _ in range(filas)]
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha

    def colocar_palabra(matriz, palabra):
        """Intenta colocar una palabra en la matriz con backtracking."""
        posiciones = [(x, y) for x in range(filas) for y in range(columnas)]
        random.shuffle(posiciones)

        for x, y in posiciones:
            camino = []
            usado = set()
            if backtracking(matriz, palabra, x, y, 0, camino, usado):
                return True
        return False

    def backtracking(matriz, palabra, x, y, indice, camino, usado):
        """Backtracking recursivo para colocar letras."""
        if indice == len(palabra):
            return True
        if not (0 <= x < filas and 0 <= y < columnas):
            return False
        if matriz[x][y] != " " and (matriz[x][y] != palabra[indice] or (x, y) in usado):
            return False

        original = matriz[x][y]
        matriz[x][y] = palabra[indice]
        camino.append((x, y))
        usado.add((x, y))

        for dx, dy in direcciones:
            if backtracking(matriz, palabra, x + dx, y + dy, indice + 1, camino, usado):
                return True

        matriz[x][y] = original
        camino.pop()
        usado.remove((x, y))
        return False

    palabras_seleccionadas = []
    palabras_descartadas = []
    intentos_por_palabra = {}

    while len(palabras_seleccionadas) < cantidad_palabras and palabras:
        palabra = random.choice(palabras)
        if palabra not in intentos_por_palabra:
            intentos_por_palabra[palabra] = 0

        if intentos_por_palabra[palabra] >= max_intentos:
            palabras.remove(palabra)
            palabras_descartadas.append(palabra)
            del intentos_por_palabra[palabra]
            continue

        if colocar_palabra(matriz, palabra):
            palabras_seleccionadas.append(palabra)
            palabras.remove(palabra)  # Evitar repeticiones
            del intentos_por_palabra[palabra]
        else:
            intentos_por_palabra[palabra] += 1

    # Rellenar espacios vacíos
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == " ":
                matriz[i][j] = random.choice(letras)

    # Crear diccionario de palabras por longitud
    palabras_por_longitud = {}
    for palabra in palabras_seleccionadas:
        longitud = len(palabra)
        if longitud not in palabras_por_longitud:
            palabras_por_longitud[longitud] = []
        palabras_por_longitud[longitud].append(palabra)

    # Ordenar las palabras por longitud de forma descendente
    palabras_por_longitud = dict(sorted(palabras_por_longitud.items(), reverse=True))

    total_palabras = len(palabras_seleccionadas)

    return matriz, palabras_seleccionadas, palabras_por_longitud, total_palabras

def saveLetrasGame(username, gameState):
    """
    Guarda el estado del juego de letras en un archivo JSON
    
    Args:
        username (str): Nombre del usuario
        gameState (dict): Estado del juego a guardar
    """
    # Crear el directorio saves si no existe
    if not os.path.exists('saves'):
        os.makedirs('saves')
    
    # Ruta del archivo de guardado
    savePath = f'saves/{username}_letras.json'
    
    # Convertir el estado del juego a un formato serializable
    saveData = {
        'gameType': 'letras',
        'matriz': gameState['matriz'],
        'palabrasSeleccionadas': list(gameState['palabrasSeleccionadas']),
        'palabrasLongitud': gameState['palabrasLongitud'],
        'palabrasEncontradas': gameState['palabrasEncontradas'],
        'palabrasPorLongitud': gameState['palabrasPorLongitud'],
        'tiempo': gameState['tiempo'],
        'ultimo_tiempo_guardado': gameState['ultimo_tiempo_guardado']
    }
    
    # Guardar en el archivo JSON
    with open(savePath, 'w', encoding='utf-8') as f:
        json.dump(saveData, f, ensure_ascii=False, indent=4)

def loadLetrasGame(username):
    """
    Carga el estado del juego de letras desde un archivo JSON
    
    Args:
        username (str): Nombre del usuario
        
    Returns:
        dict: Estado del juego cargado o None si no existe
    """
    savePath = f'saves/{username}_letras.json'
    
    if os.path.exists(savePath):
        with open(savePath, 'r', encoding='utf-8') as f:
            savedGame = json.load(f)
            
        # Convertir la lista de palabras objetivo de nuevo a un set
        if 'palabrasSeleccionadas' in savedGame:
            savedGame['palabrasSeleccionadas'] = set(savedGame['palabrasSeleccionadas'])
            
        # Si no existe ultimo_tiempo_guardado, inicializarlo a 0
        if 'ultimo_tiempo_guardado' not in savedGame:
            savedGame['ultimo_tiempo_guardado'] = 0
            
        return savedGame
    return None

def updateStats(user, game, stat_type, value=1):
    """
    Actualiza las estadísticas de un usuario para un juego específico.
    
    Args:
        user (str): Nombre del usuario
        game (str): 'letras' o 'lexireto'
        stat_type (str): Tipo de estadística a actualizar
        value (int): Valor a sumar (por defecto 1)
    """
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if user in users:
        if 'stats' not in users[user]:
            users[user]['stats'] = {
                'letras': {
                    'palabras_acertadas': 0,
                    'victorias': 0,
                    'tiempo_jugado': 0,
                    'tiempo_promedio_victoria': 0,
                    'total_tiempo_victorias': 0
                },
                'lexireto': {
                    'palabras_acertadas': 0,
                    'victorias': 0,
                    'tiempo_jugado': 0,
                    'tiempo_promedio_victoria': 0,
                    'total_tiempo_victorias': 0,
                    'heptacracks': 0
                }
            }
        
        if stat_type in users[user]['stats'][game]:
            if stat_type == 'victorias':
                # Cuando hay una victoria, actualizamos el tiempo promedio
                users[user]['stats'][game]['total_tiempo_victorias'] += value
                users[user]['stats'][game]['victorias'] += 1
                # Calculamos el nuevo promedio
                users[user]['stats'][game]['tiempo_promedio_victoria'] = (
                    users[user]['stats'][game]['total_tiempo_victorias'] / 
                    users[user]['stats'][game]['victorias']
                )
            else:
                users[user]['stats'][game][stat_type] += value
            
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)

def getStats(user, game):
    """
    Obtiene las estadísticas de un usuario para un juego específico.
    
    Args:
        user (str): Nombre del usuario
        game (str): 'letras' o 'lexireto'
    
    Returns:
        dict: Estadísticas del usuario para el juego especificado
    """
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if user in users and 'stats' in users[user]:
        return users[user]['stats'][game]
    return None

def printLetras(palabras_seleccionadas, palabras_por_longitud, total_palabras):
    print(palabras_seleccionadas)
    print(palabras_por_longitud)
    print(total_palabras)
    return

def formatTime(seconds):
    """
    Formatea el tiempo en segundos a un formato legible.
    - Si es menos de un minuto: "Xs"
    - Si es menos de una hora: "Xmin Xs" (no muestra segundos si son 0)
    - Si es menos de un día: "Xh Xm" (no muestra minutos si son 0)
    - Si es más de un día: "Xd Xh" (no muestra horas si son 0)
    """
    if seconds == 0:
        return "0s"
    elif seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes}min"
        return f"{minutes}min {remaining_seconds}s"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes == 0:
            return f"{hours}h"
        return f"{hours}h {minutes}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        if hours == 0:
            return f"{days}d"
        return f"{days}d {hours}h"

