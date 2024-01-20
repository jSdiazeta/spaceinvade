import random

import pygame as pg
import random as ra

#Inicializacion de pygame
pg.init()

#Definicion de constantes
pantalla_Ancho = 800
pantalla_Alto = 600
valI = 800

#Tamño de la pantalla
pantalla = pg.display.set_mode((pantalla_Ancho, pantalla_Alto))

#Titulo e Icono del Juego
pg.display.set_caption("Space Invader")
icono = pg.image.load("hand.png")
pg.display.set_icon(icono)

#Configuracion de fondo y sonido
fondo = pg.image.load("15349.jpg")
mixer = pg.mixer
mixer.init()
mixer_musica = mixer.music
mixer.music.load("background.wav")
mixer.music.play(loops=-1)

#Carga de Imagenes
jugadorImg = pg.image.load("hand2.png")
num_de_enemigos = 2
enemigoImg = [pg.image.load(f"A1.png") for i in range(1, num_de_enemigos + 1)]
proyectilImg = pg.image.load("B2.png")
num_de_vidas = 2
vidasImg = [pg.image.load(f"pixel_ship_yellow.png") for i in range(1, num_de_vidas + 1)]

#Variables posicion y velocidad
#Jugador
jugadorX = 370
jugadorY = 460
jugadorX_cambio = 0
jugadorY_cambio = 0

#Enemigos
enemigoX = [ra.randint(0,736) for _ in range(num_de_enemigos)]
enemigoY = [ra.randint(50,150) for _ in range(num_de_enemigos)]
enemigoX_cambio = [1 for _ in range(num_de_enemigos)]
enemigoY_cambio = [100 for _ in range(num_de_enemigos)]

#Proyectiles
proyectilX = 0
proyectilY = 480
proyectilX_cambio = 0
proyectilY_cambio = 10
proyectil_estado = "listo"

#Puntuacion
puntaje_valor = 0
textoX = 10
textoY = 10

#Funcion para dibujar el jugador 
def jugador(x,y):
    pantalla.blit(jugadorImg, (x,y))

#Funcion para dibujar el enemigo
def enemigo(x,y,i):
    pantalla.blit(enemigoImg[i], (x,y))

#Funcion para disparar el proyectil
def disparo_proyectil(x,y):
    global proyectil_estado
    proyectil_estado = "disparar"
    pantalla.blit(proyectilImg, (x+16, y+10))

#Funcion para verificar colisiones
def esColision(enemigoX, enemigoY, proyectilX, proyectilY):
    distancia = ((enemigoX - proyectilX) ** 2 + (enemigoY - proyectilY) ** 2) ** 0.5
    return distancia < 27

#Fuentes
puntaje_fuente = pg.font.Font("freesansbold.ttf",32)
game_over_fuente = pg.font.Font("freesansbold.ttf",64)

#Funcion para mostrar el puntaje
def mostrar_puntaje(x,y):
    puntaje = puntaje_fuente.render(
        "puntaje: " + str(puntaje_valor), True, (244,255,51))
    pantalla.blit(puntaje, (x,y))

#Funcion para mostrar las vidas
def corazon(valI, y, i):
    for i in range(2):
        valI -= 100
        pantalla.blit(vidasImg[i], (valI,y))


#Funcion para mostrar el Game Over
def game_over_mensaje():
    game_over_mensaje = game_over_fuente.render(
        "PERDISTE", True, (94,11,86))
    pantalla.blit(game_over_mensaje,(200,250))

#Ciclo natural del juego
ejecutando = True
while ejecutando:
    pantalla.fill((0,0,0))
    pantalla.blit(fondo, (0,0))

    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            ejecutando = False
        
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_LEFT:
                jugadorX_cambio = -5
            if evento.key == pg.K_RIGHT:
                jugadorX_cambio = 5
            if evento.key == pg.K_SPACE:
                if proyectil_estado == "listo":
                    proyectil_Sound = mixer.Sound("laser.wav")
                    proyectil_Sound.play()
                    proyectilX = jugadorX
                    disparo_proyectil(proyectilX, proyectilY)
        
        elif evento.type == pg.KEYUP:
            if evento.key == pg.K_LEFT or evento.key == pg.K_RIGHT:
                jugadorX_cambio = 0
                
            
    #Validacion de los limites del jugador
    jugadorX += jugadorX_cambio
    if jugadorX <= 0:
        jugadorX = 0
    elif jugadorX >= 736:
        jugadorX = 736

    
    #Actulizacion de la posicion de los enemigos
    for i in range(num_de_enemigos):
        #Si el enemigo ha llegado al final del juego, se detiene el ciclo
        if enemigoY[i] > 440:
            if(num_de_vidas==0):
              for j in range(num_de_enemigos):
                  enemigoY[i] = 2000
                  game_over_mensaje()
              break
            else:
                enemigoX[i]=random.randint(0,736)
                enemigoY[i]=random.randint(50,150)
                num_de_vidas-=1
        #Actualizacion de la posicion horizontal del enemigo
        enemigoX[i] += enemigoX_cambio[i]
        if enemigoX[i] <= 0 or enemigoX[i] >= 736:
            enemigoX_cambio[i] *= -1
            enemigoY[i] += enemigoY_cambio[i]

        #Deteccion de colision entre enemigo y bala
        colision = esColision(
            enemigoX[i], enemigoY[i], proyectilX, proyectilY)
        if colision:
            #Reproduccion del sonido de la explosion y actualizacion del puntaje 
            explosionSonido = mixer.Sound("explosion.wav")
            explosionSonido.play()
            proyectilY = 480
            proyectil_estado = "listo"
            puntaje_valor += 1
            #Reubicacion aleatoria del enemigo despues de la ubicacion
            enemigoX[i] = ra.randint(0,736)
            enemigoY[i] = ra.randint(50,150)

        #Dibuja los enemigos
        enemigo(enemigoX[i], enemigoY[i], i)

    #Acutalizcion de la posicion de la bala
    if proyectilY <= 0 or proyectilX <= 0:
        proyectilY = 480
        proyectilX = 736
        proyectil_estado = "listo"
    #Dispara la bala si el estado es disparar
    if proyectil_estado == "disparar":
        disparo_proyectil(proyectilX,proyectilY)
        proyectilY -= proyectilY_cambio 
        proyectilX -= proyectilX_cambio
    
    #Actualizar vidas
    corazon(valI, 10, i)

    #Dibuja el jugador
    jugador(jugadorX, jugadorY)

    #Muestra el puntaje 
    mostrar_puntaje(textoX, textoY)
    
    #Actualiza la pantalla
    pg.display.update()