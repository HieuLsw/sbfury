# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from pyglet.gl import *
import cocos
import common
import config


class State:
    "Representa un estado de un personaje."

    def __init__(self, target):
        self.target = target

    def update(self, dt):
        pass

    def on_control_press(self, map):
        pass

    def on_control_release(self, map):
        pass

    def on_collision_send(self, other_sprite):
        pass

    def on_collision_receive(self, other_sprite, force):
        """Returns True if collision do something."""
        pass


class Sprite(cocos.sprite.Sprite):
    """Represena a un actor dentro del juego, un enemigo un protagonista.

    Los objetos dentro del juego heredan de esta clase, por lo que no
    verás instancias de la clase Sprite así como está. Sprite es una
    clase abstracta.
    """

    def __init__(self, image=None, must_be_updated=False, *args, **kwargs):

        # Si no se le indica una imagen asume que tiene que mostrar
        # una imagen predeterminada.
        if not image:
            image = common.load_image('none.png')

        super(Sprite, self).__init__(image, *args, **kwargs)
        self.set_collision(None)
        self.distance_to_floor = 0
        self.shadow = False
        self.move(0, 0)

        # Si es un objeto actualizable genera una tarea que lo actualiza.
        if must_be_updated:
            self.schedule(self.update)

    def update_animation(self, dt, repeat=True):
        "Actualiza el estado de la animación, retorna True si se termina o se reinicia."
        if self.animation.update(dt, self.flip, repeat=repeat):
            return True

        self.image = self.animation.image

    def set_frame(self, index):
        "Define el cuadro de animación"
        self.animation.set_frame(index, self.flip)
        self.image = self.animation.image

    def set_state(self, state):
        "Cambia el estado del personaje"
        self._state = state

    def update(self, dt):
        "Si es un objeto actualizable, aquí va el código de lógica."
        self._state.update(dt)

    def on_collision_receive(self, other_sprite, collision_force):
        "Callback que se llama cuando este objeto recibe una colisión."
        return self._state.on_collision_receive(other_sprite, collision_force)
        #print "I am are:", self, "\t\tand the other sprite are:", other_sprite

    def on_collision_send(self, other_sprite):
        "Se llama cuando una colision que emite este pesonaje efectivamente toca a otro."
        self._state.on_collision_send(other_sprite)
        #print "I am are:", self, "\t\tand i send a collision to:", other_sprite

    def set_collision(self, rect, force=1):
        """Define un area de colision para emitir una colisión.

            `rect`: tuple
                El area de colisión, relativa a donde se encuentra el personaje.
            `force`: int
                Fuerza que imprime la colisión, puede ser 1, 2, 3 o 4 (como máximo)."""

        self.rect_collision = rect

        if force in [1, 2, 3, 4]:
            self.collision_force = force
        else:
            raise ValueError("Collision force are not in [1, 4] range.")

    def draw(self):
        "Imprime al personaje sobre la pantalla."
        self.image.blit(self.x, self.y + self.distance_to_floor)

        if config.SHOW_CONTROL_POINTS:
            common.draw_point(self.x, self.y + self.distance_to_floor)

        if config.SHOW_COLLISION_BOXES and self.rect_collision:
            rect = self.get_rect_collision_world_position()
            common.draw_collision(*rect)

    def get_rect_collision_world_position(self):
        """Obtiene la posición efectiva de la emisión de colisión.

        Inicialmente la colisión es un rectángulo independiente, pero cuando
        se llama a esta función se pasa a tener un rectángulo asociado
        a la posición del personaje. Ya sea que esté en un parte del
        escenario o saltando.
        """
        x, y, w, h = self.rect_collision

        if self.flip:
            x += self.x - w
        else:
            x += self.x

        y += self.y + h +  self.distance_to_floor
        return x, y, w, h

    def move(self, dx, dy):
        "Mueve al personaje pero respetando los límites del escenario."
        x, y = self.position
        speed = 300
        to_x, to_y = x + speed * dx, y + speed * dy

        if to_y <= 10:
            to_y = 10
        elif to_y >= 230:
            to_y = 230

        if to_x <= 10:
            to_x = 10
        elif to_x >= 5200:
            to_x = 5200

        self.position = to_x, to_y

        if self.shadow:
            self.shadow.position = to_x, to_y + 1
            self.shadow.scale = (1 - self.distance_to_floor / 400.0)

    def get_collision_receive_area(self):
        "Obtiene el area que representa al personaje. Esta area es la que podría ser golpeada."
        w, h = self.image.width, self.image.height
        x, y = self.x, self.y + self.distance_to_floor
        return x - w / 2, y, w, h

if __name__ == '__main__':
    common.director.init(resizable=True)

    sprite = Sprite()
    sprite.position = 300, 300
    layer = cocos.layer.ColorLayer(100, 100, 100, 255)
    scene = cocos.scene.Scene(layer)
    layer.add(sprite)

    common.director.run(scene)
