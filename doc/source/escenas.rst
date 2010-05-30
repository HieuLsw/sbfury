Escenas
=======

El juego se encuentra organizado por escenas, la presentación, el
menú principal, la pantalla de créditos... etc.

Las escenas están dentro del módulo ``scene`` y todas heredan
de la clase ``cocos.scece.Scene``.


Game
----

La escena ``Game`` carga un nivel y administra todos los personajes
y objetos para ese nivel.

Al iniciar el objeto ``Game`` se puede indicar el nivel
que tiene que cargar, por ejemplo::

.. code-block:: python

    next_scene = scene.game.Game(level=2)
    common.director.run(next_scene)
