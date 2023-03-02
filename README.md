# CivitAI_GalleryGrabber
Grabs the gallery of images for a particular model on CivitAI.com utilizing API calls with the model hash and using Python for image processing and tag application, all wrapped in a tkinter GUI.

# Notes
Will save all images in the selected folder for the model hash being downloaded. Be advised the folder resets after a batch is done and you will have to choose a new folder for the next model hash. If no download folder has been specified it will create an folder with the name of the model corresponding to the model hash and store the images inside of it.

# Usage
first run ```pip install -r requirements.txt``` from within the application directory. afterwards you can simply launch the application from the command line with ```python ./main.py```

# Todo

I am working to improve ease of launching and adding the ability to download a larger amount of model galleries using a list of model hashes.
