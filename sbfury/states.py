# -*- coding: utf-8 -*-
import time


def get_ticks():
    return time.time()




class State:
    
    def __init__(self, player):
        #print "The new state is:", self.__class__
        self.player = player
        #self.player.unset_collision()

    def update(self, dt):
        raise Exception('you must redefine "update" method')


class Stand(State):
    
    def __init__(self, player, animate_bandage=True):
        State.__init__(self, player)
        player.set_animation('stand')

        '''
        if animate_bandage:
            player.bandage.set_state('tostand')
        else:
            player.bandage.set_state('stand')
        '''

    def update(self, dt):
        self.player.update_animation(dt)
        c = self.player.control

        if c.left or c.right or c.up or c.down:
            self.player.change_state(Walk(self.player))

        if c.attack:
            self.player.change_state(Attack(self.player, False))
        elif c.jump:
            self.player.change_state(JumpStand(self.player))

        #self.player.check_collision_receive();
                

class Walk(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        player.set_animation('walk')
        c = player.control

        '''
        if c.left or c.right:
            self.impulse_bandage_when_walk = True
            player.bandage.set_state('towalk')
        else:
            self.impulse_bandage_when_walk = False
            player.bandage.set_state('stand')
        '''

    def update(self, dt):
        c = self.player.control
        self.player.update_animation(dt)
        velocity = 300 * dt
        dx = 0
        dy = 0

        '''
        if self.player.do_fall_if_are_in_air():
            return
        '''
        
        if c.run:
            self.player.change_state(Run(self.player))
            return
        
        if c.attack:
            self.player.change_state(Attack(self.player, True))
            return

        if c.left:
            dx = -velocity
            self.player.set_flip(True)
        elif c.right:
            dx = velocity
            self.player.set_flip(False)

        # ensure that bandage follow the player walk motion
        '''
        if not self.impulse_bandage_when_walk and (c.left or c.right):
            self.impulse_bandage_when_walk = True
            self.player.bandage.set_state("towalk")
        '''

        if c.up:
            dy = -velocity
        elif c.down:
            dy = velocity

        '''
        # Intenta sujetar a los enemigos
        if c.up or c.down:
            enemy_to_take = self.player.get_collision_to_take_enemies(dy)

            if enemy_to_take:
                self.player.change_state(Take(self.player, enemy_to_take))
                return
        '''

        self.player.move(dx, dy)

        if c.jump:
            if dx > 0:
                self.player.change_state(JumpWalk(self.player, 1))
            else:
                self.player.change_state(JumpWalk(self.player, -1))

        if not (c.up or c.down or c.left or c.right):
            self.player.change_state(Stand(self.player))
            #self.player.change_state(Stand(self.player, self.impulse_bandage_when_walk))

        #self.player.check_collision_receive();


class Run(State):

    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('run')
        player.bandage.set_state('run')

    def update(self):
        self.player.update_animation()
        velocity = 10
        c = self.player.control

        if self.player.do_fall_if_are_in_air():
            return

        if c.left:
            dx = -velocity
            self.player.flip = True
        elif c.right:
            dx = velocity
            self.player.flip = False
        else:
            self.player.change_state(Stand(self.player))
            return
        
        if c.up:
            dy = - velocity + 3
        elif c.down:
            dy = velocity - 3
        else:
            dy = 0
    
        self.player.move(dx, dy)

        if c.attack:
            self.player.change_state(AttackRun(self.player, dx))

        if c.jump:
            self.player.change_state(JumpRun(self.player, dx))

        self.player.check_collision_receive();

class AttackRun(State):
    
    def __init__(self, player, velocity):
        State.__init__(self, player)
        self.velocity = velocity
        player.animation.set_state('attackrun')
        player.bandage.set_state('attackrun')
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

        if self.player.do_fall_if_are_in_air():
            return


class HitStand(State):
    
    def __init__(self, player, number=1):
        State.__init__(self, player)
        player.animation.set_state('hitstand' + str(number))

        if self.player.flip:
            self.player.move(+2, 0)
        else:
            self.player.move(-2, 0)

        self.player.sensitive = False
        self.player.bandage.set_state('towalk')
        self.player.energy_model.change_energy(-10)
        player.update_animation()

    def update(self):

        if self.player.update_animation():
            self.player.change_state(Stand(self.player, True))
            self.player.sensitive = True


class HardHit(State):
    
    def __init__(self, player, dy=-6, initial_dx=4):
        State.__init__(self, player)
        player.animation.set_state('hardhit')
        player.update_animation()
        player.bandage.set_state('hardhit')
        player.bandage.update_animation()
        self.dy = dy
        self.initial_dy = dy
        self.player.sensitive = False
        self.player.energy_model.change_energy(-15)
        self.in_air = True

        if player.flip:
            self.dx = abs(initial_dx)
        else:
            self.dx = -abs(initial_dx)

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
            self.player.bandage.update_animation()
        else:
            if self.dy < 0.0:
                frame = 1
            else:
                frame = 0

            flip = self.player.flip
            self.player.animation.step = frame
            self.player.image = self.player.animation.get_image(flip)


    def reduce_dx(self):
        try:
            self.dx -= (self.dx / abs(self.dx)) 
        except:
            self.dx = 0
        pass


class Ground(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        self.delay = 50
        player.animation.set_state('ground')
        player.bandage.set_state('ground')
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
        self.player.sensitive = True

        if self.player.update_animation():
            self.player.change_state(Stand(self.player))
            self.player.sensitive = True


class Attack(State):
    
    def __init__(self, player, animate_bandage=True):
        State.__init__(self, player)
        (last_tick, last_number) = player.last_attack

        if get_ticks() - last_tick < 300:
            number = last_number + 1
            if number > 4:
                number = 1
        else:
            number = 1

        self.collision_power = number
        player.set_animation('attack%d' %(number))
        self.number = number

        '''
        if animate_bandage:
            player.bandage.set_state('tostand')
        else:
            player.bandage.set_state('stand')
        '''
    
    def update(self, dt):
        c = self.player.control

        if c.special:
            self.player.change_state(Special(self.player))
            return

        if self.player.update_animation(dt):
            self.player.change_state(Stand(self.player, False))
        else:
            # si es el cuadro de animacion indicado genera una colision
            '''
            if self.player.animation.step == 1:
                self.player.set_collision(self.collision_power)
                if self.player.get_collision_send():
                    self.player.last_attack = (get_ticks(), self.number)
            '''
        

class Special(State):
    
    def __init__(self, player, dy=-8):
        State.__init__(self, player)
        player.animation.set_state('special')
        self.initial_dy = dy
        self.dy = dy

        if player.flip:
            self.dx = +2
        else:
            self.dx = -2

    def update(self):
        self.dy += 0.5
        self.player.dy += self.dy
        self.player.move(self.dx, 0)

        if self.dy > -self.initial_dy - 1:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))
        else:
            self.player.update_animation()
            self.player.set_collision(5, cw=150)


