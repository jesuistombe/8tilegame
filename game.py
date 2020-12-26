# import the pygame module, so you can use it
import pygame
from random import shuffle

BORDERCOLOR = (255, 0, 0)
BACKGROUNDCOLOR = (0, 0, 0)
EMPTYIMAGETILE = 0 # which tile of the original image should be empty/dark
BORDERWIDTH = 5

def drawBorderAroundTile(screen, tile, remove=False):
    if remove:
        pygame.draw.rect(screen, BACKGROUNDCOLOR, tile, BORDERWIDTH)
    else:
        pygame.draw.rect(screen, BORDERCOLOR, tile, BORDERWIDTH)

# the only tiles that have no right neighbor are 2,5 and 9. Otherwise just add 1
# the same logic applies to the other directions
def getRightNeighborTile(currentSelectedTile):
    if currentSelectedTile in [2,5,8]:
        return -1
    else:
        return currentSelectedTile + 1

def getLeftNeighborTile(currentSelectedTile):
    if currentSelectedTile in [0,3,6]:
        return -1
    else:
        return currentSelectedTile - 1

def getUpperNeighborTile(currentSelectedTile):
    if currentSelectedTile in [0,1,2]:
        return -1
    else:
        return currentSelectedTile - 3

def getLowerNeighborTile(currentSelectedTile):
    if currentSelectedTile in [6,7,8]:
        return -1
    else:
        return currentSelectedTile + 3

