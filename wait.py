#!/usr/bin/python
'''
This program does the same things as data.py, except it waits for user
input to continue.

'''

print("importing libraries..")
import time, math, smbus2 as sb
from time import sleep
import torch
from torchvision import transforms
import cv2 as cv
from PIL import Image
print("Done importing.")

DEVICE_BUS = 1 
DEVICE_ADDR = 0x12

my_data = (0x10, 0x11, 0x20, 0x32)

print("Connect to bus.")
bus = sb.SMBus(DEVICE_BUS)
sleep(1)
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
        print("output !!")
        sleep(0.1)
        outputs = model(img)
        _, preds = torch.max(outputs, 1)
        return (outputs, preds)

if __name__ == '__main__':

    print("Loading the model...")
    sleep(1)
    # Load model that we trained
    model = torch.jit.load("tl_model.ptl", map_location=torch.device('cpu'))
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

        while():
            pass

        preds = predict_from_im(model, data_transforms, frame)
        print(preds)
        
        # Write to the device
        bus.write_byte(DEVICE_ADDR, 0x26)
        sleep(0.1)
        our_pr = preds[1]
        pr = our_pr[0]
       

       # ROMI HAS 5 ACTIONS
       # 0: MOVE FORWARD
       # 1: MOVE BACKWARD
       # 2: STOP
       # 3: TURN 90
       # 4: TURN -90
       # TODO:
       # You should set unknown to something you want
        if pr.item() == 0:
            print("Stop.")
            bus.write_byte(DEVICE_ADDR, 2)
        elif pr.item() == 1:
            print("Backward.")
            bus.write_byte(DEVICE_ADDR, 1)
        elif pr.item() == 2:
            print("Forward.")
            bus.write_byte(DEVICE_ADDR, 0)
        else:
            bus.write_byte(DEVICE_ADDR, pr.item())


        if cv.waitKey(1) == 27: # exit on ESC
            break

    vc.release()


'''
while True:
    bus.write_byte(DEVICE_ADDR, 0x26)
    print("Type F to move forward, B backward, S to stop, T to turn.")
    c = input(">>> ")
    if c == 'F':
        bus.write_byte(DEVICE_ADDR, 0)
    elif c == 'B':
        bus.write_byte(DEVICE_ADDR, 1)
    elif c == 'S':
        bus.write_byte(DEVICE_ADDR, 2)
    elif c == 'T':
        print("Between 10 and 360 degrees, how much would you want to turn? Type X to cancel.")
        i = input(">>> ")
        if i == 'X':
            pass
        elif int(i) < 10 or int(i) > 360:
            pass
        else:
            bus.write_byte(DEVICE_ADDR, int(i))
    else:
        pass
    sleep(0.2)
    print("hi")
'''
