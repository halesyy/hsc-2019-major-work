#// Author Jack Hales, 17-year-old Australian kas.nsw.edu.au Student
#// --
#// BitMap manipulation, BitMap refers to the process of creating a
#// black-background image that contains a prominent set of colours
#// that are significant in meaning.

import time, random, math
import numpy as np
from PIL import Image, ImageDraw
import pprint as pprint
import os, sys

pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint
os.system("clear")

# Pathfinding!
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#// Manual Colour-coding array
#// To be in JSON file one day

#// Requirement splitting for Vision rules
#// % value, 0.25 = 25% means splitting into 4 parts x 4 parts

# Meta retention-data,
# not defined by the type of image,
# but the self-manipulation.
Complexity, by = 1, 32
split = 1 / by
squares  = int(1 / split)
squaresx = squares
totalSquares = int(squares*squares)
xs, ys = 0, 0

class PixelArray(object):
    # - dynamically set variables
    # Squares
    # OGPixelArray is a numpy array

    def __init__(self, PA):
        # cp-string for data collection and retention
        global xs, ys, xSplit, ySplit, squarePixels, totalSquares, squaresx, squares, split, by

        self.OGPixelArray = PA
        self.BitMap = Image.fromarray(PA)
        xs, ys = self.BitMap.size[0], self.BitMap.size[1]

        squarePixels = (xs*ys)/squares
        xSplit = int((xs) / (1 / split))
        ySplit = int((ys) / (1 / split))

        self.Squares = []
        # - convert the "pixel array" location
        #   into the square information and insert
        #   seq
        self.PixelArrCache = np.zeros(shape=(squares*xSplit*xSplit+1, squares*ySplit*ySplit+1), dtype=list)

    # | Quick anti-alias removal, black & white ONLY,
    # | lesser is reduced to black, and higher is
    # | ceiling'd to white
    def AARemove(self):
        global xs, ys, xSplit, ySplit, squarePixels, totalSquares, squaresx, squares, split, by
        PixelArr = self.OGPixelArray
        for i in range(0, xs):
            for b in range(0, ys):
                if PixelArr[i, b][0] < 120: PixelArr[i, b] = [0, 0, 0]
                else: PixelArr[i, b] = [255, 255, 255]
        self.OGPixelArray = PixelArr

    def SortSquares(self):
        PixelArr = self.OGPixelArray
        print("from ss: ", str(squares), )
        Squares = [None for f in range(0, squares*squares)]
        startX, startY, iteration = 0, 0, 0
        # squares are stored from 0 -> squares*squares
        for i in range(int(squares*squares)):
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

    # | Return the colours in the square number
    def AllColourInSquare(self, squareNo, colour=[255, 255, 255]):
        # print(squareNo)
        area = []
        for eachInfoBundle in self.PixelArrCache:
            for cacheInformation in eachInfoBundle:
                if (cacheInformation != 0) and (squareNo == cacheInformation["square"]):
                    x, y = cacheInformation["insertX"], cacheInformation["insertY"]
                    # y, x
                    # print(self.OGPixelArray[y, x], colour)
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
            self.OGPixelArray[EditInfo[0], EditInfo[1]] = to

    def SQCHange(self, s=0, x=0, y=0, to=[255, 255, 255]):
        self.Change(src="Squares", xy=[x, y], squareno=s, to=to)







    def Trim(self, NewBy, to=[0, 0, 0]):
        global by, split, squares, totalSquares, xs, ys, xSplit, ySplit
        OldSquares, OldBy = self.Squares, by

        # NEW, FOR SPLIT TRIMMING
        by = NewBy
        split = 1 / by
        squares, squaresx = int(1 / split), int(1 / split)
        totalSquares = int(squares*squares)
        xSplit = int((xs) / (1 / split))
        ySplit = int((ys) / (1 / split))
        self.SortSquares()

        for k, sqr in enumerate(self.Squares):
            #SQCHange(self, s=0, x=0, y=0, to=[255, 255, 255]):
            # print(k, " empty check in trim: ", self.Empty(k))
            if not self.Empty(k):
                self.SQCHange(s=k, x=0, y=0, to=to)

        # OLD, GOING BACK TO OLD DATA
        by = OldBy
        split = 1 / by
        squares, squaresx = int(1 / split), int(1 / split)
        totalSquares = int(squares*squares)
        xSplit = int((xs) / (1 / split))
        ySplit = int((ys) / (1 / split))
        self.Squares = OldSquares
        self.SortSquares()






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

    def PathVisualize(self):
        i = 0
        for DirectionSpace in self.DirectionSequence:
            Direction, SquareNo = DirectionSpace[0], DirectionSpace[1]
            if i == 0:
                First = SquareNo
            elif i == 1:
                self.Start_RandomLineBetweenFilledSquares(first=First, second=SquareNo)
            # elif i > 1:
            #     self.Next_RandomLineFromLastInFilledSquares(SquareNo)
            i += 1
















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

    def Contains(self, squareNo, highlight="no"):
        if squareNo == highlight: return 2
        return not self.Empty(squareNo)

    # - inserting all the "contains" info into an array that can be edited
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

    # - inserting all the "contains" info into an array that can be edited
    def ContainsArrayPoints(self):
        access = 0
        mapArray = [[]]
        for i in range(len(self.Squares)):
            ic = i + 1
            if access > (len(mapArray)-1): mapArray.append([])
            if self.Contains(i): mapArray[access].append(i)
            if ic % squares == 0: access += 1
        return mapArray

    def PrintSquareMap(self, highlight="no"):
        print("HIGHLIGHTING: {0}".format(highlight))
        for i in range(len(self.Squares)):
            ic = i + 1
            print(int(self.Contains(i, highlight=highlight)), end=" ")
            if ic % squares == 0: print("")


    def SquareXYCache(self):
        xtemp = 0
        ytemp = 0
        squarescache = [i for i in range(squaresx*squaresx)]

        for i in range(squaresx*squaresx): # 0 -> 63
            # want to increate X each run
            # when going Y up, X = 0, Y += 1
            squarescache[i] = [xtemp, ytemp]
            #             |
            #             |
            # x = ->, y = v

            if (xtemp+1) % squaresx == 0:
                xtemp =  0
                ytemp += 1
            else:
                xtemp += 1
        # pp(squarescache)
        return squarescache


    # - taking the square, and applying the direction sequence
    # - to where to apply each period
    def SquareBounds(self, squareNo, direction):

        # Creating an array converter, since
        # the dest-mathematical generality is just
        # too simple for the creation.
        SCHE = self.SquareXYCache()

        # print(str(squareNo) + " stopped by " + str(direction), end=" ")
        # X = math.ceil((squareNo+1)/squaresx)
        # Y = math.ceil((squareNo)%squaresx)+1
        # X = math.floor((squareNo)/squaresx)
        # Y = math.floor((squareNo)%squaresx)
        X, Y = SCHE[squareNo]
        X += 1
        Y += 1

        # right = the square's right-side
        # Right =
        # print(xSplit, ySplit)
        TrueRight = xs - ((xSplit-1) * X)
        TrueDown = ys - ((ySplit-1) * Y)
        Right = xSplit * X
        Down = ySplit * Y
        # Right = xSplit * Y
        # Down = ySplit * X
        Left = Right - xSplit
        Up = Down - ySplit

        print("bounds for {0}, X,Y={1},{2} - ".format(squareNo, X, Y), Up, TrueDown, Left, TrueRight)
        if Left < 0: Left = 0
        if Up < 0: Up = 0

        DirectionConvert = {
            "O":   [0, 0, 0, 0],
            "L":   [0, 0, Left, 0],
            "D":   [0, Down, 0, 0],
            "UR":  [Up, 0, 0, Right],
            "UL":  [Up, 0, Left, 0],
            "BL":  [0, Down, Left, 0],
            "BR":  [0, Down, 0, Right],
            "R":   [0, 0, 0, Right],
            "U":   [Up, 0, 0, 0]}

        # print(" - " + str(DirectionConvert[direction]))
        return DirectionConvert[direction]

    def TestBounds(self):
        for i in range(squaresx*squaresx):
            self.SquareBounds(i, "U")
            if i%squaresx == 0: print()


    # - taking the square, and applying the direction sequence
    # - to where to apply each period
    def SquareCentre(self, squareNo):

        # X = math.ceil((squareNo+1)/squaresx)
        # Y = math.ceil((squareNo)%squaresx)+1
        SCHE = self.SquareXYCache()
        X, Y = SCHE[squareNo]
        X += 1
        Y += 1 # higher-ref, since it index starts at 0

        Right = xSplit * X
        Down = ySplit * Y
        Left = Right - xSplit
        Up = Down - ySplit
        if Left < 0: Left = 0
        if Up < 0: Up = 0

        Right -= round(xSplit/2)
        Down  -= round(ySplit/2)
        print("centre position for {0}:".format(squareNo), Right, Down)
        print()
        return [Right, Down]







    # - | finding the "best path" to
    # - | to follow in the writing algorithm,
    # - | writes all the path code and
    # - | does all the handling for passing
    # - | into the further creation realm
    def Path(self):
        # 16 -> 3
        # 08 -> 1.2
        #

        Compression = 5 # overall tests, for the "sloppiness"
        Leveler     = 3 # the expected overhead of moves required
                        # to finally get to the ending area of
                        # total control.
        Leveler     = (by/8)*(1.8+Complexity) if by >= 8 else 3
        # leveler-specific itemic values
        # if by == 8: Leveler = 1.5

        ConsiderableSquares = self.ContainsArrayPoints()
        ConsiderableSquares1d = [] # - a flat array
        for cs in ConsiderableSquares:
            for each in cs:
                ConsiderableSquares1d.append(each)

        # | - the parent, starting on a random
        # | - line then sub-bruting till it
        # | - finds a dead end and goes till
        # | - it covers every square and resolves
        # | - the path
        Brute, OverallBrute = round(len(ConsiderableSquares1d)*Leveler), 10000*Compression # Brute=overall attempts, Overall=individual attempts at pathfinding
        # Brute, OverallBrute = 2, 1
        CoveredSquares = []
        AllCovered = False


        for i in range(OverallBrute):

            Movement, CurrentPlace = "O", random.choice(ConsiderableSquares1d)
            DirectionSequence = [["O", CurrentPlace]] # the operations of movement dir's
            CoveredArea = [CurrentPlace] # the covered area through pathfinding
            # recording the direction and meta info
            StepInformation, Original, LinearDirections = [], CurrentPlace, [CurrentPlace]
            if AllCovered: break

            for i in range(Brute):
                # checking if all CoveredArea numbers makeup the entire length
                AllCovered = True
                for ConsLoc in ConsiderableSquares1d:
                    if ConsLoc not in CoveredArea:
                        AllCovered = False

                if AllCovered == True:
                    self.DirectionSequenceDone = True
                    self.DirectionSequence = DirectionSequence
                    # print("finished in {0}".format(i))
                    self.PrintSquareMap(highlight=Original)
                    print(self.DirectionSequence)
                    # print("\n\n")
                    # pp(LinearDirections)
                    # pp(StepInformation)
                    return DirectionSequence
                else: self.DirectionSequenceDone = False

                Movements = {
                    "U":   CurrentPlace-squaresx,
                    "R":   (CurrentPlace+1)           if ((CurrentPlace+1)%squaresx!=0) else -1, #rc
                    "UR":  CurrentPlace-squaresx+1    if ((CurrentPlace+1)%squaresx!=0) else -1, #rc
                    "UL":  CurrentPlace-squaresx-1    if ((CurrentPlace)%squaresx!=0) else -1, #lc
                    "BL":  CurrentPlace+squaresx-1    if ((CurrentPlace)%squaresx!=0) else -1, #lc
                    "BR":  CurrentPlace+squaresx+1    if ((CurrentPlace+1)%squaresx!=0) else -1, #rc
                    "L":   CurrentPlace-1             if ((CurrentPlace)%squaresx!=0) else -1, #lc
                    "D":   CurrentPlace+squaresx}

                for Movement, Place in sorted(Movements.items(), key=lambda x: random.random()):
                    if Place in ConsiderableSquares1d:
                        DirectionSequence.append([Movement, Place])
                        CoveredArea.append(Place)

                        # print(Movement, Place)

                        StepInformation.append({
                            "before": CurrentPlace,
                            "after": Place,
                            "movements": Movements,
                            "newPlace": Place,
                            "beforePlace": CurrentPlace,
                            "direction": Movement
                        })

                        CurrentPlace = Place

                        # placing into direction
                        LinearDirections.append("{0}:{1}".format(Movement, Place))
                        break


                else: print("n")




    # - takes squareNo and applies where it will be after
    # - direction is applied
    def DirectionApplySquareNo(self, SquareNo, Direction):
        CurrentPlace = SquareNo
        Movements = {
            "O":   CurrentPlace,
            "U":   CurrentPlace-squaresx,
            "R":   (CurrentPlace+1)           if ((CurrentPlace+1)%squaresx!=0) else -1, #rc
            "UR":  CurrentPlace-squaresx+1    if ((CurrentPlace+1)%squaresx!=0) else -1, #rc
            "UL":  CurrentPlace-squaresx-1    if ((CurrentPlace)%squaresx!=0) else -1, #lc
            "BL":  CurrentPlace+squaresx-1    if ((CurrentPlace)%squaresx!=0) else -1, #lc
            "BR":  CurrentPlace+squaresx+1    if ((CurrentPlace+1)%squaresx!=0) else -1, #rc
            "L":   CurrentPlace-1             if ((CurrentPlace)%squaresx!=0) else -1, #lc
            "D":   CurrentPlace+squaresx
        }
        # print("from {0} in dir {1} makes {2}".format(SquareNo, Direction, Movements[Direction]))
        return Movements[Direction]






    # - | formating the self.DirectionSequence into
    # - | a fair format.
    def PathFormat(self):
        if self.DirectionSequenceDone == False:
            print("Path has not been established...")
            return False

        AngleConvert = {
            "O": 0,
            "U": 0,
            "D": 180,
            "L": 270,
            "R": 90,
            "UR": 45,
            "UL": 315,
            "BL": 225,
            "BR": 135}
        i, Series = 0, []

        for DirectionSpace in self.DirectionSequence:
            if i >= 1:
                Direction, SquareNo, PastDirection = DirectionSpace[0], DirectionSpace[1], self.DirectionSequence[i-1]
                # THIS IS THE MOST IMPORTANT KEYWORD THAT IS IN THIS ENTIRE CODEBASE VVV
                # we're going from PastDirection, to the SquareNo in Direction
                OldSquareNo = PastDirection[1]
                # OldSquareNo -> SquareNo, by Direction
                # print(OldSquareNo, '->', SquareNo, 'by', Direction)


                Angle = AngleConvert[Direction]
                # Bounds = self.SquareBounds(self.DirectionApplySquareNo(SquareNo, Direction), Direction)
                Bounds = self.SquareBounds(SquareNo, Direction)
                X, Y   = self.SquareCentre(OldSquareNo)

                PackedFormatOBJ = {
                    "oldSquareX": X,
                    "oldSquareY": Y,
                    "stoppingBounds": Bounds,
                    "newSquareNo": SquareNo,
                    "oldSquareNo": OldSquareNo,
                    "direction": Direction,
                    "pastDirection": PastDirection,
                    "angle": Angle,
                }
                # pp(PackedFormatOBJ)

                # print('[', X, ',', Y, ',', Angle, ",", Bounds, ',', OldSquareNo, ',\'', Direction, '\'',  ']', end=", ")
                Series.append([X, Y, Angle, Bounds, OldSquareNo, Direction])
            i += 1
        # else:
        #     print("b4 else")
        #     a = self.SquareBounds(DirectionSpace[1], DirectionSpace[0])

        return Series






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
