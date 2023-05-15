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

    print("poop")
    print(sorted_hexagon[3].centroid)
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
        # if top_region.centroid[1]  < region.centroid[1]:  #to the right or bottom
        #     if region.centroid[0] > sorted_hexagon[3].centroid[0]: #new bottom
        #         sorted_hexagon[1] = sorted_hexagon[2]
        #         sorted_hexagon[2] = sorted_hexagon[3]
        #         sorted_hexagon[3] = region
        #     elif region.centroid[0] > sorted_hexagon[2].centroid[0]:
        #         sorted_hexagon[1] = sorted_hexagon[2]
        #         sorted_hexagon[2] = region
        #     elif region.centroid[0] > sorted_hexagon[1].centroid[0]:
        #         sorted_hexagon[1] = region
        # else: #left or bottom
        #     if region.centroid[0] > sorted_hexagon[3].centroid[0]: #new bottom
        #         sorted_hexagon[5] = sorted_hexagon[4]
        #         sorted_hexagon[4] = sorted_hexagon[3]
        #         sorted_hexagon[3] = region

        #     elif region.centroid[0] > sorted_hexagon[4].centroid[0]:
        #         sorted_hexagon[5] = sorted_hexagon[4]
        #         sorted_hexagon[4] = region
        #     elif region.centroid[0] > sorted_hexagon[5].centroid[0]:
        #         sorted_hexagon[5] = region