# define a main function
def main():

    # initialize the pygame module
    pygame.init()

    img = pygame.image.load("imageToSlide.jpg")
    pygame.display.set_icon(img)
    pygame.display.set_caption("Slide Game")


    background = pygame.image.load("imageToSlide.jpg")
    background.fill(BACKGROUNDCOLOR)

    """
    OriginTileX labels the part of the location of the upper left corner of each tile
    ImageTileX is the recangle of the corresponding frame in the original image
    |_|1|2|
    |3|4|5|
    |6|7|8|
    """
    # the image is split in 9 tiles and we add a small seperation line between
    width, height = img.get_width()/3, img.get_height()/3
    tileDimension = (width, height)

    # create a surface on screen (1 seperation before, 2 between and another behind)
    SCREEN_WIDTH, SCREEN_HEIGHT = img.get_width()+4*BORDERWIDTH, img.get_height()+4*BORDERWIDTH
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    originTile0 = (BORDERWIDTH, BORDERWIDTH)
    originTile1 = originTile0[0] + width + BORDERWIDTH, originTile0[1]
    originTile2 = originTile1[0] + width + BORDERWIDTH, originTile1[1]
    originTile3 = originTile0[0], originTile0[1] + height + BORDERWIDTH
    originTile4 = originTile1[0], originTile0[1] + height + BORDERWIDTH
    originTile5 = originTile2[0], originTile0[1] + height + BORDERWIDTH
    originTile6 = originTile0[0], originTile3[1] + height + BORDERWIDTH
    originTile7 = originTile1[0], originTile3[1] + height + BORDERWIDTH
    originTile8 = originTile2[0], originTile3[1] + height + BORDERWIDTH
    originTiles = [originTile0, originTile1, originTile2,
                   originTile3, originTile4, originTile5,
                   originTile6, originTile7, originTile8]

    imageTile0 = pygame.Rect((0,0), tileDimension)
    imageTile1 = pygame.Rect((width, 0), tileDimension)
    imageTile2 = pygame.Rect((2*width, 0), tileDimension)
    imageTile3 = pygame.Rect((0, height), tileDimension)
    imageTile4 = pygame.Rect((width, height), tileDimension)
    imageTile5 = pygame.Rect((2*width, height), tileDimension)
    imageTile6 = pygame.Rect((0, 2*height), tileDimension)
    imageTile7 = pygame.Rect((width, 2*height), tileDimension)
    imageTile8 = pygame.Rect((2*width, 2*height), tileDimension)
    imageTiles = [imageTile0, imageTile1, imageTile2,
                  imageTile3, imageTile4, imageTile5,
                  imageTile6, imageTile7, imageTile8]

    # Once a tile is selected we want to draw a BORDERWIDTH which goes around the entire tile
    # the rectangle (ie the BORDERWIDTH) start $BORDERWIDTH in front and should end $BORDERWIDTH behind
    borderDimension = (tileDimension[0] + BORDERWIDTH, tileDimension[1] + BORDERWIDTH)

    # The origin of the BORDERWIDTH for each tile is a little bit outside the tile
    def borderOrigin(originTile):
        return (originTile[0] - BORDERWIDTH/2, originTile[1] - BORDERWIDTH/2)

    borderTile0 = pygame.Rect(borderOrigin(originTile0), borderDimension)
    borderTile1 = pygame.Rect(borderOrigin(originTile1), borderDimension)
    borderTile2 = pygame.Rect(borderOrigin(originTile2), borderDimension)
    borderTile3 = pygame.Rect(borderOrigin(originTile3), borderDimension)
    borderTile4 = pygame.Rect(borderOrigin(originTile4), borderDimension)
    borderTile5 = pygame.Rect(borderOrigin(originTile5), borderDimension)
    borderTile6 = pygame.Rect(borderOrigin(originTile6), borderDimension)
    borderTile7 = pygame.Rect(borderOrigin(originTile7), borderDimension)
    borderTile8 = pygame.Rect(borderOrigin(originTile8), borderDimension)
    borderTiles = [borderTile0, borderTile1, borderTile2,
                   borderTile3, borderTile4, borderTile5,
                   borderTile6, borderTile7, borderTile8]

    # Draw the image Tiles 
    # At index i of this list there is the number of the tile of the original image
    currentImageTiles = [0,1,2,
                         3,4,5,
                         6,7,8]
    shuffle(currentImageTiles)

    currentEmptyTile = currentImageTiles.index(EMPTYIMAGETILE)
    currentSelectedTile = 0
    drawBorderAroundTile(screen, borderTiles[currentSelectedTile])

    for i in range(9):
        screen.blit(img, originTiles[i], imageTiles[currentImageTiles[i]])

    # empty tile should be background color
    screen.blit(background, originTiles[currentEmptyTile], imageTiles[currentEmptyTile])

    pygame.display.flip()

    def swapTiles(tileOne, tileTwo):
        imgTileOne = currentImageTiles[tileOne]
        imgTileTwo = currentImageTiles[tileTwo]
        if tileOne == currentEmptyTile:
            screen.blit(img, originTiles[tileOne], imageTiles[imgTileTwo])
            screen.blit(background, originTiles[tileTwo], imageTiles[imgTileOne])
        elif tileTwo == currentEmptyTile:
            screen.blit(background, originTiles[tileOne], imageTiles[imgTileTwo])
            screen.blit(img, originTiles[tileTwo], imageTiles[imgTileOne])
        currentImageTiles[tileOne], currentImageTiles[tileTwo] = currentImageTiles[tileTwo], currentImageTiles[tileOne]

    # define a variable to control the main loop
    running = True
    showWinningScreen = False

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            doQuit = (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
            if doQuit:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # determine new tile
                selectedTile = [tile for tile in borderTiles if tile.collidepoint(pos)]

                # remove old tile and draw new one
                drawBorderAroundTile(screen, borderTiles[currentSelectedTile], remove=True)
                currentSelectedTile = borderTiles.index(selectedTile[0])
                drawBorderAroundTile(screen, borderTiles[currentSelectedTile])

                pygame.display.flip()
            
            if (event.type == pygame.KEYDOWN):
                neighborTile = -1
                if (event.key == pygame.K_RIGHT):
                    neighborTile = getRightNeighborTile(currentSelectedTile)
                elif (event.key == pygame.K_LEFT):
                    neighborTile = getLeftNeighborTile(currentSelectedTile)
                elif (event.key == pygame.K_UP):
                    neighborTile = getUpperNeighborTile(currentSelectedTile)
                elif (event.key == pygame.K_DOWN):
                    neighborTile = getLowerNeighborTile(currentSelectedTile)

                if neighborTile == -1 or neighborTile != currentEmptyTile:
                    continue

                swapTiles(currentSelectedTile, neighborTile)

                # remove old tile and draw new one
                drawBorderAroundTile(screen, borderTiles[currentSelectedTile], remove=True)
                currentSelectedTile = neighborTile
                drawBorderAroundTile(screen, borderTiles[currentSelectedTile])

                currentEmptyTile = currentImageTiles.index(EMPTYIMAGETILE)

                pygame.display.flip()
            if currentImageTiles == list(range(9)):
                showWinningScreen = True
                running = False

    if showWinningScreen:
        screen.blit(img, originTile0)

        # draw winning text in the cente
        pygame.font.init()
        font = pygame.font.Font(None, 100)
        text = font.render("You win!", True, BACKGROUNDCOLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
        pygame.display.flip()

    while showWinningScreen:
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            doQuit = (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
            if doQuit:
                showWinningScreen = False


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
