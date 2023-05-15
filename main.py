from calibrate import *
from task2 import *

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

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
        # self.image_frame.grid_propagate(False)
        self.image_frame.pack(side=tk.TOP,expand=True,padx=10, pady=10)

        # Create a label to display the chosen image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side=tk.LEFT, padx=5, pady=5)
        # Create a label to display the filtered image 
        self.filtered_label = tk.Label(self.image_frame)
        self.filtered_label.pack(side=tk.RIGHT, padx=5, pady=5)
        #Create a frame for the buttons
        self.button_frame = tk.Frame(self.border,borderwidth=2, width=700, height=300)
        self.button_frame.pack(side=tk.TOP,expand=True,padx=10, pady=10)
        # Create a "Load Image" button
        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.display_image)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)
        # Create a "Detect Edges" button
        self.task1 = tk.Button(self.button_frame, text="Task 1", command  = self.task1)
        self.task1.pack(side=tk.LEFT, padx=5, pady=5)
        # Create a Scale widget for the Edge Detection
        # self.edge_size_var = tk.IntVar()
        # self.edge_scale = tk.Scale(self.button_frame, orient=tk.HORIZONTAL, from_=0.1, to=10.0, resolution=0.1, label="Threshhold for edge detection", variable=self.edge_size_var)
        # self.edge_scale.pack(side=tk.LEFT, padx=5, pady=5)
        # #Create a frame
        # self.low_frame = tk.Frame(self.border,borderwidth=2)
        # self.low_frame.pack(side=tk.TOP,expand=True,padx=10, pady=10)

        # self.algo_variable = tk.StringVar
        # self.comboBox = ttk.Combobox(self.low_frame, textvariable = self.algo_variable ,values=["Canny", "Prewitt", "Hough"])
        # self.comboBox.pack(side=tk.LEFT, padx=5, pady=5)
        # self.comboBox.current(0)
        # self.comboBox['state'] = 'readonly'

        # # Create a Scale widget for the Circle Radius
        # self.radius_var = tk.DoubleVar()
        # self.radius_scale = tk.Scale(self.low_frame, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, label="Approximate Radius for Circle Detection", variable=self.radius_var)
        # self.radius_scale.pack(side=tk.RIGHT, padx=5, pady=5)

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
        max_size = 600
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        self.original_image = self.original_image.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it on the left side
        photo = ImageTk.PhotoImage(self.original_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo


    def fit_image(self, new_image):
            # Resize the image to fit in the label
            width, height = new_image.size
            max_size = 600
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_width = int(width * (max_size / height))
                new_height = max_size
            new_image = new_image.resize((new_width, new_height))
            
            # Convert the image to Tkinter format and display it on the right side
            photo = ImageTk.PhotoImage(new_image)
            self.filtered_label.configure(image=photo)
            self.filtered_label.image = photo

    def task1(self):
    #load image and get mask by colour
        image = load_image(FILENAME)
        mask = cull_by_colour(image)

        #use the mask to label connected regions
        labelled = measure.label(mask)


        #specify values to exclude accidentally labelled objects
        min_area = 30
        max_area = 250

        axis_ratio = 0.5

        ellipse_threshold = 1


        #get list of region properties by which to cull bad regions
        current_candidates = measure.regionprops(labelled)

        #remove incorrectly identified regions
        current_candidates = cull_by_size(current_candidates, min_area, max_area)
        current_candidates = cull_by_roundness(current_candidates, axis_ratio)
        final_candidates, candidate_regions = cull_by_neighbours(current_candidates, ellipse_threshold)


        #Display labelled regions with colour
        image_label_overlay = color.label2rgb(labelled, image=image, bg_label=0)
        ig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(image_label_overlay)


        #draw boxes over the candidates that survived
        for region in final_candidates:
            # take the bounding box from regionprops to draw rectangles
            min_row, min_col, max_row, max_col = region.bbox
            rectangles = mpatches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, 
                fill=False, edgecolor='red', linewidth=1)
            ax.add_patch(rectangles)
            plt.annotate('lalala', (min_col, min_row), fontsize=10)
            # tp = TextPath((min_col, min_row), "Test", size=0.4)
            # plt.gca().add_patch(mpatches.PathPatch(tp, color="black"))

        for hexagon in candidate_regions:
            for pointInd in hexagon:
                if isBlue(final_candidates[pointInd]):
                    pass

        ax.set_axis_off()
        plt.tight_layout()
        plt.show()         

if __name__ == '__main__':
    root = tk.Tk()
    gui = ImageGUI(root)
    root.mainloop()
    # task1()