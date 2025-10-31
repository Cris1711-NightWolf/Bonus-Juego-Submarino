import pygame
import threading
import random
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aventura Submarina - Esquiva los Obstáculos")

fondo = pygame.image.load("fondo_marino.png")
fondo = pygame.transform.scale(fondo, (800, 600))

img_player = pygame.image.load("submarino.png")
img_player = pygame.transform.scale(img_player, (60, 40))

img_player_flipped = pygame.transform.flip(img_player, True, False)

img_obstaculo = pygame.image.load("medusa.png")
img_obstaculo = pygame.transform.scale(img_obstaculo, (45, 45))

img_tiburon_original = pygame.image.load("tiburon.png")
img_tiburon_original = pygame.transform.scale(img_tiburon_original, (45, 35))
img_obstaculo2 = pygame.transform.rotate(img_tiburon_original, -90)

MENU = 0
JUGANDO = 1
GAME_OVER = 2

estado_juego = MENU
dificultad = "medio"
player_direccion = "derecha"

player = pygame.Rect(370, 500, 60, 40)

obstaculos = []

mutex = threading.Lock()
condicion = threading.Condition(mutex)

vidas = 5
puntos = 0
juego_activo = True
pausado = False
nivel = 1

font = pygame.font.SysFont(None, 36)
font_grande = pygame.font.SysFont(None, 64)
font_chica = pygame.font.SysFont(None, 28)

def configurar_dificultad(diff):
    """Configura los parámetros según la dificultad"""
    global vidas
    if diff == "facil":
        return 5, 2, 3, 0.5
    elif diff == "medio":
        return 4, 3, 5, 0.3
    else:
        return 3, 4, 7, 0.2

def reiniciar_juego():
    """Reinicia todas las variables del juego"""
    global vidas, puntos, nivel, obstaculos, player, pausado, player_direccion
    vidas, _, _, _ = configurar_dificultad(dificultad)
    puntos = 0
    nivel = 1
    obstaculos.clear()
    player.x, player.y = 370, 500
    pausado = False
    player_direccion = "derecha"

def generar_obstaculos():
    """Hilo que genera obstáculos periódicamente"""
    global juego_activo, pausado, nivel, dificultad
    while juego_activo:
        _, vel_min, vel_max, tiempo_gen = configurar_dificultad(dificultad)
        tiempo_espera = max(0.1, tiempo_gen - (nivel * 0.05))
        time.sleep(tiempo_espera)
        with condicion:
            if not pausado and juego_activo and estado_juego == JUGANDO:
                if random.random() < 0.6:
                    obstaculos.append({
                        'rect': pygame.Rect(random.randint(0, 755), -60, 45, 45),
                        'tipo': 'medusa',
                        'velocidad': vel_min + nivel
                    })
                else:
                    obstaculos.append({
                        'rect': pygame.Rect(random.randint(0, 755), -60, 35, 45),
                        'tipo': 'tiburon', 
                        'velocidad': vel_max + nivel
                    })
                condicion.notify()

def mover_obstaculos():
    """Hilo que mueve obstáculos hacia abajo"""
    global juego_activo, vidas, puntos, pausado, nivel, estado_juego
    while juego_activo:
        with condicion:
            while not obstaculos and juego_activo and estado_juego == JUGANDO:
                condicion.wait()
            if not pausado and juego_activo and estado_juego == JUGANDO:
                for obstaculo in obstaculos[:]:
                    obstaculo['rect'].move_ip(0, obstaculo['velocidad'])
                    
                    if obstaculo['rect'].y > 600:
                        obstaculos.remove(obstaculo)
                        puntos += 1
                        if puntos % 10 == 0:
                            nivel += 1

                for obstaculo in obstaculos[:]:
                    if obstaculo['rect'].colliderect(player):
                        vidas -= 1
                        obstaculos.remove(obstaculo)
                        if vidas <= 0:
                            estado_juego = GAME_OVER
                            break
        time.sleep(0.03)

def dibujar_menu():
    """Dibuja el menú principal"""
    screen.blit(fondo, (0, 0))
    
    titulo = font_grande.render("AVENTURA SUBMARINA", True, (0, 255, 255))
    screen.blit(titulo, (150, 100))
    
    y_pos = 250
    dificultades = ["facil", "medio", "dificil"]
    colores = {
        "facil": (0, 255, 0),
        "medio": (255, 255, 0), 
        "dificil": (255, 0, 0)
    }
    
    for diff in dificultades:
        color = colores[diff] if diff != dificultad else (255, 255, 255)
        texto = font.render(f"{diff.upper()} - {configurar_dificultad(diff)[0]} vidas", True, color)
        rect = texto.get_rect(center=(400, y_pos))
        screen.blit(texto, rect)
        y_pos += 60
    
    instrucciones = font_chica.render("Selecciona dificultad con 1, 2, 3 y presiona ESPACIO para jugar", True, (255, 255, 255))
    screen.blit(instrucciones, (150, 500))

