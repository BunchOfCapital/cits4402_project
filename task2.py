def isBlue(region):
    blue_bounds = ([90,50,50], [150, 255, 255])
    green_bounds = ([30, 50, 50], [90, 255, 255])
    red_bounds = ([150, 50, 50], [180, 255, 255])

    #here we can consider true blue to be 120, true green to be 60 and true red to be 180, with a diffcolour of 30
    bounds = [blue_bounds, green_bounds, red_bounds]