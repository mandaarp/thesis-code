import sys
import csv

if len(sys.argv) != 2:
    print "usage: " + sys.argv[0] + " <classification_result.csv>"
    exit

p_back="pedestrian-back"
p_front="pedestrian-front"
p_left="pedestrian-left"
p_right="pedestrian-right"

back_as_back=0
back_as_front=0
back_as_left=0
back_as_right=0

front_as_back=0
front_as_front=0
front_as_left=0
front_as_right=0

left_as_back=0
left_as_front=0
left_as_left=0
left_as_right=0

right_as_back=0
right_as_front=0
right_as_left=0
right_as_right=0

#f = open(sys.argv[1],"r")
#lines = f.readlines()
#f.close()
image_to_class = {}
for row in list(csv.reader(open(sys.argv[1],"r")))[1:]:
    if p_back == row[1]:
        if p_back in row[0]:
            back_as_back = back_as_back + 1
        if p_front in row[0]:
            front_as_back = front_as_back + 1
        if p_left in row[0]:
            left_as_back = left_as_back + 1
        if p_right in row[0]:
            right_as_back = right_as_back + 1

print "back_as_back: " + str(back_as_back)
print "front_as_back: " + str(front_as_back)
print "left_as_back: " + str(left_as_back)
print "right_as_back: " + str(right_as_back)

