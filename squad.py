import cybw
from cybw import Position

# squad class
class Squad:
    def __init__(self,squad_num):
        self.units = []
        self.center = Position(0,0)
        self.Max_units=4
        self.current_units=0
        self.old_current_units=0
        self.squad_leader=0
        self.squad_number=squad_num
        self.reward=0.01
        self.killCounts=[]
        self.status=[]

    def add(self, unit):
        if self.current_units<self.Max_units:
            self.units.append(unit)
            self.killCounts.append(0)
            self.status.append(1)
            self.updateCenter()
            self.current_units+=1
            self.old_current_units+=1
            print(self.units)
        else:
            print("To many units in squad %d"%self.squad_number)

    def getNearbyEnemies(self):
        enemies = []
        nearby = self.units[self.squad_leader].getUnitsInRadius(self.units[self.squad_leader].getType().sightRange())
        for e in nearby:
            if e.getPlayer().getID() != self.units[self.squad_leader].getPlayer().getID():
                enemies.append(e)
        return enemies

    def getEnemyPosition(self, enemies):
        enemyPos = self.center
        if len(enemies) > 0:
            for e in enemies:
                enemyPos += e.getPosition()
            enemyPos /= len(enemies)
        return enemyPos

    def retreatFromPosition(self, position):
        sight = self.units[self.squad_leader].getType().sightRange()
        retreatVector = position - self.center
        retreatVector = Position(2*retreatVector.getX(), 2*retreatVector.getY())
        retreatPos = self.center - retreatVector
        self.move(retreatPos)

    def retreat(self, enemies):
        enemyPos = self.getEnemyPosition(enemies)
        self.retreatFromPosition(enemyPos)

    def getPosShift(self, position):
        xshift = self.center.getX() - position.getX()
        yshift = self.center.getY() - position.getY()
        return (xshift, yshift)

    def move(self, position):
        for unit in self.units:
            unit.move(position)

    def attackMove(self, position):
        #print(position)
        for unit in  self.units:
            unit.attack(position)

    def attackShift(self, shift):
        for unit in  self.units:
            unit.attack(Position(shift[0] + unit.getPosition().getX(), shift[1] + unit.getPosition().getY()))

    def updateCenter(self):
        self.center = Position(0,0)
        for unit in self.units:
            self.center += unit.getPosition()
        if self.current_units>0:
            self.center /= len(self.units)
            
    def update(self, events):
        
        self.reward=0.01
        iterator=0
        for unit in self.units:
            #print(iterator)
            if not unit.exists() and self.status[iterator]==1:
                self.status[iterator]=0
                #if squad leader died change sqaud leader
                if unit== self.units[self.squad_leader]:
                    print(self.units[self.squad_leader])
                    iters=0
                    for s in self.units:
                        #print(s)
                        if s.exists():
                            #print(iters)
                            #print(self.squad_leader)
                            self.squad_leader=iters
                            #print(self.squad_leader)
                            break
                        iters+=1
                    print(self.units[self.squad_leader])     
                self.current_units-=1
                self.reward=-1
            elif unit.getKillCount()>self.killCounts[iterator]:
                self.killCounts[iterator]= unit.getKillCount()
                self.reward=1
                print("Unit %d got a kill"%iterator)
            
            iterator+=1
        self.updateCenter()
   
