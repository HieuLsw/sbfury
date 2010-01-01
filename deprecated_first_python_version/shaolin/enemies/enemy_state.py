# -*- coding: utf-8 -*-
# Copyright 2007 Hugo Ruscitti <hugoruscitti@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

from pygame.time import get_ticks
import common 

class NotImplemented(Exception):
    pass



class State:
    
    def __init__(self, player):
        #print "The new state is:", self.__class__
        self.player = player
        self.player.unset_collision()

    def update(self):
        raise NotImplemented('you must redefine "update" method')


class Stand(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('stand')

    def update(self):
        self.player.update_animation()
                
        if self.player.get_collision_receive():
            power, self.player.flip = self.player.get_collision_receive()

            if power == 1 or power == 3:
                self.player.change_state(HitStand(self.player))
            elif power == 2:
                self.player.change_state(HitStand(self.player, 2))
            else:
                self.player.change_state(HardHit(self.player))

            self.player.create_hit()



class Walk(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('walk')

    def update(self):
        self.player.update_animation()
        velocity = 5
        dx = 0
        dy = 0

        self.player.move(dx, dy)


class Run(State):

    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('run')

    def update(self):
        self.player.update_animation()
        velocity = 10
        self.player.move(dx, dy)

class AttackRun(State):
    
    def __init__(self, player, velocity):
        State.__init__(self, player)
        self.velocity = velocity
        player.animation.set_state('attackrun')
        self.player.update_animation()
        self.delay = 0
        common.audio.play('attack_run')


    def update(self):
        self.player.move(self.velocity, 0)
        self.player.set_collision(4)

        if self.delay == 0:
                
            if self.velocity > 0:
                self.velocity -= 2
            else:
                self.velocity += 2

            if self.velocity == 0:
                self.player.change_state(Stand(self.player))

            self.delay = 6
        else:
            self.delay -= 1


class HitStand(State):
    
    def __init__(self, player, number=1):
        State.__init__(self, player)
        player.animation.set_state('hitstand' + str(number))

        if self.player.flip:
            self.player.move(+2, 0)
        else:
            self.player.move(-2, 0)

        self.player.sensitive = False
        self.player.id.change_energy(-10)
        common.audio.play('punch1')

    def update(self):

        if self.player.update_animation():
            self.player.change_state(Stand(self.player))
            self.player.sensitive = True


class HardHit(State):
    
    def __init__(self, player, dy=-6, initial_dx=4):
        State.__init__(self, player)
        player.animation.set_state('hardhit')
        self.dy = dy
        self.initial_dy = dy
        self.player.sensitive = False
        self.player.id.change_energy(-15)
        common.audio.play('punch2')
        self.in_air = True
        #self.player.game.world.fps.slow()

        if player.flip:
            self.dx = abs(initial_dx)
        else:
            self.dx = - abs(initial_dx)

    def update(self):

        self.dy += 0.5
        self.player.dy += self.dy
        
        self.player.move(self.dx, 0)

        # si toca el suelo
        if self.player.dy > - self.initial_dy -1:
            self.in_air = False
            self.initial_dy += 1.9
            self.dy = self.initial_dy
            self.reduce_dx()

            if self.dx > 3 or self.dx < -3:
                common.audio.play('touch_flood')
                self.player.game.stage.do_camera_effect()

            if self.initial_dy > 1:
                common.audio.play('touch_flood')
                self.player.change_state(Ground(self.player))
                self.player.dy = 0
                return

        if self.in_air:
            self.player.update_animation()
        else:
            if self.dy < 0.0:
                frame = 3
            else:
                frame = 2

            flip = self.player.flip
            self.player.animation.step = frame
            self.player.image = self.player.animation.get_image(flip)


    def reduce_dx(self):
        try:
            self.dx -= (self.dx / abs(self.dx)) 
        except:
            self.dx = 0
        pass


    def deprecated_update_last(self):

        self.dy += 0.5
        self.player.dy += self.dy

        if self.player.flip:
            dx = 8
        else:
            dx = -8
        
        self.player.move(dx, 0)

        self.player.update_animation()

        if self.player.dy > - self.initial_dy -1:
            self.player.dy = 0
            self.player.change_state(Ground(self.player))


class Ground(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        self.delay = 50
        player.animation.set_state('ground')
        player.update_animation()
        self.player.sensitive = False

    def update(self):
        self.delay -= 1
        
        if self.delay < 1:
            self.player.change_state(GroundToStand(self.player))

class GroundToStand(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('groundtostand')


    def update(self):
        if self.player.update_animation():
            self.player.change_state(Stand(self.player))
            self.player.sensitive = True



class Attack(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        (last_tick, last_number) = player.last_attack

        if get_ticks() - last_tick < 300:
            number = last_number + 1
            if number > 4:
                number = 1
        else:
            number = 1

        self.collision_power = number
        player.animation.set_state('attack' + str(number))
        self.number = number

    
    def update(self):

        if self.player.update_animation():
            self.player.change_state(Stand(self.player))
        else:
            # si es el cuadro de animacion indicado genera una colision
            if self.player.animation.step == 1:
                self.player.set_collision(self.collision_power)
                if self.player.get_collision_send():
                    self.player.last_attack = (get_ticks(), self.number)
        

class Special(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('special')

    def update(self):
        if self.player.update_animation():
            self.player.change_state(Stand(self.player))
        else:
            self.player.set_collision(4, cw=150)

class Jump(State):
    
    def __init__(self, player, dy):
        State.__init__(self, player)
        self.dy = dy

    def advance_animation(self):
        self.player.animation.advance()
        flip = self.player.flip
        self.player.image = self.player.animation.get_image(flip)


class JumpWalk(Jump):
    
    def __init__(self, player, vx, dy=-12):
        Jump.__init__(self, player, dy)
        player.animation.set_state('jumpwalk')
        player.image = player.animation.get_image(player.flip)
        self.step = 0
        self.vx = vx
        self.initial_dy = dy
        self.state = self.when_jump

    def when_jump(self):
        if self.dy > -3:
            self.advance_animation()
            self.state = self.when_are_on_top

    def when_are_on_top(self):
        if self.dy > 3:
            self.advance_animation()
            self.state = self.when_fall

    def when_fall(self):
        if self.dy > - self.initial_dy - 1:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))

    def update(self):
        self.player.move(self.vx, 0)
        self.dy += 0.5
        self.player.dy += self.dy
        self.state()
    
        if self.dy > - self.initial_dy - 1:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))



class JumpStand(Jump):
    
    def __init__(self, player, dy=-12):
        Jump.__init__(self, player, dy)
        player.animation.set_state('jumpstand')
        self.step = 0
        self.state = self.when_jump
        self.player.image = self.player.animation.get_image(self.player.flip)
        self.initial_dy = dy

    def update(self):
        self.dy += 0.5
        self.player.dy += self.dy
        self.state()


    def when_start(self):
        if self.dy > -8:
            self.advance_animation()
            self.state = self.when_jump

    def when_jump(self):
        if self.dy > -3:
            self.advance_animation()
            self.state = self.when_are_on_top

    def when_are_on_top(self):
        if self.dy > 3:
            self.advance_animation()
            self.state = self.when_fall

    def when_fall(self):
        if self.dy > - self.initial_dy - 1:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))


