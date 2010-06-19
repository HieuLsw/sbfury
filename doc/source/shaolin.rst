Shaolin, el protagonista
========================

Inicio
------

El personaje del videojuego se encuentra implementado en la
clase ``Shaolin`` dentro del directorio ``shaolin``.

El objeto que instancia al shaolin es la escena ``game`` dentro
de la función ``_create_player_and_stage``.

Estas son las lineas mas significativas:

.. code-block:: python

    shaolin_sprite = shaolin.shaolin.Shaolin()
    control_layer = control.Control(shaolin_sprite)

    
Control del personaje
---------------------

En el código anterior puedes ver que el objeto que se vincula
al shaolin es ``Control``, esto es así porque en realidad
quien determina los cambios de estado del shaolin es el propio
usuario.

El objeto control consulta el estado del teclado todo el tiempo
y cuando detecta un evento llama el método ``on_control_press`` del
shaolin.


Shaolin, una maquina de estados
-------------------------------

El personaje del juego tiene que realizar muchas acciones: caminar, 
correr, golpear, saltar... etc.

Para representar este comportamiento se ha optado por implementar
el patrón estratégia (el mismo que se utiliza para administrar escenas).

La idea es así, el personaje tiene un atributo que indica en qué
estado se encuentra. Inicialmente está en estado ``Stand``:

    class Shaolin(Sprite):

        def __init__(self):
            ...
            self.set_state(states.Stand(self))

entonces, a partir de ese momento lo que hace el personaje
depende de lo que le han asignado como estado.

Si el jugador pulsa una tecla, el objeto Shaolin recibe
la tecla pulsada y la envía directamente a su instancia
de objeto ``state`` para que la procese.

Entonces, por ejemplo, el estado ``Stand`` puede interpretar
una tecla como ``left`` para cambiar a otro estado, y así
lograr que el personaje camine cuando se pulsa una tecla.

Este es un código boceto de la clase ``Stand``:

.. code-block:: python

    class Stand(state):

        def __init__(self, shaolin):
            self.shaolin = shaolin
            self.shaolin.set_animation('stand')

        def on_control_press(self, map):
            if map.motion:
                new_state = Walk(self.shaolin, map)
                self.shaolin.set_state(new_state)

        def update(self, dt):
            # lo que tenga que hacer cuando esta parado.
            self.shaolin.update_animation(dt)


Es decir, los nuevos estados se pueden crear indicando el
objeto que manejan (en este caso shaolin) y luego llamando
al método ``set_state``.
