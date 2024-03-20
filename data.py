#!/usr/bin/python
print("Importing libraries..")
import time, math, smbus2 as sb
from time import sleep
import torch
from torchvision import transforms
import cv2 as cv
from PIL import Image
print("Importing done.")

DEVICE_BUS = 1 
DEVICE_ADDR = 0x12

my_data = (0x10, 0x11, 0x20, 0x32)
path_to_model = "tl_model.ptl"

print("Connect to bus.")
bus = sb.SMBus(DEVICE_BUS)
time.sleep(1)
i = 0 

# Helper functions
def predict_from_im(model, transform, image):
    # Convert OpenCV image to PIL Image
    color_converted_im = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(color_converted_im)

    # Apply transforms to work with model
    img = transform['predict'](pil_img)
    img = img.unsqueeze(0)

    with torch.no_grad():
        sleep(0.1)
        outputs = model(img)
        _, preds = torch.max(outputs, 1)
        return (outputs, preds)

if __name__ == '__main__':

    print("Loading the model...")
    time.sleep(1)
    # Load model that we trained
    model = torch.jit.load(path_to_model, map_location=torch.device('cpu'))
    model.eval()
    print("Model loaded.")

    # Use the same transforms as validation
    data_transforms = {
        'predict': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Set up the camera
    vc = cv.VideoCapture(0)
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()

        preds = predict_from_im(model, data_transforms, frame)
        print(preds)
        
        # Write to the device
        bus.write_byte(DEVICE_ADDR, 0x26)
        time.sleep(1)
        our_pr = preds[1]
        pr = our_pr[0]
       

       # ROMI HAS 5 ACTIONS
       # 0: STOP
       # 1: MOVE FORWARD
       # 2: MOVE BACKWARD
       # 3: TURN ON BUZZER
       # 4: TURN OFF BUZZER
       # 5: TURN ON YELLOW LED
       # 6: TURN OFF YELLOW LED
       # TODO:
       # You should set unknown to something you want
        
        # Stop the movement
        if pr.item() == 0:
            print("UNKNOWN")
            print("STOP")
            bus.write_byte(DEVICE_ADDR, 0)
        # move backward
        elif pr.item() == 1:
            print("TURN YELLOW LED ON")
            bus.write_byte(DEVICE_ADDR, 5)
        elif pr.item() == 2:
            print("TURN YELLOW LED OFF")
            bus.write_byte(DEVICE_ADDR, 6)
        elif pr.item() == 3:
            print("GO FORWARD")
            bus.write_byte(DEVICE_ADDR, 1)
        elif pr.item() == 4:
            print("GO BACKWARD")
            bus.write_byte(DEVICE_ADDR, 2)
        elif pr.item() == 5:
            print("BUZZER?")
            bus.write_byte(DEVICE_ADDR, 3)
        else:
            print("OUTSIDE RANGE")
            bus.write_byte(DEVICE_ADDR, 0)


        if cv.waitKey(1) == 27: # exit on ESC
            break

    vc.release()