class JumpRun(JumpWalk):
    
    def __init__(self, player, vx, dy=-12):
        JumpWalk.__init__(self, player, vx, dy)

    def update(self):
        self.player.move(self.vx, 0)
        self.dy += 0.5
        self.player.dy += self.dy
        self.state()


class AttackJump:

    def __init__(self, player):
        self.delay = 25
        self.player = player

    def update_collision_sender(self):

        self.player.animation.advance(repeat=False)
        self.player.image = self.player.animation.get_image(self.player.flip)

        if self.delay > 0:
            self.delay -= 1

            if self.player.animation.step == 1:
                self.player.set_collision(4, 20)
        else:
            self.player.unset_collision()
            first = self.player.animation.get_first_frame(self.player.flip)
            self.player.image = first


class AttackJumpStand(State, AttackJump):
    
    def __init__(self, player, dy, initial_dy):
        State.__init__(self, player)
        AttackJump.__init__(self, player)
        player.animation.set_state('attackjumpstand')
        self.dy = dy
        self.initial_dy = initial_dy


    def update(self):

        self.dy += 0.5
        self.player.dy += self.dy

        if self.dy > - self.initial_dy - 1:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))
            return

        self.update_collision_sender()


class AttackJumpWalk(State, AttackJump):
    
    def __init__(self, player, dy, initial_dy, vx):
        State.__init__(self, player)
        AttackJump.__init__(self, player)
        player.animation.set_state('attackjumpwalk')
        self.dy = dy
        self.initial_dy = initial_dy
        self.vx = vx

    def update(self):

        self.player.move(self.vx, 0)
        self.dy += 0.5
        self.player.dy += self.dy

        if self.dy > - self.initial_dy - 1:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))
            return

        self.update_collision_sender()


