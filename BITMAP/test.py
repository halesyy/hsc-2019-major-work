#// Author Jack Hales, 17-year-old Australian kas.nsw.edu.au Student
#// --
#// BitMap manipulation, BitMap refers to the process of creating a
#// black-background image that contains a prominent set of colours
#// that are significant in meaning.

#// Image.fromarray(numpyarray[.astype('uint8')], 'RGB')

import time, random
import numpy as np
from PIL import Image, ImageDraw

# Pathfinding!
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

BitMap = Image.open("alphabet-bitmap-ds/a.jpg")
PixelArr = np.array(BitMap)

xs = BitMap.size[0]
ys = BitMap.size[1]

#// Manual Colour-coding array
#// To be in JSON file one day

#// Requirement splitting for Vision rules
#// % value, 0.25 = 25% means splitting into 4 parts x 4 parts

by    = 8
split = 1 / by
squares  = int(1 / split)
squaresx = squares
totalSquares = int(squares*squares)
squarePixels = (xs*ys)/squares

xSplit = int((xs) / (1 / split))
ySplit = int((ys) / (1 / split))




class PixelArray(object):
    # - dynamically set variables
    # Squares
    # OGPixelArray is a numpy array

    def __init__(self, PA):
        self.OGPixelArray = PA
        self.BitMap = []
        self.Squares = []
        # - convert the "pixel array" location
        # into the square information and insert
        # seq
        self.PixelArrCache = np.zeros(shape=(squares*xSplit*xSplit+1, squares*ySplit*ySplit+1), dtype=list)

    # | Quick anti-alias removal, black & white ONLY,
    # | lesser is reduced to black, and higher is
    # | ceiling'd to white
    def AARemove(self):
        PixelArr = self.OGPixelArray
        for i in range(0, xs):
            for b in range(0, ys):
                if PixelArr[i, b][0] < 200:
                    PixelArr[i, b] = [0, 0, 0]
                else:
                    PixelArr[i, b] = [255, 255, 255]
        self.OGPixelArray = PixelArr

    def SortSquares(self):
        PixelArr = self.OGPixelArray
        Squares = [None for f in range(0, squares*squares)]
        startX, startY, iteration = 0, 0, 0
        for i in range(0, int(squares*squares)):
            # print(startX, startY)
            iteration += 1
            Squares[i] = self.SquareBundlerStartFrom(i, startX, startY)
            if iteration % int(xs/xSplit) == 0:
                startY = startY + ySplit
                startX = 0
            else:
                startX = startX + xSplit
        self.Squares = Squares

    def SquareBundlerStartFrom(self, squareNo, xStart, yStart):
        # Presetting the values for the bundled variables in a
        # 2D Numpy Array
        bundled = np.zeros(shape=(xSplit, ySplit), dtype=object)
        # Where we will start from for finding the X/Y values
        PixelArr = self.OGPixelArray
        storeX, storeY = xStart, yStart
        # For Inserting
        # print(squareNo)
        insertX, insertY, iteration = 0, 0, 0
        for i in range(0, (xSplit * ySplit)):
            iteration = i+1
            # - storing into the "bundled" array to return later
            # - storing in the bundle return [Y, X]
            bundled[insertY, insertX] = PixelArr[storeY, storeX]
            # - storing in the caches [Y, X]
            # if squareNo == 0: print("{0}: {1}, {2}".format(squareNo, storeX, storeY))
            self.PixelArrCache[storeY, storeX] = {"square": squareNo, "insertY": storeY, "insertX": storeX, "squareLocX": insertY, "squareLocY": insertX}
            if (iteration % int(xSplit) == 0):
                storeX = xStart
                storeY +=  1
                insertX = 0
                insertY += 1
            else:
                storeX += 1
                insertX += 1
        # bundled[0, 0] = [255, 255, 255]
        return bundled

    def SquareToPixelArr(self, SquareNo, Coords):
        # print(self.OGPixelArray)
        # - coords = [X, Y]
        for eachInfoBundle in self.PixelArrCache:
            for cacheInformation in eachInfoBundle:
                if (cacheInformation != 0) and (SquareNo == cacheInformation["square"]) and (Coords[0] == cacheInformation["squareLocX"]) and (Coords[1] == cacheInformation["squareLocY"]):
                    return cacheInformation

    def AllColourInSquare(self, squareNo, colour=[255, 255, 255]):
        # PixelArr = self.OGPixelArray
        area = []
        for eachInfoBundle in self.PixelArrCache:
            for cacheInformation in eachInfoBundle:
                if (cacheInformation != 0) and (squareNo == cacheInformation["square"]):
                    x, y = cacheInformation["insertX"], cacheInformation["insertY"]
                    # y, x
                    if str(self.OGPixelArray[y, x]) == str(colour).replace(',', ''):
                        area.append(cacheInformation)
        return area



    def Square2PAEditor(self, SquareNo, Coords):
        # print(SquareNo, Coords, "\n")
        CInformation = self.SquareToPixelArr(SquareNo, Coords)
        return [CInformation["insertY"], CInformation["insertX"]]

    # - editing functions

    def Change(self, src="PixelArr", xy=[], squareno=False, to=[]):
        # - src = PixelArr or Squares,
        # - Each edit has to edit the OGPixelArray
        x, y = xy[0], xy[1]
        # - Default format: [Y, X] when accessing
        if src == "Squares":
            SquareNo = squareno
            EditInfo = self.Square2PAEditor(SquareNo, [x, y])
            self.OGPixelArray[EditInfo[1], EditInfo[0]] = to

    def SQCHange(self, s=0, x=0, y=0, to=[255, 255, 255]):
        self.Change(src="Squares", xy=[x, y], squareno=s, to=to)


    def Start_RandomLineBetweenFilledSquares(self, first, second):
        AllSqrs1 = self.AllColourInSquare(first)
        AllSqrs2 = self.AllColourInSquare(second)
        ASC1 = random.choice(AllSqrs1)
        ASC2 = random.choice(AllSqrs2)
        # draw time
        Draw = self.Open()
        colour, width = "#c21f1f", 1
        Draw.line([ASC1["insertX"], ASC1["insertY"], ASC2["insertX"], ASC2["insertY"]], fill=colour, width=width)
        self.Close()
        # saving data
        self.lastFinishingPoint = [ASC2["insertX"], ASC2["insertY"]]

    def Next_RandomLineFromLastInFilledSquares(self, nextSquare):
        lastFinishingPoint = self.lastFinishingPoint
        Next = self.AllColourInSquare(nextSquare)
        ASC1 = random.choice(Next)
        # draw time
        Draw = self.Open()
        colour, width = "#c21f1f", 1
        Draw.line([lastFinishingPoint[0], lastFinishingPoint[1], ASC1["insertX"], ASC1["insertY"]], fill=colour, width=width)
        self.Close()
        # saving data
        self.lastFinishingPoint = [ASC1["insertX"], ASC1["insertY"]]


















    # - all displaying and saving functions

    def ShowOG(self):
        OGPA = self.OGPixelArray
        im = Image.fromarray(OGPA)
        im.show()
        return self

    def SaveOG(self):
        OGPA = self.OGPixelArray
        im = Image.fromarray(OGPA)
        im.save("og.png")
        return self

    # - takes a square, and creates a new image and fills it
    # - with the area data provided by the following functions.

    def ShowSquareAlone(self, squareNo):
        fa = Image.new(mode="RGB", size=[16, 16])
        faa = np.array(fa)
        for pixelParcel in self.AllColourInSquare(squareNo, [255, 255, 255]):
            for x, y in self.Unpack(pixelParcel, "squareLoc"):
                faa[x, y] = [255, 255, 255]
                # print(x, y)
        faai = Image.fromarray(faa)
        faai.show()

    def Empty(self, squareNo):
        isEmpty = 1
        square = self.Squares[squareNo]
        for a in range(len(square)):
            for b in range(len(square[a])):
                if square[a][b][0] == 255:
                    isEmpty = 0
        return bool(isEmpty)

    def Contains(self, squareNo):
        return not self.Empty(squareNo)

    def ContainsArray(self, cast=bool):
        access = 0
        mapArray = [[]]
        for i in range(len(self.Squares)):
            ic = i + 1
            if access > (len(mapArray)-1): mapArray.append([])
            mapArray[access].append(cast(self.Contains(i)))
            if ic % squares == 0: access += 1
        # print("finished at {0}".format(i))
        return mapArray

    def ContainsArrayPoints(self):
        access = 0
        mapArray = [[]]
        for i in range(len(self.Squares)):
            ic = i + 1
            if access > (len(mapArray)-1): mapArray.append([])
            if self.Contains(i): mapArray[access].append(i)
            if ic % squares == 0: access += 1
        return mapArray

    def PrintSquareMap(self):
        for i in range(len(self.Squares)):
            ic = i + 1
            print(int(self.Contains(i)), end="  ")
            if ic % squares == 0: print("\n")










    # - | finding the "best path" to
    # - | to follow in the writing algorithm,
    # - | writes all the path code and
    # - | does all the handling for passing
    # - | into the further creation realm
    def Path(self):
        Brute = 100 # length of tries in the actual pathfinding
        OverallBrute = 1 # times to try to getting the path
        ConsiderableSquares = self.ContainsArrayPoints()
        ConsiderableSquares1d = [] # - a flat array
        for cs in ConsiderableSquares:
            for each in cs:
                ConsiderableSquares1d.append(each)

        # | - the parent, starting on a random
        # | - line then sub-bruting till it
        # | - finds a dead end and goes till
        # | it covers every square and resolves
        # | the path

        CoveredSquares = []

        # | We're done WHEN: all CoveredSquares are in ConsiderableSquares

        for i in range(OverallBrute):

            # - random line to start on
            LineNo = random.randint(0, len(ConsiderableSquares)-1)
            Line = ConsiderableSquares[LineNo]

            CoveredSquares = []
            Choice = random.choice(Line)
            CoveredSquares.append(Choice)

            for b in range(Brute):
                Movements = {
                    "U": Choice+xSplit,
                    "R": Choice+1,
                    "UR": Choice+xSplit+1,
                    "UL": Choice+xSplit-1,
                    "BL": Choice-xSplit-1,
                    "BR": Choice-xSplit+1,
                    "L": Choice-1,
                    "D": Choice+xSplit
                }
            print(Movements)

        self.PrintSquareMap()
        print(ConsiderableSquares) # - all squares

        # G = Grid(matrix=Considerable)
        # Start, End = G.node(7, 1), G.node(8, 8)
        # finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        # path, runs = finder.find_path(Start, End, G)
        # print('operations:', runs, 'path length:', len(path))
        # print(G.grid_str(path=path, start=Start, end=End))
        # print(Considerable)
        # for i in range(OverallBrute):
        #     square = 0
            # - iterating by ylen of the Contains array,
            # - then the individual lines
            # randomLine = random.choice(Considerable)

            # for line in Considerable: # y-roaming line
            #     for contains in line: # indiv x-roaming line


                    # square += 1

        # else:
        #     pass
            # print("IT DIDNT FUCKING WORK", end="")

    # - iter functions to make it easier to iterate
    # | - pixelParcel (parcel) is a pack provided by the cache
    # | - information series.

    def Unpack(self, parcel, pref="insert"):
        return zip([parcel["{0}X".format(pref)]], [parcel["{0}Y".format(pref)]])

    # - bitmap opening functions, to convert the array into an
    # - original piece

    def Open(self):
        PixelArr = self.OGPixelArray
        self.BitMap = Image.fromarray(PixelArr)
        # self.BitMapDraw = ImageDraw.Draw(self.BitMap)
        return ImageDraw.Draw(self.BitMap)

    def Draw(self):
        return ImageDraw.Draw(self.BitMap)

    def Close(self, removeAA=False):
        BitMap = self.BitMap
        self.OGPixelArray = np.array(BitMap)
        if removeAA: self.AARemove()




PA=PixelArray(PixelArr)
PA.AARemove()
PA.SortSquares()

PA.Path()

PA.SaveOG()






# | Quick square is-empty clause, checking
# | if data in the square is totally black,
# | if so, return 1, else return 0.








def gradient_check(xy1, xy2):
    # getting the slope from xy1 to xy2, essentially to get the positioning
    # and get a valuemeter for it
    # if xy2 is to the LEFT of  xy1, then they are going left
    # if xy2 is to the UNDER of xy1, then they are going down
    # see the pattern? xy1 is the initial, and xy2 helps give
    # reference.
    pass
