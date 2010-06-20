Enemies
=======

Los enemigos del juego son bastante similares al protagonista, tienen
estados, también varias animaciones e interactúan con el sistema
de colisiones.

Todos los enemigos están dentro del módulo ``enemies`` y hereda del
objeto ``Enemy``.


Inteligencia artíficial con una rueda de estados
------------------------------------------------

Para que los enemigos se muevan por el escenario y puedan
simular un comportamiento hostíl contra nuestro protagista se
ha optado por un enfoque simple:

    - cada enemigo tiene una lista de posibles estados.
    - el comportamiento del personaje es cumplir cada uno de esos estados en orden.
    - la cadena de estados se utiliza como una rueda, vuelve a comenzar cuando termina.

De esta forma, si quieremos un personaje que pelee mal, tendríamos que
armarle una cadena de estados acorde::

    comportamiento = [WalkToPlayer(), Wait(), WalkRandom(), Wait(), Punch()]

(lo anterior es un ejemplo conceptual solamente).


Un ejemplo
----------

Todos los enemigos que se generan tienen que tener esta lista circular
de estados para ejecutar. Esto se suele hacer en el mismo constructor
del personaje:

.. code-block:: python

    class SampleEnemy(enemy):

        def __init__(self):
            [...]
            self.set_ai_states([state.Wait(self, 1), state.WalkRandom(self, 1)])
            self.go_to_next_ai_state()


Luego, cada estado de la cadena tiene que hacer su tarea en un tiempo
determinado por el ultimo argumento, y cuando termina tiene que llamar
internamente a ``go_to_next_ai_state`` para seguir con el siguiente
estado.


Todos miran al shaolin
----------------------

Cuando se inicializa un enemigo dentro del método ``create_enemy`` de la
escena ``Game``, se le pasa al nuevo enemigo la referencia del shaolin. Esto
es útil porque permite a los enemigos conocer la posición del shaolin, tanto
para realizar movimientos mas acertados como para observarlo todo el
tiempo.