class Starting(State):

    def __init__(self, player, dy=-8):
        State.__init__(self, player)
        player.set_animation('starting')
        #player.bandage.set_state('starting')
        self.dy = -200
        self.d = 0

    def update(self, dt):
        self.player.update_animation(dt)
        self.player.dy = self.dy
        self.d += dt * 2
        self.dy += self.d

        if self.dy > 0:
            self.player.dy = 0
            self.player.change_state(Stand(self.player))


        self.player.dy += self.dy
        self.dy += 0.5

class Jump(State):
    
    def __init__(self, player, dy):
        State.__init__(self, player)
        self.dy = dy

    '''
    def advance_animation(self):
        self.player.animation.advance()
        flip = self.player.flip
        self.player.image = self.player.animation.get_image(flip)
    '''

    def update(self, dt):
        speed = dt * 100
        self.soft_dx = 0
        self.soft_dy = 0

        self.dy += dt * 15
        self.player.dy += self.dy

        if self.player.control.left:
            self.soft_dx = -speed
        elif self.player.control.right:
            self.soft_dx = speed

        if self.player.control.up:
            self.soft_dy = -speed
        elif self.player.control.down:
            self.soft_dy = speed

        self.player.move(self.soft_dx, self.soft_dy)

        if self.player.are_in_flood():
            self.player.change_state(Stand(self.player))

class JumpWalk(Jump):
    
    def __init__(self, player, vx, dy=-4.0):
        Jump.__init__(self, player, dy)
        player.set_animation('jumpwalk')
        #player.bandage.set_state('jumpstand')
        #player.image = player.animation.get_image(player.flip)
        self.step = 0
        self.vx = vx
        self.initial_dy = dy
        self.state = self.when_jump
        #self.player.bandage.update_animation()

    def when_jump(self):
        if self.dy > -3:
            #self.advance_animation()
            self.state = self.when_are_on_top
            #self.player.bandage.update_animation()

    def when_are_on_top(self):
        if self.dy > 3:
            #self.advance_animation()
            self.state = self.when_fall
            #self.player.bandage.update_animation()

    def when_fall(self):
        if self.player.are_in_flood():
            self.player.change_state(Stand(self.player))

    def update(self, dt):
        Jump.update(self, dt)
        self.player.move((self.vx * 200) * dt, 0)
        #self.dy += 0.5
        #self.player.dy += self.dy
        self.state()
    
        if self.player.control.attack:
            p = self.player
            dy = self.dy
            idy = self.initial_dy
            self.player.change_state(AttackJumpWalk(p, dy, idy, self.vx))


