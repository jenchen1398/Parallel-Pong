import pygame
import sys
import socket, struct, select, threading

#screen = None #setting them as global for now, may be better solution
#ball = None
#ballrect = None
#paddle_left = None #these should be in array, just trying to make it work for now
#paddle_left_rect = None
#paddle_right = None
#paddle_right_rect = None
#boundsx = [None, None] #left, right
#boundsy = [None, None] #top, bottom
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
    paddle_index = tile.paddle_index
    paddle_rect = tile.paddle.get_rect()

    ballrect   = tile.ball.get_rect()
    ballrect.x = data[0] - tile.left_edge # offset the bounds
    ballrect.y = data[1] - tile.top_edge 



    tile.screen.fill( BLACK )

    if ( data[0] > tile.left_edge - 96 and data[1] < tile.right_edge ):
        tile.screen.blit( tile.ball, ballrect )

    if tile.isEdge:
        if ( data[paddle_index] > tile.top_edge and data[paddle_index] < tile.bot_edge  ):
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

def setup(ip, port, display, total_display):
    pygame.init()
    tile = Tile()
    tile.screen = pygame.display.set_mode( (display['right'] - display['left'], display['bot'] - display['top']) )

    tile.ball = pygame.image.load( 'assets/ball.png' )

    read_pong_settings(display['left'], display['right'], display['bot'], display['top'], tile)
    pygame.mouse.set_visible(False)


    if ( display['right'] == total_display['right'] ):
        print 'right_edge_node'
        tile.paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = tile.paddle.get_rect()
        print paddle_rect.w
        tile.paddle.get_rect().x = 50#(display['right'] - (1920 - 1836)) - paddle_rect.width
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
     

    threading.Thread(target = detectClose, args = [s, tile]).start()


    while 1:
        read_sockets, _, _ = select.select([s], [], [], 0)

        for sock in read_sockets:
            if tile.active:
                posvec = sock.recv(16)
            #print 'posvec = ' + posvec
            if not posvec:
                print 'not posvec'
                sys.exit()

            
            handle(posvec, tile)

        

   
def detectClose(socket, tile):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                socket.send('j')
                tile.active = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()




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


    
    
        
        
