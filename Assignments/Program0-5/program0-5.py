import pygame as pg

# Helper function to create a scaled sprite surface from a 2D array
def getScaledSprite(spriteArray, scaleFactor):
    # Create raw surface
    rawSurf = pg.Surface((len(spriteArray[0]), len(spriteArray)))
    rawSurf.fill(TRANSPARENT_MAGENTA)
    rawSurf.set_colorkey(TRANSPARENT_MAGENTA)

    # Draw sprite onto the raw surface
    for i, row in enumerate(spriteArray):
        for j, color in enumerate(row):
            if color is not None:
                rawSurf.set_at((j, i), color)

    # Scale surface
    scaledSize = (rawSurf.get_width() * scaleFactor, rawSurf.get_height() * scaleFactor)
    scaledSurf = pg.transform.scale(rawSurf, scaledSize)
    
    return scaledSurf

# Center the drawn image
def blit_centered(screen, surface, pos):
    centered_x = pos[0] - surface.get_width() / 2
    centered_y = pos[1] - surface.get_height() / 2
    screen.blit(surface, (centered_x, centered_y))

# Pygame inits
pg.init()
pg.font.init()

# Colors
WHITE = (255,255,255)
TRANSPARENT_MAGENTA = (255,0,255)
BL = (0,0,0)
BY = "#FFD700"  # A bright gold/yellow color
DY = "#DAA520"  # A darker, goldenrod-like yellow for shading
TRANSPARENT = (0, 0, 0, 0) # A transparent color for empty pixels
NA = None

# Screen setup
screenWidth = 800
screenHeight = 600
screen = pg.display.set_mode((screenWidth,screenHeight))

# ASCII setup
text = pg.font.SysFont('Arial',72)
textRender = text.render('Adriean Lemoine',True,BL)
textPos = textRender.get_rect(x=410, y=50)

# Sprite setup
triforceArray = [
    [NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA],
    [NA, NA, NA, NA, NA, NA, NA, NA, DY, BY, NA, NA, NA, NA, NA, NA, NA, NA],
    [NA, NA, NA, NA, NA, NA, NA, DY, BY, BY, BY, NA, NA, NA, NA, NA, NA, NA],
    [NA, NA, NA, NA, NA, NA, DY, BY, BY, BY, BY, BY, NA, NA, NA, NA, NA, NA],
    [NA, NA, NA, NA, NA, DY, BY, BY, BY, BY, BY, BY, BY, NA, NA, NA, NA, NA],
    [NA, NA, NA, NA, DY, BY, NA, NA, NA, NA, NA, NA, DY, BY, NA, NA, NA, NA],
    [NA, NA, NA, DY, BY, BY, BY, NA, NA, NA, NA, DY, BY, BY, BY, NA, NA, NA],
    [NA, NA, DY, BY, BY, BY, BY, BY, NA, NA, DY, BY, BY, BY, BY, BY, NA, NA],
    [NA, DY, BY, BY, BY, BY, BY, BY, BY, DY, BY, BY, BY, BY, BY, BY, BY, NA],
    [DY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY, BY]
]
starArray = [
    [NA, NA, NA, NA, BY, NA, NA, NA, DY, BY, NA, NA, NA, BY, NA, NA, NA, NA],
    [NA, BY, NA, NA, NA, BY, NA, DY, BY, BY, NA, NA, BY, NA, NA, BY, NA, NA],
    [NA, NA, BY, NA, NA, NA, NA, DY, BY, BY, BY, NA, NA, NA, BY, NA, NA, NA],
    [NA, NA, NA, NA, NA, NA, DY, BY, BY, BY, BY, BY, NA, NA, NA, NA, NA, NA],
    [NA, NA, DY, DY, DY, DY, DY, BY, BL, BY, BL, BY, DY, DY, DY, NA, NA, NA],
    [NA, NA, BY, BY, BY, BY, BY, BY, BL, BY, BL, BY, BY, BY, BY, NA, NA, NA],
    [NA, NA, NA, BY, BY, BY, BY, BY, BL, BY, BL, BY, BY, BY, NA, NA, NA, NA],
    [BY, BY, NA, NA, BY, BY, BY, BY, BY, BY, BY, BY, BY, NA, NA, BY, BY, NA],
    [NA, NA, NA, NA, NA, DY, BY, BY, BY, BY, BY, BY, NA, NA, NA, NA, NA, NA],
    [NA, NA, NA, NA, DY, BY, BY, BY, BY, BY, BY, BY, BY, NA, NA, NA, NA, NA],
    [NA, NA, NA, NA, DY, BY, BY, BY, NA, NA, BY, BY, BY, NA, NA, NA, NA, NA],
    [NA, NA, NA, DY, BY, BY, BY, NA, NA, NA, NA, BY, BY, BY, NA, NA, NA, NA],
    [NA, NA, NA, DY, BY, BY, NA, NA, BY, NA, NA, NA, BY, BY, NA, NA, NA, NA],
    [NA, NA, NA, NA, NA, NA, NA, NA, BY, NA, NA, NA, NA, NA, NA, NA, NA, NA],

]

# Generate surfaces
triforce = getScaledSprite(triforceArray,20)
star = getScaledSprite(starArray,10)

# Maintain list of surfaces to draw
surfList = []
surfList.append([textRender,textPos])
surfList.append([triforce,(400,300)])

# Main loop
running = True
while running:
    # Quit event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    # Mouse event
    if event.type == pg.MOUSEBUTTONDOWN:
        x, y = event.pos
        surfList.append([star, (x,y)])
        
    # Set background and fill screen with provided surfaces
    screen.fill(WHITE)
    for surface, pos in surfList:
        blit_centered(screen, surface, pos)

    # Update the display
    pg.display.flip()

pg.quit()
