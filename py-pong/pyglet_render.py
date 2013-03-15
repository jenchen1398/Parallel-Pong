from pygame.sprite import Sprite
import pygame
import pypong, sys
import SocketServer, struct

screen = None #setting them as global for now, may be better solution
ball = None
ballrect = None
paddle_left = None #these should be in array, just trying to make it work for now
paddle_left_rect = None
paddle_right = None
paddle_right_rect = None

black = 0,0,0

class BallRender(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        screen = pygame.disply.get_(surface)
        self.image = pygame.image.load('assets/paddle.png')
class broadcastServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
class requestHandler(SocketServer.StreamRequestHandler):
    #currentUserLogin={} #{clientArr:accountName}
    def handle(self):
        global screen, ball, ballrect, paddle_left_rect, paddle_right_rect
        posvec=self.request.recv(16)
        print(self.client_address)
        while posvec !='': 
            pos = struct.unpack( 'iiii',posvec )
            print( pos )
            ballrect.center= ( pos[0], pos[1] )
            print( pos[2], pos[3] )
            paddle_left_rect.y = ( pos[2] )
            paddle_right_rect.y = ( pos[3] )
            screen.fill( black )
            screen.blit( ball, ballrect) 
            screen.blit( paddle_right, paddle_right_rect )
            screen.blit( paddle_left, paddle_left_rect )
            pygame.display.flip()
            # self.wfile.write('server reply:{0}'.format(requestForUpdate))
            posvec=self.request.recv( 16 )
            print( posvec )
        print( 'client disconnect' )

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( (686,488) )
    #ball = BallRender()
    ball = pygame.image.load( 'assets/ball.png' )
    ballrect = ball.get_rect()
    paddle_left = pygame.image.load( 'assets/paddle.png' )
    paddle_left_rect = paddle_left.get_rect()
    paddle_left_rect.x = 84
    paddle_right = pygame.image.load( 'assets/paddle.png' )
    paddle_right_rect = paddle_right.get_rect()
    paddle_right_rect.x = 594
    server=broadcastServer( ( 'localhost',20000 ), requestHandler )
    server.serve_forever()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        
