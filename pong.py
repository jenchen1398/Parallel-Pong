from multiprocessing import Process
import master
import pongdisplay
import sys, platform


def toBounds(left, right, top, bot):
	disp = {}
	disp['left'] = left
	disp['right'] = right
	disp['bot'] = bot
	disp['top'] = top
	return disp

def disp(section, start):
	total_display = toBounds(0, totalwidth, 0, totalheight)
	Process(target = pongdisplay.setup, args= [ip, port, section, total_display, start]).start()


local = (len(sys.argv) != 1)

if local:
	totalwidth = 1200
	totalheight = 900

	ip = "0.0.0.0"
	port = 5000

	rows = 3
	cols = 5

	for w in reversed(range(rows)):
		for h in range(cols):
			width = totalwidth/cols
			left = width * h
			right = left + width

			height = totalheight/rows
			top = height * w
			bot = top + height

			disp(toBounds(left, right ,top, bot), (left,top) )

	master = Process(target = master.setup, args = [ip, port, (totalwidth, totalheight)])
	master.start()

else:
	TOTAL_WIDTH = 1200
	TOTAL_HEIGHT = 900
	COLS = 5
	ROWS = 3
	name = platform.node()
	if name == 'master':
		master.setup(ip, port, (totalwidth, totalheight))
	else if not name.startswith('tile-'):
		'pong running on odd computer'
	else:
		xcoord = name[5]
		ycoord = name[7]

		width = TOTAL_WIDTH/COLS
		left = width * xcoord
		right = left + width

		height = TOTAL_HEIGHT/ROWS
		top = height * ycoord
		bot = top + height

		bounds = toBounds(left, right, top, bot)
		total_display = (0, TOTAL_WIDTH, 0, TOTAL_HEIGHT
		pongdisplay.setup(ip, port, bounds, total_display None)


	