def dibujar_game_over():
    """Dibuja la pantalla de game over"""
    screen.fill((0, 0, 50))
    
    texto_final = font_grande.render("¡JUEGO TERMINADO!", True, (255, 0, 0))
    screen.blit(texto_final, (180, 150))
    
    texto_puntos = font.render(f"Puntos finales: {puntos}", True, (255, 255, 255))
    screen.blit(texto_puntos, (300, 250))
    
    texto_nivel = font.render(f"Nivel alcanzado: {nivel}", True, (255, 255, 255))
    screen.blit(texto_nivel, (290, 300))
    
    texto_reiniciar = font.render("Presiona R para volver a jugar", True, (0, 255, 255))
    screen.blit(texto_reiniciar, (250, 400))
    
    texto_menu = font.render("Presiona M para volver al menú", True, (255, 255, 0))
    screen.blit(texto_menu, (250, 450))
    
    texto_salir = font.render("Presiona ESC para salir", True, (255, 100, 100))
    screen.blit(texto_salir, (280, 500))

threading.Thread(target=generar_obstaculos, daemon=True).start()
threading.Thread(target=mover_obstaculos, daemon=True).start()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if estado_juego == MENU:
                if event.key == pygame.K_1:
                    dificultad = "facil"
                elif event.key == pygame.K_2:
                    dificultad = "medio"
                elif event.key == pygame.K_3:
                    dificultad = "dificil"
                elif event.key == pygame.K_SPACE:
                    reiniciar_juego()
                    estado_juego = JUGANDO
                    
            elif estado_juego == JUGANDO:
                if event.key == pygame.K_p:
                    pausado = not pausado
                elif event.key == pygame.K_r and pausado:
                    reiniciar_juego()
                    
            elif estado_juego == GAME_OVER:
                if event.key == pygame.K_r:
                    reiniciar_juego()
                    estado_juego = JUGANDO
                elif event.key == pygame.K_m:
                    estado_juego = MENU
                elif event.key == pygame.K_ESCAPE:
                    running = False

    if estado_juego == MENU:
        dibujar_menu()
        
    elif estado_juego == JUGANDO:
        keys = pygame.key.get_pressed()
        if not pausado:
            if keys[pygame.K_LEFT] and player.left > 0:
                player.move_ip(-7, 0)
                player_direccion = "izquierda"
            if keys[pygame.K_RIGHT] and player.right < 800:
                player.move_ip(7, 0)
                player_direccion = "derecha"
            if keys[pygame.K_UP] and player.top > 0:
                player.move_ip(0, -5)
            if keys[pygame.K_DOWN] and player.bottom < 600:
                player.move_ip(0, 5)

        screen.blit(fondo, (0, 0))
        
        if player_direccion == "derecha":
            screen.blit(img_player, player.topleft)
        else:
            screen.blit(img_player_flipped, player.topleft)
        
        with mutex:
            for obstaculo in obstaculos:
                if obstaculo['tipo'] == 'medusa':
                    screen.blit(img_obstaculo, obstaculo['rect'].topleft)
                else:
                    screen.blit(img_obstaculo2, obstaculo['rect'].topleft)

        texto_vidas = font.render(f"Vidas: {vidas}", True, (255, 255, 255))
        screen.blit(texto_vidas, (20, 20))

        texto_puntos = font.render(f"Puntos: {puntos}", True, (255, 255, 255))
        screen.blit(texto_puntos, (20, 60))

        texto_nivel = font.render(f"Nivel: {nivel}", True, (255, 255, 255))
        screen.blit(texto_nivel, (20, 100))
        
        texto_dificultad = font.render(f"Dificultad: {dificultad.upper()}", True, (255, 255, 255))
        screen.blit(texto_dificultad, (20, 140))

        if pausado:
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            texto_pausa = font_grande.render("PAUSA", True, (255, 0, 0))
            screen.blit(texto_pausa, (320, 200))
            
            texto_continuar = font.render("Presiona P para continuar", True, (255, 255, 255))
            screen.blit(texto_continuar, (270, 300))
            
            texto_reiniciar = font.render("Presiona R para reiniciar", True, (255, 255, 255))
            screen.blit(texto_reiniciar, (275, 350))
            
    elif estado_juego == GAME_OVER:
        dibujar_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
