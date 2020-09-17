# In this project, I think of the options of what you can do in the game in function of what buttons I press and what menu I'm in
# Various actions have a set o button pressing and logic to it, so I code functions that translate the actions I want to do into the 
# sequence of buttons to press and how much to wait depending on what I do

class game_navigation(object):
    
    def __init__ (self,up,down,left,right,enter,press_sleep,comm_sleep):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.enter = enter
        self.press_sleep = press_sleep
        self.comm_sleep = comm_sleep
        self.pos = [0,0]
        self.last_action_pos = [0,0]
        self.skill_uses = 0
        self.atk_uses = 0
        
        self.enter_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format(self.enter, self.press_sleep, self.comm_sleep)
        
        self.down_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format(self.down, self.press_sleep, self.comm_sleep)
        
        self.up_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format(self.up, self.press_sleep, self.comm_sleep)
        
        self.rotate_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format("j", self.press_sleep, self.comm_sleep)
        
    def cursor_move(self,destiny,action=0):
        
        orig = self.pos # it keeps track of where you are
        dest = destiny # it needs to be relative to the orig unless asked to go to the origin ([0,0])
        
        if dest == [0,0]:
            dest[0] = -self.pos[0]
            dest[1] = -self.pos[1]

        x_range = dest[0]
        y_range = dest[1]

        x_dir = 0 
        y_dir = 0

        if x_range == 0:
            pass
        elif abs(x_range)/x_range == 1:
            x_dir = 1
        else:
            x_dir = -1

        if y_range == 0:
            pass
        elif abs(y_range)/y_range == 1:
            y_dir = 1 
        else:
            y_dir = -1

        if x_dir != 0:    
            if x_dir == 1:
                x_key = self.down
            else:
                x_key = self.up

            x_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format(x_key, self.press_sleep, self.comm_sleep)

            x_loops = abs(x_range)
            if x_loops>1:
                print('''loop, {0}
{{'''.format(x_loops))
                print(x_comm)
                print("}")
            else:
                print(x_comm)


        if y_dir != 0:    
            if y_dir == 1:
                y_key = self.right
            else:
                y_key = self.left

            y_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format(y_key, self.press_sleep, self.comm_sleep)

            y_loops = abs(y_range)
            if y_loops>1:
                print('''loop, {0}
{{'''.format(y_loops))
                print(y_comm)
                print("}")
            else:
                print(y_comm)
                
        if action == 1:
            print(self.enter_comm)

        self.pos[0] += destiny[0]
        self.pos[1] += destiny[1]
        
    def get_char_out(self,char_place):
        
        print(self.enter_comm)
        
        if char_place == 0:
            pass
        
        else:
        
            if abs(char_place)/char_place == 1:
                nav_comm = self.down_comm

            else:
                nav_comm = self.up_comm

            if abs(char_place) == 1:
                print(self.down_comm)
            else:
                print('''loop, {0}
{{'''.format(abs(char_place)))
                print(nav_comm)
                print("}")
                
    def char_move(self,destiny):
        
        time_wait = (abs(destiny[0]) + abs(destiny[1]))*110
        
        print('''loop, 2
{''')
        print(self.enter_comm)
        print("}")
        self.cursor_move(destiny,1)
        print("Sleep, {0}".format(time_wait))
        
    def char_return(self):
        
        time_wait = (abs(self.pos[0]) + abs(self.pos[1]))*110
        
        print('''loop, 2
{''')
        print(self.enter_comm)
        print("}")
        self.cursor_move([0,0],1)
        print("Sleep, {0}".format(time_wait))
        
    def skill_use(self, skill_place, destiny=None, direction = None, rotation = None, self_use = 0):
    
        self.last_action_pos = self.pos.copy() 
        
        print(self.enter_comm)
        print('''loop, 2
{''')
        print(self.down_comm)
        print("}")
        print(self.enter_comm)
        for positioning in skill_place:
            if positioning == 0:
                pass
            elif positioning == 1:
                print(self.down_comm)
            elif positioning == -1:
                print(self.up_comm)
            elif positioning>1:
                print('''loop, {0}
{{'''.format(abs(positioning)))
                print(self.down_comm)
                print("}")
            elif positioning<-1:
                print('''loop, {0}
{{'''.format(abs(positioning)))
                print(self.up_comm)
                print("}")
            print(self.enter_comm)
            
        if rotation != None and rotation>=1:
            if rotation == 1:
                print(self.rotate_comm)
            else:
                print('''loop, {0}
{{'''.format(abs(rotation)))
                print(self.rotate_comm)
                print("}")
        
        if self_use == 0 and destiny!=None and direction==None:
            self.cursor_move(destiny,1)
            
        elif self_use == 0 and destiny==None and direction!=None:
            
            directions = [["up","d"], ["down","a"], ["left","w"], ["right","s"]]
        
            for i in directions:
                if i[0] == direction:
                    s_key = i[1]
                    break
                    
            s_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format(s_key, self.press_sleep, self.comm_sleep)
            
            print(s_comm)
            print(self.enter_comm)
                    
                
        else:
            print(self.enter_comm)
        
        self.skill_uses += 1
        
    def lift(self, lift_place):
        print(self.enter_comm)
        print('''loop, 4
{''')
        print(self.down_comm)
        print("}")
        print(self.enter_comm)
        if lift_place == 0:
            pass
        elif lift_place == 1:
            print(self.down_comm)
        elif lift_place>1:
            print('''loop, {0}
{{'''.format(abs(lift_place)))
            print(self.down_comm)
            print("}")
        print(self.enter_comm)
        
    def throw(self, direction, spaces, correct_positioning = 0):
        
        directions = [["up","d",[0,1]], ["down","a",[0,-1]], ["left","w",[-1,0]], ["right","s",[1,0]]]
        
        for i in directions:
            if i[0] == direction:
                t_key = i[1]
                throw_mult = i[2]
                break
            
        t_comm = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format(t_key, self.press_sleep, self.comm_sleep)
        
        print(self.enter_comm)
        print('''loop, 4
{''')
        print(self.down_comm)
        print("}")
        print(self.enter_comm)
        
        if correct_positioning == 0:
        
            if spaces==1:
                print(t_comm)

            else:
                print('''loop, {0}
    {{'''.format(spaces))
                print(t_comm)
                print("}")
            
        else:
            
            fake_spaces = spaces - 1
            
            if fake_spaces==1:
                print(t_comm)

            else:
                print('''loop, {0}
    {{'''.format(fake_spaces))
                print(t_comm)
                print("}")
                
        print(self.enter_comm)
        
        throw_loc = [i * spaces for i in throw_mult]
        
        self.pos[0] += throw_loc[0]
        self.pos[1] += throw_loc[1]
        
        space_time = spaces*110+300
        
        print("Sleep, {0}".format(space_time))
        
    def atk(self,enemy_place):
        
        self.last_action_pos = self.pos.copy()
        
        print(self.enter_comm)
        print(self.down_comm)
        print(self.enter_comm)
        if enemy_place == 0:
            pass
        elif enemy_place == 1:
            print(self.down_comm)
        elif enemy_place == -1:
            print(self.up_comm)
        elif enemy_place>1:
            print('''loop, {0}
{{'''.format(abs(enemy_place)))
            print(self.down_comm)
            print("}")
        elif enemy_place<-1:
            print('''loop, {0}
{{'''.format(abs(enemy_place)))
            print(self.up_comm)
            print("}")
        print(self.enter_comm)
        
        self.atk_uses += 1
        
    def end_turn(self):
        long_wait = self.skill_uses*1800+self.atk_uses*2200+6000
        end_turn_action = '''Send, {{{0} down}}
Sleep {1}
Send, {{{0} up}}
Sleep, {2}'''.format("2", self.press_sleep, long_wait)
        print(end_turn_action)
        
        if self.skill_uses>0 or self.atk_uses>0:
            self.pos = self.last_action_pos
            self.skill_uses = 0
            self.atk_uses = 0
            
            
