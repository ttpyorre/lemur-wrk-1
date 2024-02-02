# lemur-wrk-1
Lemur MQP 1st Workshop

This is the first workhop the Lemur MQP is running. By the end of the workshop you will be connecting to a romi, and running your model on the romi.

Here are the romis and their respective addresses:

**Lavasoa** -- autoreg-6602086.dyn.wpi.edu  
**Goldenbamboo** -- autoreg-6602106.dyn.wpi.edu  

**Ringtailed** -- autoreg-6602101.dyn.wpi.edu  
**Redruffed** -- autoreg-6602100.dyn.wpi.edu  

**Mongoose** -- autoreg-6602075.dyn.wpi.edu  
**Graymouse** --autoreg-6602097.dyn.wpi.edu  


## How to ssh into the pi:

In Linux and Windows, command prompt or terminal you can type the following:
ssh lemur@autoreg-#######.dyn.wpi.edu
password will be the name of the Pi.

Ex:
> ssh lemur@autoreg-6602086.dyn.wpi.edu
>
> Password: lavasoa


## Where to find the necessary code in the pi

In the terminal when accessing the pi, first do the following command:
> ls

then you should see all the directories in the system. Especially one called lemur-wrk-1
Now do:
> cd lemur-wrk-1

here you can find the data.py file, which you run after transferrin tl_model.tl to the system.
