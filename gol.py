#!/usr/bin/env python3

import copy, time

class GOL:
    # Conway's Game of Life, featuring an infinite field (dynamic resizing) and
    # moderately efficient though with a simple implementation.
    # Stores only living cells (memory efficient) and only processes living
    # cells plus neighbors (CPU efficient).

    # Performance: 384ns per tick on a 90x51 field with a population of 16.

    # Operations read oldcells and set newcells. At the end of a tick,
    # changes are applied.

    # Possible performance improvement: queue operations instead of deep copying,
    # and perhaps garbage cleanup periodically instead of at every setCell.

    def __init__(self):
        self.oldcells = {}
        self.newcells = {}

    def get(self, x, y):
        if x not in self.oldcells:
            return 0
        if y not in self.oldcells[x]:
            return 0
        return self.oldcells[x][y]

    def birth(self, x, y):
        self._setCell(x, y, 1)

    def kill(self, x, y):
        self._setCell(x, y, 0)

    def _setCell(self, x, y, state):
        if state == 0:
            if x in self.newcells and y in self.newcells[x]:
                del self.newcells[x][y]
                if len(self.newcells[x].keys()) == 0:
                    del self.newcells[x]
            return

        if x not in self.newcells:
            self.newcells[x] = {}

        self.newcells[x][y] = state

    def _checkDeadNeighbors(self, x, y):
        for xx in (1, 0, -1):
            for yy in (1, 0, -1):
                if xx == 0 and yy == 0:
                    continue

                # Skip if alive
                if self.get(x + xx, y + yy) == 1:
                    continue

                # If it's dead, check whether it should live
                neighbors = self._neighbors(x + xx, y + yy)
                if neighbors == 3:
                    self.birth(x + xx, y + yy)

    def _neighbors(self, x, y):
        total = 0
        for xx in (1, 0, -1):
            for yy in (1, 0, -1):
                if xx == 0 and yy == 0:
                    continue

                total += self.get(x + xx, y + yy)
        return total

    def tick(self):
        for x in self.oldcells:
            for y in self.oldcells[x]:
                neighbors = self._neighbors(x, y)
                if neighbors < 2 or neighbors > 3:
                    self.kill(x, y)
                self._checkDeadNeighbors(x, y)
        self.applyChanges()

    def applyChanges(self):
        self.oldcells = copy.deepcopy(self.newcells)

    def getVisualGame(self, alive = 'X.', dead = '  '):
        lowestx = 0
        lowesty = 0
        highestx = 0
        highesty = 0
        for x in self.oldcells:
            if x > highestx:
                highestx = x
            if x < lowestx:
                lowestx = x
            lowesty = min([lowesty] + self.oldcells[x].keys())
            highesty = max([highesty] + self.oldcells[x].keys())

        visgame = ''
        for y in range(lowesty, highesty + 1):
            visgame += '|'
            for x in range(lowestx, highestx + 1):
                visgame += alive if self.get(x, y) else dead
            visgame += '|\n'
        return visgame

game = GOL()

def spawnGlider(game, x, y):
    game.birth(x + 1, y + 0)
    game.birth(x + 2, y + 1)
    game.birth(x + 0, y + 2)
    game.birth(x + 1, y + 2)
    game.birth(x + 2, y + 2)
    game.applyChanges()

def spawnLWSS(game, x, y):
    game.birth(x + 1, y + 0)
    game.birth(x + 2, y + 0)
    game.birth(x + 3, y + 0)
    game.birth(x + 4, y + 0)
    game.birth(x + 4, y + 1)
    game.birth(x + 4, y + 2)
    game.birth(x + 3, y + 3)
    game.birth(x + 0, y + 1)
    game.birth(x + 0, y + 3)

def spawnBlock(game, x, y):
    game.birth(x + 0, y + 0)
    game.birth(x + 0, y + 1)
    game.birth(x + 1, y + 0)
    game.birth(x + 1, y + 1)

spawnLWSS(game, 0, 10)
spawnGlider(game, 0, 0)
spawnBlock(game, 15, 15)
spawnBlock(game, 90, 20)

while True:
    print(game.getVisualGame())
    game.tick()
    time.sleep(0.1)

