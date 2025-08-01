# write the code for creating and managing the map here
import pickle

class Mapmanager():
    """Map magement"""
    def __init__(self):
        self.model = 'block'#the cube model is in the block.egg file
        # # the following textures are used:
        self.texture ='block.png'
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ]#rgba
        #create the main map node:
        self.startNew()
        # self.addblock((0,10,0))

    def startNew(self):
        """creates the basis for the new map"""
        self.land = render.attachNewNode('Land')#the node which all the map blocks are attached to

    def getColor(self, z):
        if z<len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors)-1]
        
    def addBlock(self, position):
        #create building blocks
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.setTag("at", str(position))
        self.block.reparentTo(self.land)

    def clear (self):
        """resets the map"""
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        """creates a land map from a text file, returns its dimensions"""
        self.clear()
        with open(filename) as file:
            y=0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y
    
    def findBlocks(self, pos):
        return self.land.findAllMatches('=at='+str(pos))
    
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
        
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return(x,y,z)
    
    def buildBlock(self, pos):
        """"kita menempatkan balok dengan mempertimbangkan gravitasi:"""
        x, y, z = pos
        new=self.findHighestEmpty(pos)
        if new[2]<= z+1:
            self.addBlock(new)

    def delBlock(self, position):
        """"menghapus blok pada posisi yang ditentukan"""
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z -1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        """"menyimpan semua blok, termasuk bangunan, ke file biner"""
        """"mengembalikan koleksi NodePath untuk semua blok yang ada"""
        blocks = self.land.getChildren()
        #buka file biner untuk menulis
        with open('my_map.dat','wb') as fout:
            #simpan jumlah blok di awal file
            pickle.dump(len(blocks), fout)
            #melintasi semua blok
            for block in blocks:
                #simpan posisi
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)
    
    def loadMap(self):
        #hapus semua blok
        self.clear()
        #buka file biner untuk dibaca
        with open('my_map.dat','rb') as fin:
            #membaca jumlah blok
            length = pickle.load(fin)
            for i in range(length):
                #baca posisinya
                pos = pickle.load(fin)
                #buat blok baru
                self.addBlock(pos)