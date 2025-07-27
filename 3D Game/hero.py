key_switch_camera = 'c'
key_switch_mode = 'z'

key_forward = 'w' #langkah maju
key_back = 's' #langkah mundur
key_left = 'a' #langkah ke kiri
key_right = 'd' #langkah ke kanan
key_up = 'e' #langkah ke atas
key_down = 'q' #langkah ke bawah

key_turn_left = 'n' #putar kamera ke kanan
key_turn_right = 'm' #putar kamera ke kiri

key_build = 'b'#bangun blok di depan anda
key_destroy = 'v'#hancurkan blok di depan anda

key_savemap ='k'
key_loadmap = 'l'

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True #melewati semua mode
        self.hero = loader.loadModel('smiley')
        self.hero.setColor (1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setH(180)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        #base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        self.hero.setH((self.hero.getH()+5)%360)

    def turn_right(self):
        self.hero.setH((self.hero.getH()-5)%360)

    def look_at(self, angle):

        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from
    
    def just_move (self, angle):
        #bergerak ke koordinat yang diinginkan dalam hal apa pun
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <=245:
            return (-1, 1)
        elif angle <= 290:
            return (-1,0)
        elif angle <= 335:
            return(-1, -1)
        else:
            return(0, -1)
        
    def forward(self):
        angle = (self.hero.getH())%360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH()+180)%360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH()+90)%360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH()+270)%360
        self.move_to(angle)

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def try_move(self, angle):
        #bergerak jka dia bisa
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            #ada area bebas di depan kita. mungkin anda perlu jatuh:
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            #didepan kita sedang sibuk.jika kita berhasil, mari kita panjat blok ini:
            pos = pos[0], pos[1], pos[2]+1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
                #kita tidak akan bisa mendaki-kita akan diam

    def up (self):
        if self.mode:
            self.hero.setZ(self.hero.getZ()+1)

    def down(self):
        if self.mode and self.hero.getZ()>1:
            self.hero.setZ(self.hero.getZ()-1)

    def build(self):
        angle = self.hero.getH()%360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle=self.hero.getH()%360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left+'-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right+'-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward+'-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back+'-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left+'-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right+'-repeat', self.right)
        
        base.accept(key_switch_camera, self.changeView)

        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_up, self.up)
        base.accept(key_up+'-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down+'-repeat', self.down)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

        base.accept(key_savemap, self.land.saveMap)
        base.accept(key_loadmap, self.land.loadMap)