class JumpStand(Jump):
    
    def __init__(self, player, dy=-4.5):
        Jump.__init__(self, player, dy)
        player.set_animation('jumpstand')
        #player.bandage.set_state('jumpstand')
        self.step = 0
        self.state = self.when_jump
        #self.player.bandage.update_animation()
        #self.player.image = self.player.animation.get_image(self.player.flip)
        self.initial_dy = dy

    def update(self, dt):
        '''
        Jump.update(self, dt)
        self.dy += dt * 10
        self.player.dy += self.dy
        self.state()

        if self.player.control.attack:
            p = self.player
            dy = self.dy
            idy = self.initial_dy
            self.player.change_state(AttackJumpStand(p, dy, idy))
        '''
        Jump.update(self, dt)

    def when_jump(self):
        if self.dy > -3:
            #self.advance_animation()
            #self.player.bandage.update_animation()
            self.state = self.when_are_on_top

    def when_are_on_top(self):
        if self.dy > 3:
            #self.advance_animation()
            #self.player.bandage.update_animation()
            self.state = self.when_fall

    def when_fall(self):
        if self.player.are_in_flood():
            self.player.change_state(Stand(self.player))

class JumpRun(JumpWalk):
    
    def __init__(self, player, vx, dy=-4.5):
        JumpWalk.__init__(self, player, vx, dy)

    def update(self):
        self.player.move(self.vx, 0)
        #self.dy += 0.5
        #self.player.dy += self.dy
        self.state()

        if self.player.control.attack:
            p = self.player
            dy = self.dy
            idy = self.initial_dy
            self.player.change_state(AttackJumpRun(p, dy, idy, self.vx))


class AttackJump(State):

    def __init__(self, player):
        State.__init__(self, player)
        self.delay = 25
        self.player = player
        player.bandage.set_state('walk')

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

    def update(self):

        self.player.move(self.vx, 0)
        self.dy += 0.5
        self.player.dy += self.dy

        self.update_collision_sender()
        
        if self.player.do_stand_if_are_in_flood():
            return


class AttackJumpStand(AttackJump):
    
    def __init__(self, player, dy, initial_dy):
        AttackJump.__init__(self, player)
        player.animation.set_state('attackjumpstand')
        player.bandage.set_state('walk')
        self.dy = dy
        self.initial_dy = initial_dy
        self.vx = 0


class AttackJumpWalk(AttackJump):
    
    def __init__(self, player, dy, initial_dy, vx):
        AttackJump.__init__(self, player)
        player.animation.set_state('attackjumpwalk')
        self.dy = dy
        self.initial_dy = initial_dy
        self.vx = vx


class AttackJumpRun(State):
    
    def __init__(self, player, dy, initial_dy, vx):
        State.__init__(self, player)
        player.animation.set_state('attackjumprun')
        player.bandage.set_state('walk')
        self.dy = dy
        self.initial_dy = initial_dy
        self.vx = vx

    def update(self):
        self.player.move(self.vx, 0)
        self.dy += 0.5

        self.player.dy += self.dy

        if self.player.do_stand_if_are_in_flood():
            self.player.dy = 0
            self.player.change_state(Stand(self.player))
            return

        self.player.animation.advance(repeat=False)
        self.player.image = self.player.animation.get_image(self.player.flip)
        self.player.set_collision(4, 20)


class Take(State):
    """Mantiene sujetado al enemigo"""
    
    def __init__(self, player, enemy, attack_counter=0):
        State.__init__(self, player)
        player.animation.set_state('take')
        player.update_animation()
        player.bandage.set_state('take')
        self.enemy = enemy
        self.enemy.y = player.y - 1
        self._change_enemy_position()
        self.enemy.change_state(Taked(self.enemy))
        self.attack_counter = attack_counter

    def update(self):
        c = self.player.control

        if c.attack:
            if c.left or c.right:
                self.player.flip = c.right
                self._change_enemy_position()
                self.player.change_state(Throw(self.player, c.left))
                self.enemy.flip = not c.left
                self.enemy.change_state(enemy_state.Throwed(self.enemy))
            else:
                self.attack_counter += 1

                if self.attack_counter > 3:
                    # supera la cantidad máxima de golpes locales.
                    self.enemy.change_state(enemy_state.HardHit(self.enemy))
                    self.player.change_state(AttackTakeAndJump(self.player, 
                        self.enemy, 0))
                else:
                    self.enemy.change_state(enemy_state.HitTaked(self.enemy, True))
                    self.player.change_state(AttackTake(self.player, self.enemy,
                        self.attack_counter))
        elif c.jump:
            self.enemy.change_state(enemy_state.Stand(self.enemy))
            self.player.change_state(JumpStand(self.player))
                    
    def _change_enemy_position(self):
        if self.player.flip:
            dx = 60
        else:
            dx = - 60
        
        self.enemy.x = self.player.x - dx
        self.enemy.flip = not self.player.flip
        self.player.update_animation()


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
        self.player.create_hit()
        self.continue_taked = continue_taked
        self.enemy_taked = enemy_taked
        self.attack_counter = attack_counter
        player.bandage.set_state('attacktake')
        

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
    "Arroja al enemigo previamente sujetado."
    
    def __init__(self, player, last_flip):
        State.__init__(self, player)
        self.player.animation.set_state('throw')
        self.step = 0
        self.last_flip = last_flip
        common.audio.play('throw')
        player.bandage.set_state('throw')

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
