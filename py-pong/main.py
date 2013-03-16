import pypong
from pypong.player import BasicAIPlayer, KeyboardPlayer, MousePlayer
import socket
import struct
import time
num_of_clients = 4 #global that will hold the number of nodes we have
    
def run():
    configuration = {
        'screen_size': (2720,1536),
        'paddle_image': 'assets/paddle.png',
        'paddle_left_position': 84.,
        'paddle_right_position': 2636.,
        'paddle_velocity': 20.,
        'paddle_bounds': (0, 1536), # This sets the upper and lower paddle boundary.The original game didn't allow the paddle to touch the edge, 
        'line_image': 'assets/dividing-line.png',
        'ball_image': 'assets/ball.png',
        'ball_velocity': 30.,
        'ball_velocity_bounce_multiplier': 1.105,
        'ball_velocity_max': 60.,
        'score_left_position': (141, 30),
        'score_right_position': (473, 30),
        'digit_image': 'assets/digit_%i.png',
        'sound_missed': 'assets/missed-ball.wav',
        'sound_paddle': 'assets/bounce-paddle.wav',
        'sound_wall': 'assets/bounce-wall.wav',
        'sound': True,
    }
    #make a socket, and connect to a already running server socket
    # read some file with the ip addresses and put them in the variables ip addersses
    # hard coded for now
    clisocket = [ None, None, None, None ]
    ip_addresses = ( '10.10.0.10','10.10.0.20', '10.10.0.30', '10.10.0.40' )
    for x in range(0,num_of_clients):
        clisocket[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clisocket[x].connect((ip_addresses[x], 20000))
    clock = time.clock()
    input_state = {'key': None, 'mouse': None}
    
    # Prepare game
    #player_left = KeyboardPlayer(input_state, pygame.K_w, pygame.K_s)
    #player_right = MousePlayer(input_state)
    
    player_left = BasicAIPlayer()
    player_right = BasicAIPlayer()
    game = pypong.Game(player_left, player_right, configuration)

    
    # Main game loop
    while game.running:
        game.update()
        posvect = struct.pack('iiii', game.ball.position_vec[0], game.ball.position_vec[1], \
            game.paddle_left.rect.y, game.paddle_right.rect.y )
        # loop over clients and send the coordinates
        for x in range(0,num_of_clients):
            clisocket[x].sendall(posvect)
        # wait for them to send stuff back to avoid a race condition.
        for x in range(0,num_of_clients):
            clisocket[x].recv(100)
        # time.sleep(3)
        
if __name__ == '__main__': run()
