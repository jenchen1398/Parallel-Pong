import pypong
from pypong.player import BasicAIPlayer, KeyboardPlayer, MousePlayer
import socket
import struct
import time
import threading
import os, sys
num_of_clients = 6 #global that will hold the number of nodes we have
player_left = None
def run():
    global player_left
    configuration = {
        'screen_size': (5773,2405),
        'paddle_image': 'assets/paddle.png',
        'paddle_left_position': 84.,
        'paddle_right_position': 5689.,
        'paddle_velocity': 70.,
        'paddle_bounds': (0, 2405), # This sets the upper and lower paddle boundary.The original game didn't allow the paddle to touch the edge, 
        'line_image': 'assets/dividing-line.png',
        'ball_image': 'assets/ball.png',
        'ball_velocity': 80.,
        'ball_velocity_bounce_multiplier': 1.105,
        'ball_velocity_max': 130.,
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
    clisocket = [ None, None, None, None, None, None ]
    ip_addresses = ( '10.10.0.10','10.10.0.11', '10.10.0.12', '10.10.0.13', '10.10.0.14', '10.10.0.15' )
    for x in range(0,num_of_clients):
        clisocket[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clisocket[x].connect((ip_addresses[x], 20000))
    clock = time.clock()
    input_state = None
    
    # Prepare game
    player_left = KeyboardPlayer(input_state, 'w', 's')
    #player_right = MousePlayer(input_state)
    
    #player_left = BasicAIPlayer()
    player_right = BasicAIPlayer()
    game = pypong.Game(player_left, player_right, configuration)
    os.system('stty raw')
    stdin_reader = StdinReader()
    stdin_reader.start()
    # root = tk.Tk()
    # print ("press a key")
    # root.bind_all('<Key>', key)
    # root.withdraw()
    # root.mainloop()
    
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
            clisocket[x].recv(16)
        # time.sleep(3)


# def key(event):
#     """shows key or tk code for the key"""
#     if event.keysym == 'Escape':
#         root.destroy()
#     if event.char == event.keysym:
#         # normal number and letter characters
#         print( 'Normal Key %r' % event.char )
#     elif len(event.char) == 1:
#         # charcters like []/.,><#$ also Return and ctrl/key
#         print( 'Punctuation Key %r (%r)' % (event.keysym, event.char) )
#     else:
#         # f1 to f12, shift keys, caps lock, Home, End, Delete ...
#         print( 'Special Key %r' % event.keysym )

class StdinReader(threading.Thread):
    def run(self):
        global player_left
        while True:
            x = sys.stdin.read(1)
            if x == 'w':
                player_left.input_state = 'w'
            elif x == 's':
                player_left.input_state = 's'
            else:
                player_left.input_state = None
            x = None

            # if repr(sys.stdin.read(1))
            # player_left
        
if __name__ == '__main__': run()
