import pygame
import utilities

def loginMenu(SCREEN, WIDTH, HEIGHT):
    running = True
    submenuRect, background, blurSurface = utilities.createSubmenu(WIDTH, HEIGHT, SCREEN, 400, 400)
    
    # Crear campos de texto
    inputFont = utilities.getMainFontBold(24)
    titleFont = utilities.getMainFontBold(32)
    errorFont = utilities.getMainFontBold(20)
    
    # Rectángulos para los campos de entrada
    usernameRect = pygame.Rect(submenuRect.x + 50, submenuRect.y + 120, 300, 40)
    passwordRect = pygame.Rect(submenuRect.x + 50, submenuRect.y + 200, 300, 40)
    
    # Botón para mostrar/ocultar contraseña
    showPasswordButton = pygame.Rect(passwordRect.right - 35, passwordRect.centery - 12, 24, 24)
    showPassword = False
    
    # Variables para almacenar el texto
    usernameText = ""
    passwordText = ""
    
    # Variables para controlar qué campo está activo
    activeInput = usernameRect
    
    # Variable para el mensaje de error
    showError = False

    # Diccionario de botones
    buttons = {
        "INICIAR SESIÓN": pygame.Rect(submenuRect.x + 50, passwordRect.y + 65, 300, 50),
        "REGISTRARSE": pygame.Rect(submenuRect.x + 50, passwordRect.y + 65 + 60, 300, 50)
    }

    # Colores de los botones
    buttonColors = {
        "INICIAR SESIÓN": (50, 147, 254),
        "REGISTRARSE": (66, 159, 121)
    }

    # Colores para los campos de entrada
    inputColors = {
        "active": (185, 185, 185),    # Color más oscuro para el campo activo
        "inactive": (255, 255, 255)   # Color blanco para el campo inactivo
    }
    
    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenu(submenuRect, background, blurSurface, SCREEN)
        
        # Dibujar título
        titleSurface = titleFont.render("INICIAR SESIÓN", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(submenuRect.centerx, submenuRect.y + 50))
        SCREEN.blit(titleSurface, titleRect)
        
        # Dibujar mensaje de error si es necesario
        if showError:
            errorSurface = errorFont.render("Usuario o contraseña incorrectos", True, (245, 77, 64))
            errorRect = errorSurface.get_rect(center=(submenuRect.centerx, passwordRect.y + 50))
            SCREEN.blit(errorSurface, errorRect)
        
        # Dibujar etiquetas
        usernameLabel = inputFont.render("Usuario:", True, (255, 255, 255))
        passwordLabel = inputFont.render("Contraseña:", True, (255, 255, 255))
        SCREEN.blit(usernameLabel, (usernameRect.x, usernameRect.y - 30))
        SCREEN.blit(passwordLabel, (passwordRect.x, passwordRect.y - 30))
        
        # Dibujar campos de entrada con colores según estén activos o no
        pygame.draw.rect(SCREEN, inputColors["active"] if activeInput == usernameRect else inputColors["inactive"], usernameRect, 2)
        pygame.draw.rect(SCREEN, inputColors["active"] if activeInput == passwordRect else inputColors["inactive"], passwordRect, 2)
        
        # Dibujar texto en los campos
        usernameSurface = inputFont.render(usernameText, True, (255, 255, 255))
        passwordSurface = inputFont.render("*" * len(passwordText) if not showPassword else passwordText, True, (255, 255, 255))
        SCREEN.blit(usernameSurface, (usernameRect.x + 5, usernameRect.y + 5))
        SCREEN.blit(passwordSurface, (passwordRect.x + 5, passwordRect.y + 5))
        
        # Dibujar botón de mostrar/ocultar contraseña
        pygame.draw.circle(SCREEN, (255, 255, 255), showPasswordButton.center, 12, 2)
        if showPassword:
            pygame.draw.circle(SCREEN, (255, 255, 255), showPasswordButton.center, 8)
        
        # Dibujar botones
        for text, rect in buttons.items():
            # Sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], rect, border_radius=10)
            # Texto
            text_surface = inputFont.render(text, True, (255, 255, 255))
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
                elif event.key == pygame.K_TAB:
                    # Cambiar entre campos con Tab
                    if activeInput == usernameRect:
                        activeInput = passwordRect
                    else:
                        activeInput = usernameRect
                elif event.key == pygame.K_RETURN:
                    # Intentar iniciar sesión al presionar Enter
                    if activeInput == usernameRect:
                        activeInput = passwordRect
                    elif usernameText and passwordText:
                        utilities.pressButton(buttons["INICIAR SESIÓN"], buttonColors["INICIAR SESIÓN"], SCREEN, inputFont, "INICIAR SESIÓN")
                        # Verificar credenciales
                        if utilities.logInUser(usernameText, passwordText):
                            running = False
                            return True # MainMenu
                        else:
                            showError = True
                elif event.key == pygame.K_BACKSPACE:
                    # Borrar caracteres
                    if activeInput == usernameRect:
                        usernameText = usernameText[:-1]
                    elif activeInput == passwordRect:
                        passwordText = passwordText[:-1]
                else:
                    # Agregar caracteres
                    if activeInput == usernameRect:
                        usernameText += event.unicode
                    elif activeInput == passwordRect:
                        passwordText += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
                elif showPasswordButton.collidepoint(MOUSE_POS):
                    showPassword = not showPassword
                elif usernameRect.collidepoint(MOUSE_POS):
                    activeInput = usernameRect
                elif passwordRect.collidepoint(MOUSE_POS):
                    activeInput = passwordRect
                elif buttons["INICIAR SESIÓN"].collidepoint(MOUSE_POS):
                    if usernameText and passwordText:
                        utilities.pressButton(buttons["INICIAR SESIÓN"], buttonColors["INICIAR SESIÓN"], SCREEN, inputFont, "INICIAR SESIÓN")
                        # Verificar credenciales
                        if utilities.logInUser(usernameText, passwordText):
                            running = False
                            return True
                        else:
                            showError = True
                elif buttons["REGISTRARSE"].collidepoint(MOUSE_POS):
                    utilities.pressButton(buttons["REGISTRARSE"], buttonColors["REGISTRARSE"], SCREEN, inputFont, "REGISTRARSE")
                    # Aquí iría la lógica para abrir el menú de registro
                    running = False
                    print("Abrir menú de registro")
                    if(registerMenu(SCREEN, WIDTH, HEIGHT)):
                        running = False
                        return True
                else:
                    activeInput = None

        pygame.display.flip()

