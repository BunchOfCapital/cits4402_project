from calibrate import *
from task2 import *
from task3 import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import json
FILENAME = ""

class ImageGUI:
   
    def __init__(self, master):
        self.master = master
        self.master.title("Image GUI")

        # Create a frame for the GUI and center it
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=10, pady=10)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        # Create a border for the GUI
        self.border = tk.Frame(self.frame, borderwidth=2, relief="groove")
        self.border.grid(row=0, column=0, sticky="nsew")
        #Frame for the images
        self.image_frame = tk.Frame(self.border,borderwidth=2, width=900   , height=600)
        self.image_frame.pack(side=tk.TOP,expand=True,padx=10, pady=10)
        # Create a label to display the chosen image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side=tk.LEFT, padx=5, pady=5)
        #Create a frame for the buttons
        self.button_frame = tk.Frame(self.border,borderwidth=2, width=700, height=300)
        self.button_frame.pack(side=tk.TOP,expand=True,padx=10, pady=10)
        # Create a "Load Image" button
        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.display_image)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)
        # Create a "Task 1" button
        self.task1but = tk.Button(self.button_frame, text="Task 1", command  = self.task1)
        self.task1but.pack(side=tk.LEFT, padx=5, pady=5)
        # Create a "Task 2" button
        self.task2but = tk.Button(self.button_frame, text="Task 2", command  = lambda: self.task1(task2= True))
        self.task2but.pack(side=tk.LEFT, padx=5, pady=5)
        self.task3but = tk.Button(self.button_frame, text="Task 3", command  = self.main)
        self.task3but.pack(side=tk.LEFT, padx=5, pady=5)

    def display_image(self):
        # Open a file selection dialog box to choose an image file
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        global FILENAME
        FILENAME = file_path

        # Load the chosen image using PIL
        self.original_image = Image.open(file_path)
        self.original_path = file_path
        # Resize the image to fit in the label
        width, height = self.original_image.size
        max_size = 900
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        self.original_image = self.original_image.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it 
        photo = ImageTk.PhotoImage(self.original_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def task1(self, filename= False, task2 = False):
        #load image and get mask by colour
        if not filename:
            filename = FILENAME
        image = load_image(filename)
        blurred = cv2.GaussianBlur(image,(11,11),0)
        coloured = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cull_by_colour(image)

        #use the mask to label connected regions
        labelled = measure.label(mask)

        #specify values to exclude accidentally labelled objects
        min_area = 2
        max_area = 250
        axis_ratio = 0.1
        ellipse_threshold = 0.2


        #get list of region properties by which to cull bad regions
        current_candidates = measure.regionprops(labelled)

        #remove incorrectly identified regions
        current_candidates = cull_by_size(current_candidates, min_area, max_area)
        current_candidates = cull_by_roundness(current_candidates, axis_ratio)
        
        final_candidates, candidate_regions = cull_by_neighbours(current_candidates, ellipse_threshold, coloured)



        #Display labelled regions with colour
        # image_label_overlay = color.label2rgb(labelled, image=image, bg_label=0)
        ig, ax = plt.subplots(figsize=(10, 6))
        im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(im_rgb)
        points_coords = []
        points_strings = []

        for hexagon in candidate_regions: 
            #A hexagon is a group of 6 regions
            top_region = hexagon[0]
            hexaString = ""
            sorted_hexagon = []
            for region in hexagon:
                totalHue = 0
                blueCount = 0
                for x, y in  region.coords:
                    totalHue += coloured[x,y][0]
                avgHue = totalHue / len(region.coords)
                
                if 95 < avgHue and avgHue < 131:
                    blueCount += 1
                    if blueCount > 1: 
                    #If there are multiple blue points go to next hexagon
                        break
                    top_region = region
                    sorted_hexagon, hexaString = calculateHexagon(coloured, hexagon, top_region)
            if not sorted_hexagon:
                continue

            for ind, region in enumerate(sorted_hexagon):
                #Drawing Rectangles
                min_row, min_col, max_row, max_col = region.bbox
                rectangles = mpatches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, 
                fill=False, edgecolor='red', linewidth=1)
                ax.add_patch(rectangles)

                if task2:
                    #Drawing Circles
                    x_centre, y_centre = calculate_centroid(region, image)
                    circle = mpatches.Circle((x_centre,y_centre), .5, color = "red", fill = True )
                    ax.add_patch(circle)
                    #Adding Strings
                    finString = hexaString + str(ind)
                    plt.annotate(finString, (min_col, min_row), fontsize=10)
                    points_coords.append((x_centre,y_centre))
                    points_strings.append(finString)

        ax.set_axis_off()
        plt.tight_layout()
        plt.show()  

        return points_coords, points_strings


    def main(self):
        list_of_cameras_images = [("zedLeft720p.json", "camera 11/2022_12_15_15_51_19_927_rgb_left.png"),
                                ("zedRight720p.json","camera 11/2022_12_15_15_51_19_927_rgb_right.png"),
                                ("realsense71RGB.json","camera 71/2022_12_15_15_51_19_944_rgb.png"),
                                ("realsense72RGB.json","camera 72/2022_12_15_15_51_19_956_rgb.png"),
                                ("realsense73RGB.json","camera 73/2022_12_15_15_51_19_934_rgb.png"),
                                ("realsense74RGB.json","camera 74/2022_12_15_15_51_19_951_rgb.png")]
        
        list_cameras = []
        for name, image in list_of_cameras_images: 
            coords, HexStrings = self.task1(image, task2=True)
            with open('camera parameters/'+name, 'r') as f:
                json_read = json.load(f)
            list_cameras.append([json_read, HexStrings , coords])
        

        task3(list_cameras)


    


if __name__ == '__main__':
    root = tk.Tk()
    gui = ImageGUI(root)
    # gui.main()
    root.mainloop()
