# import the pygame module, so you can use it
import pygame
BORDERCOLOR = (255, 0, 0)
BACKGROUNDCOLOR = (0, 0, 0)
BORDERWIDTH = 5

def drawBorderAroundTile(screen, tile, remove=False):
    if remove:
        pygame.draw.rect(screen, BACKGROUNDCOLOR, tile, BORDERWIDTH)
    else:
        pygame.draw.rect(screen, BORDERCOLOR, tile, BORDERWIDTH)

# the only tiles that have no right neighbor are 2,5 and 9. Otherwise just add 1
# the same logic applies to the other directions
def getRightNeighborTile(currentSelectedTile):
    if currentSelectedTile in [2,5,9]:
        return -1
    else:
        return currentSelectedTile + 1

def getLeftNeighborTile(currentSelectedTile):
    if currentSelectedTile in [2,5,9]:
        return -1
    else:
        return currentSelectedTile + 1

# define a main function
def main():

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Slide Game")


    # load image (it is in same directory)
    img = pygame.image.load("01_image.jpg")

    """
    OriginTileX labels the part of the location of the upper left corner of each tile
    ImageTileX is the recangle of the corresponding frame in the original image
    |_|1|2|
    |3|4|3|
    |6|7|8|
    """
    # the image is split in 9 tiles and we add a small seperation line between
    width, height = img.get_width()/3, img.get_height()/3
    tileDimension = (width, height)

    # create a surface on screen (1 seperation before, 2 between and another behind)
    screen = pygame.display.set_mode((1920+4*BORDERWIDTH,1080+4*BORDERWIDTH))

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

    screen.blit(img, originTile1, imageTile1)
    screen.blit(img, originTile2, imageTile2)
    screen.blit(img, originTile3, imageTile3)
    screen.blit(img, originTile4, imageTile4)
    screen.blit(img, originTile5, imageTile5)
    screen.blit(img, originTile6, imageTile6)
    screen.blit(img, originTile7, imageTile7)
    screen.blit(img, originTile8, imageTile8)

    def swapTiles(tileOne, tileTwo):
        screen.blit(img, originTiles[tileOne], imageTiles[tileTwo])
        screen.blit(img, originTiles[tileTwo], imageTiles[tileOne])

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

    currentEmptyTile = 0
    currentSelectedTile = 1
    drawBorderAroundTile(screen, borderTiles[currentSelectedTile])

    pygame.display.flip()

    # define a variable to control the main loop
    running = True

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

                # determine new tile (shouldn't be the current empty tile)
                selectedTile = [tile for tile in borderTiles if tile.collidepoint(pos)]
                if selectedTile[0] == borderTiles[currentEmptyTile]:
                    continue

                # remove old tile and draw new one
                drawBorderAroundTile(screen, borderTiles[currentSelectedTile], remove=True)
                currentSelectedTile = borderTiles.index(selectedTile[0])
                drawBorderAroundTile(screen, borderTiles[currentSelectedTile])

                pygame.display.flip()
            
            if (event.type == pygame.KEYDOWN)
                if (event.key == pygame.K_RIGHT):
                    neighborTile = getRightNeighborTile(currentSelectedTile)
                    swapTiles(1, 2)
                pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
