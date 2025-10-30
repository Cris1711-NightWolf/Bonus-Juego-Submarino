## 🎮 Aventura Submarina - Juego Multihilo con Sincronización

https://img.shields.io/badge/Python-3.8%252B-blue

https://img.shields.io/badge/Pygame-2.0%252B-green

https://img.shields.io/badge/Threading-Synchronized-orange

Un juego submarino desarrollado en Python que demuestra el uso avanzado de hilos, mutex, semáforos y secciones críticas para la sincronización de procesos concurrentes.

------------

## 🚀 Características Principales

- ✅ Programación multihilo para generación y movimiento de obstáculos
- ✅ Sincronización con Mutex para proteger recursos compartidos
- ✅ Variables de condición como semáforos controlados
- ✅ Secciones críticas para acceso seguro a datos
- ✅ 3 niveles de dificultad configurables
- ✅ Sistema de vidas, puntos y niveles progresivos
- ✅ Menús interactivos y controles intuitivos

------------

## 🎯 Capturas del Juego

### 1. 🏠 Menú Principal

![Menú Principal](https://github.com/Cris1711-NightWolf/Bonus-Juego-Submarino/blob/main/Pantallazos/menu_principal.png?raw=true)

Selecciona dificultad con 1, 2, 3 y confirma con ESPACIO

### 2. 🎮 Juego en Acción

![Juego Pincipal](https://github.com/Cris1711-NightWolf/Bonus-Juego-Submarino/blob/main/Pantallazos/juego_activo.png?raw=true)

Controla el submarino con las flechas y esquiva obstáculos

### 3. ⏸️ Menú de Pausa

![Menú de Pausa](https://github.com/Cris1711-NightWolf/Bonus-Juego-Submarino/blob/main/Pantallazos/menu_pausa.png?raw=true)

Pausa el juego con P y reinicia con R

### 4. 🎯 Pantalla de Game Over

![Game Over](https://github.com/Cris1711-NightWolf/Bonus-Juego-Submarino/blob/main/Pantallazos/game_over.png?raw=true)

Reinicia con R, vuelve al menú con M, o sale con ESC

------------

## 🛠️ Tecnologías y Conceptos de Sincronización

### 🔧 Stack Tecnológico

- Python 3.8+ - Lenguaje de programación
- Pygame - Librería para desarrollo de juegos
- Threading - Módulo para programación concurrente

------------

## 🔄 Mecanismos de Sincronización Implementados

#### 1. Mutex (Exclusion Mutua)

    mutex = threading.Lock()
    
    with mutex:
        for obstaculo in obstaculos:
            if obstaculo['tipo'] == 'medusa':
                screen.blit(img_obstaculo, obstaculo['rect'].topleft)

Función: Protege el acceso concurrente a la lista compartida de obstáculos durante el renderizado, evitando condiciones de carrera.

#### 2. Variables de Condición (Condition) - Semáforos Controlados



    condicion = threading.Condition(mutex)
    
    with condicion:
        if not pausado and juego_activo and estado_juego == JUGANDO:
            obstaculos.append({...})
            condicion.notify()
    
    with condicion:
        while not obstaculos and juego_activo and estado_juego == JUGANDO:
            condicion.wait()

Función: Actúa como semáforo que permite la comunicación entre hilos. El hilo consumidor espera hasta que el productor genere nuevos obstáculos.

#### 3. Secciones Críticas



    def mover_obstaculos():
        while juego_activo:
            with condicion:
    
    for obstaculo in obstaculos[:]:
                    obstaculo['rect'].move_ip(0, obstaculo['velocidad'])
    
    if obstaculo['rect'].colliderect(player):
                        vidas -= 1
    obstaculos.remove(obstaculo)

Función: Garantiza que las operaciones sobre datos compartidos (lista de obstáculos, vidas) se ejecuten atómicamente.
