import sprite

class Enemy(sprite.Sprite):

    def __init__(self, shaolin, must_be_updated=False):
        super(Enemy, self).__init__(must_be_updated=must_be_updated)
        self.flip = True
        self.shaolin = shaolin

    def set_ai_states(self, ai_states):
        "Define la rueda de estados que tiene que seguir el personaje (AI simple)."
        self.ai_states = ai_states
        self.i = 0

    def reset_ai_state(self):
        "Reinicia la rueda de estados, generalmente porque lo han golpeado."
        self.i = 0
        
    def _get_next_ai_state(self):
        "Retorna el siguiente estado de la rueda de AI."
        if self.i >= len(self.ai_states):
            self.i = 0

        next_state = self.ai_states[self.i]
        self.i += 1

        return next_state

    def go_to_next_ai_state(self):
        "Hace que el personaje siga las ordenes de la rueda de AI"
        next_state = self._get_next_ai_state()
        next_state.start()
        self.set_state(next_state)

    def update(self, dt):
        self._state.update(dt)

    def see_to_player(self):
        "Mira en la direccion del shaolin, esto simula que el personaje no pierde de vista al protagonista."
        self.flip = (self.shaolin.position[0] < self.position[0])

import fat
import hannia
