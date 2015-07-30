from multiprocessing import Process
import master
import pongdisplay

def toDict(left, right, top, bot):
	disp = {}
	disp['left'] = left
	disp['right'] = right
	disp['bot'] = bot
	disp['top'] = top
	return disp


ip = "0.0.0.0"
port = 5000
totalwidth = 800
totalheight = 600

master = Process(target = master.setup, args = [ip, port, (totalwidth, totalheight)])
master.start()

total_display = toDict(0, totalwidth, 0, totalheight)
left = toDict(0, totalwidth/2, 0, totalheight)
right = toDict(totalwidth/2, totalwidth, 0, totalheight)

display = Process(target = pongdisplay.setup, args= [ip, port, right, total_display])
display.start()

display = Process(target = pongdisplay.setup, args= [ip, port, left, total_display])
display.start()



