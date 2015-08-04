import pygame
import sys
import socket, struct, select, threading
import pypong.entity as entity
import os


BLACK = 0,0,0
LEFT_PADDLE = 2
RIGHT_PADDLE = 3

#class broadcastServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    #pass
#class requestHandler(posvec):
def handle(posvec, tile):
    if not tile.active:
        sys.exit()

    data = struct.unpack( 'iiii',posvec )
    tile.screen.fill( BLACK )
    
    paddle_index = tile.paddle_index
 
    paddleTopEdge = data[paddle_index]
    paddleBotEdge = paddleTopEdge + entity.PADDLE_LENGTH


    ballRightEdge = data[0] + 96
    ballLeftEdge  = data[1]


    if ( ballRightEdge > tile.left_edge and ballLeftEdge < tile.right_edge ):
        ballrect   = tile.ball.get_rect()
        ballrect.x = data[0] - tile.left_edge # offset the bounds
        ballrect.y = data[1] - tile.top_edge 
        tile.screen.blit( tile.ball, ballrect )

    if tile.isEdge:
        if ( paddleBotEdge > tile.top_edge and paddleTopEdge < tile.bot_edge  ):
            paddle_rect  = tile.paddle.get_rect()
            if paddle_index == RIGHT_PADDLE:
                paddle_rect.x = tile.right_edge - (paddle_rect.w + tile.left_edge)
            paddle_rect.y = data[paddle_index] - tile.top_edge
            tile.screen.blit( tile.paddle, paddle_rect )

    pygame.display.flip()
        #self.request.send( 'Got it' )
        #try:
          #  posvec=self.request.recv( 16 )
       # except:
          #  print( 'client disconnect' )
    #         pygame.quit()
    #         sys.exit()
    # pygame.quit()
    # sys.exit()

def read_pong_settings(left_edge, right_edge, bot_edge, top_edge, tile):
    # put in seperate function since it's special. Could have been done easier
    #settings = open( 'Pong Renders/settings.txt', 'r' )
    #line = settings.readline()
    tile.left_edge = left_edge
    tile.right_edge = right_edge
    tile.bot_edge = bot_edge
    tile.top_edge = top_edge

def setup(ip, port, display, total_display, coords = None):
    if coords != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % coords
    pygame.init()
    tile = Tile()
    tile.screen = pygame.display.set_mode( (display['right'] - display['left'], display['bot'] - display['top']))

    tile.ball = pygame.image.load( 'assets/ball.png' )

    read_pong_settings(display['left'], display['right'], display['bot'], display['top'], tile)
    pygame.mouse.set_visible(False)


    if ( display['right'] == total_display['right'] ):
        print 'right_edge_node'
        tile.paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = tile.paddle.get_rect()
        tile.isEdge = True #will signal to update paddle as well
        tile.paddle_index = RIGHT_PADDLE

    if( display['left'] == total_display['left'] ):
        print 'left_edge_node'
        tile.paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = tile.paddle.get_rect()
        tile.isEdge = True #will signal to update paddle as well
        tile.paddle_index = LEFT_PADDLE

    #else:
     #   print 'nope'
     #   edge_node = False
    pygame.display.flip()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try :
        s.connect((ip, port))
    except :
        print 'Unable to connect'
        sys.exit()


    while 1:
        read_sockets, _, _ = select.select([s], [], [], 0)

        for sock in read_sockets:
            if tile.active:
                posvec = sock.recv(16)
            if not posvec:
                sys.exit()

            handle(posvec, tile)

class Tile:
    active = True
    isEdge = False
    ball = None
    screen = None
    bot_edge = 0
    top_edge = 0
    right_edge = 0
    left_edge = 0
    boundsy = (0, 0)
    left_edge_node = ''
    right_edge_node = ''
    paddle_index = 0


    
    
        
        