def registerMenu(SCREEN, WIDTH, HEIGHT):
    running = True
    submenuRect, background = utilities.createSubmenuWithoutBlur(WIDTH, HEIGHT, SCREEN, 400, 450)
    
    # Crear campos de texto
    inputFont = utilities.getMainFontBold(24)
    titleFont = utilities.getMainFontBold(32)
    errorFont = utilities.getMainFontBold(20)
    
    # Rectángulos para los campos de entrada
    usernameRect = pygame.Rect(submenuRect.x + 50, submenuRect.y + 120, 300, 40)
    passwordRect = pygame.Rect(submenuRect.x + 50, submenuRect.y + 200, 300, 40)
    confirmPasswordRect = pygame.Rect(submenuRect.x + 50, submenuRect.y + 280, 300, 40)
    
    # Botón para mostrar/ocultar contraseña
    showPasswordButton = pygame.Rect(passwordRect.right - 35, passwordRect.centery - 12, 24, 24)
    showConfirmPasswordButton = pygame.Rect(confirmPasswordRect.right - 35, confirmPasswordRect.centery - 12, 24, 24)
    showPassword = False
    showConfirmPassword = False
    
    # Variables para almacenar el texto
    usernameText = ""
    passwordText = ""
    confirmPasswordText = ""
    
    # Variables para controlar qué campo está activo
    activeInput = usernameRect
    
    # Variable para el mensaje de error
    showError = False
    errorMessage = ""

    # Diccionario de botones
    buttons = {
        "REGISTRARSE": pygame.Rect(submenuRect.x + 50, confirmPasswordRect.y + 65, 300, 50)
    }

    # Colores de los botones
    buttonColors = {
        "REGISTRARSE": (66, 159, 121)
    }

    # Colores para los campos de entrada
    inputColors = {
        "active": (185, 185, 185),    # Color más oscuro para el campo activo
        "inactive": (255, 255, 255)   # Color blanco para el campo inactivo
    }
    
    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        utilities.blitSubmenuWithoutBlur(submenuRect, background, SCREEN)
        
        # Dibujar título
        titleSurface = titleFont.render("REGISTRARSE", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(submenuRect.centerx, submenuRect.y + 50))
        SCREEN.blit(titleSurface, titleRect)
        
        # Dibujar mensaje de error si es necesario
        if showError:
            errorSurface = errorFont.render(errorMessage, True, (245, 77, 64))
            errorRect = errorSurface.get_rect(center=(submenuRect.centerx, confirmPasswordRect.y + 50))
            SCREEN.blit(errorSurface, errorRect)
        
        # Dibujar etiquetas
        usernameLabel = inputFont.render("Usuario:", True, (255, 255, 255))
        passwordLabel = inputFont.render("Contraseña:", True, (255, 255, 255))
        confirmPasswordLabel = inputFont.render("Confirmar Contraseña:", True, (255, 255, 255))
        SCREEN.blit(usernameLabel, (usernameRect.x, usernameRect.y - 30))
        SCREEN.blit(passwordLabel, (passwordRect.x, passwordRect.y - 30))
        SCREEN.blit(confirmPasswordLabel, (confirmPasswordRect.x, confirmPasswordRect.y - 30))
        
        # Dibujar campos de entrada con colores según estén activos o no
        pygame.draw.rect(SCREEN, inputColors["active"] if activeInput == usernameRect else inputColors["inactive"], usernameRect, 2)
        pygame.draw.rect(SCREEN, inputColors["active"] if activeInput == passwordRect else inputColors["inactive"], passwordRect, 2)
        pygame.draw.rect(SCREEN, inputColors["active"] if activeInput == confirmPasswordRect else inputColors["inactive"], confirmPasswordRect, 2)
        
        # Dibujar texto en los campos
        usernameSurface = inputFont.render(usernameText, True, (255, 255, 255))
        passwordSurface = inputFont.render("*" * len(passwordText) if not showPassword else passwordText, True, (255, 255, 255))
        confirmPasswordSurface = inputFont.render("*" * len(confirmPasswordText) if not showConfirmPassword else confirmPasswordText, True, (255, 255, 255))
        SCREEN.blit(usernameSurface, (usernameRect.x + 5, usernameRect.y + 5))
        SCREEN.blit(passwordSurface, (passwordRect.x + 5, passwordRect.y + 5))
        SCREEN.blit(confirmPasswordSurface, (confirmPasswordRect.x + 5, confirmPasswordRect.y + 5))
        
        # Dibujar botones de mostrar/ocultar contraseña
        pygame.draw.circle(SCREEN, (255, 255, 255), showPasswordButton.center, 12, 2)
        pygame.draw.circle(SCREEN, (255, 255, 255), showConfirmPasswordButton.center, 12, 2)
        if showPassword:
            pygame.draw.circle(SCREEN, (255, 255, 255), showPasswordButton.center, 8)
        if showConfirmPassword:
            pygame.draw.circle(SCREEN, (255, 255, 255), showConfirmPasswordButton.center, 8)
        
        # Dibujar botón de registro
        for text, rect in buttons.items():
            # Sombra del botón
            shadow_button = pygame.Rect(rect.x, rect.y + 3, rect.width, rect.height)
            pygame.draw.rect(SCREEN, (30, 40, 42), shadow_button, border_radius=10)
            # Rectángulo del botón con su color específico
            pygame.draw.rect(SCREEN, buttonColors[text], rect, border_radius=10)
            # Texto
            text_surface = inputFont.render(text, True, (255, 255, 255))
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
                elif event.key == pygame.K_TAB:
                    # Cambiar entre campos con Tab
                    if activeInput == usernameRect:
                        activeInput = passwordRect
                    elif activeInput == passwordRect:
                        activeInput = confirmPasswordRect
                    else:
                        activeInput = usernameRect
                elif event.key == pygame.K_RETURN:
                    # Intentar registrar al presionar Enter
                    if activeInput == usernameRect:
                        activeInput = passwordRect
                    elif activeInput == passwordRect:
                        activeInput = confirmPasswordRect
                    elif usernameText and passwordText and confirmPasswordText:
                        if passwordText == confirmPasswordText:
                            utilities.pressButton(buttons["REGISTRARSE"], buttonColors["REGISTRARSE"], SCREEN, inputFont, "REGISTRARSE")
                            # Aquí iría la lógica para registrar el usuario
                            if utilities.registerUser(usernameText, passwordText):
                                running = False
                                return True
                            else:
                                showError = True
                                errorMessage = "El usuario ya existe"
                        else:
                            showError = True
                            errorMessage = "Las contraseñas no coinciden"
                elif event.key == pygame.K_BACKSPACE:
                    # Borrar caracteres
                    if activeInput == usernameRect:
                        usernameText = usernameText[:-1]
                    elif activeInput == passwordRect:
                        passwordText = passwordText[:-1]
                    elif activeInput == confirmPasswordRect:
                        confirmPasswordText = confirmPasswordText[:-1]
                else:
                    # Agregar caracteres
                    if activeInput == usernameRect:
                        usernameText += event.unicode
                    elif activeInput == passwordRect:
                        passwordText += event.unicode
                    elif activeInput == confirmPasswordRect:
                        confirmPasswordText += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not submenuRect.collidepoint(MOUSE_POS):
                    running = False
                elif showPasswordButton.collidepoint(MOUSE_POS):
                    showPassword = not showPassword
                elif showConfirmPasswordButton.collidepoint(MOUSE_POS):
                    showConfirmPassword = not showConfirmPassword
                elif usernameRect.collidepoint(MOUSE_POS):
                    activeInput = usernameRect
                elif passwordRect.collidepoint(MOUSE_POS):
                    activeInput = passwordRect
                elif confirmPasswordRect.collidepoint(MOUSE_POS):
                    activeInput = confirmPasswordRect
                elif buttons["REGISTRARSE"].collidepoint(MOUSE_POS):
                    if usernameText and passwordText and confirmPasswordText:
                        if passwordText == confirmPasswordText:
                            utilities.pressButton(buttons["REGISTRARSE"], buttonColors["REGISTRARSE"], SCREEN, inputFont, "REGISTRARSE")
                            # Aquí iría la lógica para registrar el usuario
                            if utilities.registerUser(usernameText, passwordText):
                                running = False
                                return True
                            else:
                                showError = True
                                errorMessage = "El usuario ya existe"
                        else:
                            showError = True
                            errorMessage = "Las contraseñas no coinciden"
                else:
                    activeInput = None

        pygame.display.flip()