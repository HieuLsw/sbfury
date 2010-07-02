Energia
=======

Cada uno de los personajes del juego tiene un atributo que
indica cual es su nivel de energia.

Cuando la energia de un enemigo llega a cero entonces muere. Mientras
que el protagonista solo pierde una vida.


El objeto EnergyIndicator
-------------------------

El objeto ``EnergyIndicator`` representa al visualizador de energia. Este
objeto se instancia dentro de la clase ``game``::

    def _create_player_and_stage(self):
        """Genera al personaje principal y al objeto Stage.

        [...]
        # Genera el indicador de energia
        self.messages.add(energy.EnergyIndicator(shaolin_sprite, 10, 470))


y para inicializar el objeto ``EnergyIndicator`` tiene que indicarle
un sprite para monitorizar. Este sprite se puede cambiar tocando el
atributo ``target``, pero en principio es buena idea asignarlo en
el constructor.

EnergyIndicator va a consultar el atributo ``energy`` y ``name`` para
representar la enegía correctamente.
