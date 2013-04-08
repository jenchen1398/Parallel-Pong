# Script for generating the settings file used by the rendering nodes.
import sys
import re
# # boundsx[0] 
# 0 
# # boundsx[1] 
# 1360  
# # boundsy[0]
# 0   
# # boundsy[1]
# 768
# # right_edge_node 
# False
# # left_edge_node
# True
# # ip_address 
# 10.10.0.10 

aspect_ratio = raw_input('What is the demensions of the display wall in number' \
  'of monitors i.e. 5x3?[WxH]')
aspect_ratio = re.sub(r'\s+', '', aspect_ratio)
# match on numbers to width and height
width_num = re.search('(?<!x)\d+', aspect_ratio)
width_num = int(width_num.group(0))
height_num = re.search('(?<=x)\d+', aspect_ratio)
height_num = int(height_num.group(0))

aspect_ratio = raw_input('What is the demensions of the monitors?[WxH]')
print aspect_ratio
# take out any white space
aspect_ratio = re.sub(r'\s+', '', aspect_ratio)

# match on numbers to width and height
width = re.search('(?<!x)\d+', aspect_ratio)
width = int(width.group(0))
height = re.search('(?<=x)\d+', aspect_ratio)
height = int(height.group(0))

french_windowing = raw_input('Finally, what is the distance (in pixels) between'\
          + ' each monitor horizontally?')
offsetx = re.search( '\d+', french_windowing )
offsetx = int( offsetx.group( 0 ) )

french_windowing = raw_input( 'Vertically?' )
offsety = re.search( '\d+', french_windowing )
offsety = int( offsety.group( 0 ) )

previous_x = 0
previous_y = 0
boundsx = [ None, None ]
boundsy = [ None, None ]
ip = 10
# write file
for x in range(0,width_num):
  boundsx[0] = previous_x + x
  boundsx[1] = boundsx[0] + width
  previous_x = boundsx[1] + offsetx # offset to negate windowing effect
  previous_y = 0
  for y in range(0,height_num):
    #new bounds
    boundsy[0] = previous_y + y
    boundsy[1] = boundsy[0] + height

    #write the bounds
    outfile = open( str(x)+ ':' + str(y) + ' Settings.txt', 'w' )
    outfile.write( '# boundsx[0]\n' )
    outfile.write( str(boundsx[0])+'\n' )
    outfile.write( '# boundsx[1]\n' )
    outfile.write( str(boundsx[1])+'\n' )
    outfile.write( '# boundsy[0]\n' )
    outfile.write( str(boundsy[0])+'\n' )
    outfile.write( '# boundsy[1]\n' )
    outfile.write( str(boundsy[1])+'\n' )

    #write the edge node booleans
    outfile.write( '# right_edge_node\n' )
    if x == width_num - 1:
      outfile.write( 'True\n' )
    else:
      outfile.write( 'False\n' )

    outfile.write( '# left_edge_node\n' )
    if x == 0:
      outfile.write( 'True\n' )
    else:
      outfile.write( 'False\n' )
    #write the ip address
    outfile.write( '# ip_address\n' )
    outfile.write( '10.10.0.' + str(ip) )
    outfile.close()

    # update ip plus add the offset
    ip += 1
    previous_y = boundsy[1] + offsety
