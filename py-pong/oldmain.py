import pygame, pypong
from pypong.player import BasicAIPlayer, KeyboardPlayer, MousePlayer
import socket
import threading,SocketServer,time

game = None

class requestHandler(SocketServer.StreamRequestHandler):
    #currentUserLogin={} #{clientArr:accountName}
    def handle(self):
        requestForUpdate=self.request.recv(1024)
	requestForUpdate=self.request.send(str(game.ball.position_vec[0]))
        #print(self.client_address)
        #while requestForUpdate!='':           
        #    print(requestForUpdate)
        #    self.wfile.write('server reply:{0}'.format(requestForUpdate))
        #    requestForUpdate=self.request.recv(1024)
        #print('client disconnect')

class broadcastServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):    
    pass


def run():
    configuration = {
        'screen_size': (686,488),
        'paddle_image': 'assets/paddle.png',
        'paddle_left_position': 84.,
        'paddle_right_position': 594.,
        'paddle_velocity': 6.,
        'paddle_bounds': (0, 488), # This sets the upper and lower paddle boundary.The original game didn't allow the paddle to touch the edge, 
        'line_image': 'assets/dividing-line.png',
        'ball_image': 'assets/ball.png',
        'ball_velocity': 4.,
        'ball_velocity_bounce_multiplier': 1.105,
        'ball_velocity_max': 32.,
        'score_left_position': (141, 30),
        'score_right_position': (473, 30),
        'digit_image': 'assets/digit_%i.png',
        'sound_missed': 'assets/missed-ball.wav',
        'sound_paddle': 'assets/bounce-paddle.wav',
        'sound_wall': 'assets/bounce-wall.wav',
        'sound': True,
    }
    #make a socket, and connect to a already running server socket
    #clisocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #clisocket.connect(('127.0.0.1', 23000))
    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.init()
    display_surface = pygame.display.set_mode(configuration['screen_size'])
    output_surface = display_surface.copy().convert_alpha()
    output_surface.fill((0,0,0))
    #~ debug_surface = output_surface.copy()
    #~ debug_surface.fill((0,0,0,0))
    debug_surface = None
    clock = pygame.time.Clock()
    input_state = {'key': None, 'mouse': None}
    
    # Prepare game
    #player_left = KeyboardPlayer(input_state, pygame.K_w, pygame.K_s)
    #~ player_right = MousePlayer(input_state)
    
    player_left = BasicAIPlayer()
    player_right = BasicAIPlayer()
    global game 
    game = pypong.Game(player_left, player_right, configuration)
    server=broadcastServer(('127.123.0.1',20000),requestHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon=True
    t.start()
    print('server start')
    
    # Main game loop
    timestamp = 1
    while game.running:
        clock.tick(60)
        now = pygame.time.get_ticks()
        if timestamp > 0 and timestamp < now:
            timestamp = now + 5000
            print clock.get_fps()
        input_state['key'] = pygame.key.get_pressed()
        input_state['mouse'] = pygame.mouse.get_pos()
        game.update()
	#this is where you would have to send the location out to all of the rpis
	#So the draw should be changed, everything else can stay the same 
        game.draw(output_surface)
        #~ pygame.surfarray.pixels_alpha(output_surface)[:,::2] = 12
        display_surface.blit(output_surface, (0,0))
        #clisocket.send(self.ball.position_vec)
        if debug_surface:
            display_surface.blit(debug_surface, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.running = False
        
if __name__ == '__main__': 

    run()
    server.socket.close()
