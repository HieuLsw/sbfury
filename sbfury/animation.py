# License: Public Domain
# Author: Hugo Ruscitti (http://www.losersjuegos.com.ar)
import sheet

class Animation:

    def __init__(self, sheet, delay, sequence, stop_when_finish=False):
        self.step_in_sequence = 0
        self.sheet = sheet
        self.delay = delay
        self.reset()
        self.sequence = sequence
        self.stop_when_finish = stop_when_finish

    def reset(self):
        self.delay_counter = 0

    def update(self):
        "Avanza en la animacion y retorna True si ha reiniciado."
        self.delay_counter += 0.1

        if self.delay_counter >= self.delay:
            self.reset()
            return self.next_frame()

    def Assign(self, sprite):
        self.sheet.Assign(sprite)

    def next_frame(self):
        "Avanza en la secuencia y retorna True si la animacion termina."
        was_restarted = False
        self.step_in_sequence += 1

        if self.step_in_sequence >= len(self.sequence):
            if self.stop_when_finish:
                self.step_in_sequence -= 1
            else:
                self.step_in_sequence = 0
                was_restarted = True

        frame_to_show = self.sequence[self.step_in_sequence]
        self.sheet.SetFrameIndex(frame_to_show)

        return was_restarted
