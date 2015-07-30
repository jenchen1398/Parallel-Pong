import pypong, socket, struct, threading, select, time, pygame
from pypong.player import BasicAIPlayer, Player

player_left = None # set the players as global so the control thread has access
player_right = None # simplest way to do it
def setup(ip, port, display):
    global player_left, player_right
    configuration = {
        'screen_size': display,
        'paddle_image': 'assets/paddle.png',
        'paddle_left_position': 184.,
        'paddle_right_position': display[0] - pygame.image.load( 'assets/paddle.png' ).get_rect().w,
        'paddle_velocity': 120.,
        'paddle_bounds': (1, 768),  
        'line_image': 'assets/dividing-line.png',
        'ball_image': 'assets/ball.png',
        'ball_velocity': 80.,
        'ball_velocity_bounce_multiplier': 1.105,
        'ball_velocity_max': 130.,
    }
    #make a socket, and connect to a already running server socket
    # read some file with the ip addresses and put them in the variables ip addersses
    # hard coded for now
    
    connections = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen(15)

    connections.append(server_socket)

    # Prepare game
    player_left = Player(None, 'up', 'down')
    player_right = Player(None, 'up', 'down')
    
    #player_left = BasicAIPlayer()
    #player_right = BasicAIPlayer()
    game = pypong.Game(player_left, player_right, configuration)
    #controls = RPIGPIO()
    #controls.start()
    # Main game loop
    while game.running:
        if findnewConnections(connections, server_socket):
            break
        game.update()

        #print str(game.ball.position_vec[0]) + '-' + str(game.ball.position_vec[1]) + '-' + str(game.paddle_left.rect.y) + '-' + str(game.paddle_right.rect.y)

        posvect = struct.pack('iiii', game.ball.position_vec[0], game.ball.position_vec[1], game.paddle_left.rect.y, game.paddle_right.rect.y )
        # loop over clients and send the coordinates
        for sock in connections:
            if sock != server_socket:
                sock.send(posvect)
        

        # wait for them to send stuff back to avoid a race condition.
        #for x in range( 0,len( clisocket ) ):
            #clisocket[x].recv( 16 )
        time.sleep(0.1)

    print 'server is closing'
    server_socket.close()

def findnewConnections(connections, server_socket):
    read_sockets, write_sockets, error_sockets = select.select(connections,[],[], 0.)

    for sock in read_sockets:
        if sock == server_socket:
            sockfd, addr = server_socket.accept()
            connections.append(sockfd)
        else:
            connections.remove(sock)
            sock.close()
            return True

    return False


class RPIGPIO( threading.Thread ):
    def run( self ):
        global player_left, player_right
        #GPIO.setwarnings( False )
        #GPIO.setmode( GPIO.BOARD )
        up1 = 7
        down1 = 11
        up2 = 13
        down2 = 15
       # GPIO.setup( up1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
       # GPIO.setup( down1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
       # GPIO.setup( up2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
       # GPIO.setup( down2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

        while True:
            #if GPIO.input( up1 ):
                player_left.input_state = 'up'
            #elif GPIO.input( down1 ):
                player_left.input_state = 'down'
            #else:
                player_left.input_state = None

           # if GPIO.input( up2 ):
                player_right.input_state = 'up'
           # elif GPIO.input( down2 ):
                player_right.input_state = 'down'
           # else:
                player_right.input_state = None
        

