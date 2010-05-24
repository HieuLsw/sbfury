# Puede compilar este programa de dos maneras diferentes:
#
#    1 - Con aceleración de video mediante OpenGL.
#    2 - Sin aceleración de hardware usando SDL.
#
# Para generar estas versiones tiene que recompilar el programa
# alterando el valor de CFLAGS y LDFLAGS, aquí dos ejemplos:
#
#   * habilitar aceleración por hardware:
#
#	CFLAGS=`sdl-config --cflags` -DHAVE_OPENGL $(DEBUG)
#	LDFLAGS=`sdl-config --libs` -lSDL_image -lGL -lGLU
#
#   * deshabilitar aceleración por hardware, solo usar SDL:
#
#	CFLAGS=`sdl-config --cflags` -DHAVE_OPENGL $(DEBUG)
#	LDFLAGS=`sdl-config --libs` -lSDL_image -lGL -lGLU
#   	
# (note que los ejemplos podrían estar desactualizados...)

CC = g++
DEBUG=-ggdb3
CFLAGS=`sdl-config --cflags` -DHAVE_OPENGL $(DEBUG)
LDFLAGS=`sdl-config --libs` -lSDL_image -lGL -lGLU

CXXFLAGS=$(CFLAGS)

BINS=sbfury
OBJS= \
    director.o \
    scene.o \
    game.o \
    common.o \
    sprite.o \
    group.o \
    glSDL.o \
    shaolin.o \
    states.o \
    stage.o \
    shadow.o \
    animation.o \
    SDL_rotozoom.o \
    control.o \
    config.o \
    ninja.o \
    actor.o \
    enemy.o

all: $(BINS) 
sbfury: sbfury.o $(OBJS) 
clean:
	$(RM) *.o  $(BINS) *.exe
