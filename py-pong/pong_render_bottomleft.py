from pygame.sprite import Sprite
import pygame
import sys
import SocketServer, struct

screen = None #setting them as global for now, may be better solution
ball = None
ballrect = None
paddle_left = None #these should be in array, just trying to make it work for now
paddle_left_rect = None
paddle_right = None
paddle_right_rect = None
boundsx = ( 0, 1360 ) #left, right
boundsy = ( 768, 1536 ) #top, bottom
right_edge_node = False
left_edge_node = True
ip_address = '10.10.0.20'
paddle_index = 0
edge_node = False

black = 0,0,0

class broadcastServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
class requestHandler(SocketServer.StreamRequestHandler):
    #currentUserLogin={} #{clientArr:accountName}
    def handle(self):
        global screen, ball, ballrect, paddle_left_rect, paddle_right_rect, bounds,\
            edge_node, paddle_index
        posvec=self.request.recv(16)
        print(self.client_address)
        while posvec !='':
            pos = struct.unpack( 'iiii',posvec )
            #print( pos )
            ballrect.x = pos[0] - boundsx[0] # offset the bounds
            ballrect.y = pos[1] - boundsy[0] 
            # print "ball postition"
            # print "x= " + str(ballrect.x)
            # print "y= " +str(ballrect.y)
            # print "center = " + str(ballrect.center)
            # print "top = " +str(ballrect.top)
            # print "bottom = " + str(ballrect.bottom)
            # print "left = " + str(ballrect.left)
            # print "right = " + str(ballrect.right)
            # print "topleft = " + str(ballrect.topleft)
            #print( pos[2], pos[3] )
            screen.fill( black )
            if ( pos[0] > boundsx[0] and pos[1] < boundsx[1] ):
                screen.blit( ball, ballrect )
            #don't care for now but will have to figure out what to do after
            # screen.blit( paddle_right, paddle_right_rect )
            if edge_node:
                if ( pos[paddle_index] > boundsy[0] and pos[paddle_index] < boundsy[1]  ):
                    paddle_rect.y = pos[paddle_index] - boundsy[0]
                    screen.blit( paddle, paddle_rect )
            pygame.display.flip()
            self.request.send( 'Got it' )
            try:
                posvec=self.request.recv( 16 )
            except:
                print( 'client disconnect' )
                pygame.quit()
                sys.exit()
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( (1360,768) )
    ball = pygame.image.load( 'assets/ball.png' )
    ballrect = ball.get_rect()
    if ( right_edge_node ):
        paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = paddle.get_rect()
        paddle_rect.x = 1276
        edge_node = True #will signal to update paddle as well
        paddle_index = 3
    elif( left_edge_node ):
        paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = paddle.get_rect()
        paddle_rect.x = 84
        edge_node = True #will signal to update paddle as well
        paddle_index = 2
    server=broadcastServer( ( ip_address,20000 ), requestHandler )
    server.serve_forever()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        
