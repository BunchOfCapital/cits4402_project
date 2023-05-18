from calibrate import *
def calculateHexagon(image, hexagon, top_region):
    # green_bounds = ([30, 50, 50], [90, 255, 255])
    # red_bounds = ([150, 50, 50], [180, 255, 255])
    sorted_hexagon = [top_region] * 6 
    hex_string = [""]*5
    deepestHex = sorted(hexagon, key=lambda x: x.centroid[0])
    sorted_hexagon[3] = deepestHex[5] #bottom
    for ind in range(1,3):
        region = hexagon[ind]
        if top_region.centroid[1]  < region.centroid[1]:
            sorted_hexagon[1] = region
        else:
            sorted_hexagon[5] = region
    for ind in range(3,5):
        region = hexagon[ind]
        if top_region.centroid[1]  < region.centroid[1]:
            sorted_hexagon[2] = region
        else:
            sorted_hexagon[4] = region

    for ind, region in enumerate(sorted_hexagon):
        totalHue = 0
        for x, y in  region.coords:
            totalHue += image[x,y][0]
        avgHue = totalHue / len(region.coords)
        # print(avgHue)
        if 30 < avgHue and avgHue < 95: #Green
            hex_string[ind-1] = 'G'
        elif 150< avgHue and avgHue < 180: #Red
            hex_string[ind-1] = 'R'
        else:
            hex_string[ind-1] = '?'

    
    finalString = "HexaTarget_"
    for c in hex_string: 
        finalString = finalString+ c
    
    return sorted_hexagon, finalString


def caculate_weight(point_i,average_intensity , max_i):
    numerator = np.linalg.norm(point_i - average_intensity)
    denominator=   np.linalg.norm(max_i - average_intensity)
    return 1 - (numerator/denominator)

def calculate_centroid(region , image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    coord_list = region.coords 
    total_weight = 0
    total_point_x = 0
    total_point_y = 0
    num_pixels = len(coord_list)
    max_intensity = 0
    total_intensity = 0
    for y,x in coord_list:
        total_intensity += img_gray[y][x] 
        if img_gray[y][x] > max_intensity:
            max_intensity = img_gray[y][x]
    average_intensity = total_intensity/num_pixels

    for y, x in coord_list:
        intensity = img_gray[y][x] 

        weight = caculate_weight(intensity,average_intensity,max_intensity)
        total_weight += weight
        total_point_x += weight * x
        total_point_y += weight * y
    y_centroid = total_point_y / total_weight
    x_centroid = total_point_x/ total_weight
    #For all p in the dilated E     

    return x_centroid, y_centroid