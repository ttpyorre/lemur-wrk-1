import cv2 as cv
import os
from time import sleep

# Create directory for current item
item = input("Enter the name of your item for training: ")

if not os.path.exists(f"train/{item}") or not os.path.exists(f"validate/{item}"): # Make directories to store training and validation images
    print(f"Creating training and validation directories for {item}")
    os.makedirs(f"train/{item}")
    os.makedirs(f"validate/{item}")

print(f"Prep {item} and camera.")
sleep(5)

# Set up the camera
vc = cv.VideoCapture(0)

# Check that it's working
result, image = vc.read()

if result:
    for i in range(1, 401): # Take 400 images of the item
        print(f"Image #{i}")
        
        result, image = vc.read() # Capture image

        if i % 5 == 0: # Save most images to training set
            cv.imwrite(f'validate/{item}/{item}_sample_{i}.png', image)

        else: # Save a few for validation
            cv.imwrite(f'train/{item}/{item}_sample_{i}.png', image) # Save image to file
        if (i % 40 == 0) and i != 0:
            wait = input("Ready for new pose? Press any key to continue.")

# We're done, close everything down
vc.release()