class AttackJumpRun(State):
    
    def __init__(self, player, dy, initial_dy, vx):
        State.__init__(self, player)
        player.animation.set_state('attackjumprun')
        self.dy = dy
        self.initial_dy = initial_dy
        self.vx = vx

    def update(self):
        self.player.move(self.vx, 0)
        self.dy += 0.5

        self.player.dy += self.dy

        if self.dy > - self.initial_dy - 1:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))
            return

        self.player.animation.advance(repeat=False)
        self.player.image = self.player.animation.get_image(self.player.flip)
        self.player.set_collision(4, 20)


class Taked(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('taked')
        player.update_animation()

    def update(self):
        self.player.update_animation()

class HitTaked(State):
    
    def __init__(self, player, continue_taked=True):
        State.__init__(self, player)
        player.animation.set_state('hittaked')
        self.continue_taked = continue_taked

    def update(self):

        if self.player.update_animation():

            if self.continue_taked:
                self.player.change_state(Taked(self.player))
            else:
                self.player.change_state(Stand(self.player))


class AttackTake(State):
    
    def __init__(self, player, enemy_taked, attack_counter, continue_taked=True):

        State.__init__(self, player)
        player.animation.set_state('attacktake')
        common.audio.play('punch1')
        self.player.create_hit()
        self.continue_taked = continue_taked
        self.enemy_taked = enemy_taked
        self.attack_counter = attack_counter

    def update(self):

        if self.player.update_animation():

            if self.continue_taked:
                self.player.change_state(Take(self.player, self.enemy_taked,
                    self.attack_counter))
            else:
                self.player.change_state(Stand(self.player))


class AttackTakeAndJump(State):
    
    def __init__(self, player, enemy_taked, attack_counter, dy=-7):
        State.__init__(self, player)
        player.animation.set_state('attacktake')
        common.audio.play('punch1')
        self.player.create_hit()
        self.enemy_taked = enemy_taked
        self.attack_counter = attack_counter
        self.initial_dy = dy
        self.dy = dy
        self.state = 0

    def update(self):
        self.player.update_animation()
        self.dy += 0.5
        self.player.dy += self.dy

        if self.player.flip:
            dx = -3
        else:
            dx = +3

        self.player.move(dx, 0)

        if self.state == 0:
            if self.dy > -3:
                self.state = 1
        else:
            if self.dy > - self.initial_dy - 1:
                self.player.dy = 0
                self.player.change_state(Stand(self.player))


class Throw(State):
    
    def __init__(self, player, last_flip):
        State.__init__(self, player)
        self.player.animation.set_state('throw')
        self.step = 0
        self.last_flip = last_flip
        common.audio.play('throw')

    def update(self):
        if self.player.animation.advance(repeat=False):
            self.step += 1

            if self.step > 2:
                self.player.flip = self.last_flip
                self.player.change_state(Stand(self.player))
        else:
            self.player.image = self.player.animation.get_image(self.player.flip)


class Throwed(State):
    
    def __init__(self, player, dy=-8):
        State.__init__(self, player)
        player.animation.set_state('throwed')
        self.dy = dy
        self.initial_dy = dy
        self.player.sensitive = False
        self.player.id.change_energy(-15)
        self.in_air = True

        if player.flip:
            self.dx = 6
        else:
            self.dx = -6

    def update(self):

        self.dy += 0.5
        self.player.dy += self.dy
        
        self.player.move(self.dx, 0)

        # si toca el suelo
        if self.player.dy > - self.initial_dy -1:
            self.in_air = False
            self.initial_dy += 1.9
            self.dy = self.initial_dy
            self.reduce_dx()

            if self.dx > 3 or self.dx < -3:
                common.audio.play('touch_flood')
                self.player.game.stage.do_camera_effect()

            if self.initial_dy > 1:
                common.audio.play('touch_flood')
                self.player.change_state(Ground(self.player))
                self.player.dy = 0
                return


        if self.in_air:
            self.player.update_animation()
        else:
            if self.dy < 0.0:
                frame = 3
            else:
                frame = 2

            flip = self.player.flip
            self.player.animation.step = frame
            self.player.image = self.player.animation.get_image(flip)


    def reduce_dx(self):
        try:
            self.dx -= (self.dx / abs(self.dx)) 
        except:
            self.dx = 0
        pass
