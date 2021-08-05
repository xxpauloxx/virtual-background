# Virtual Background
Virtual background using Python, OpenCV and Tensorflow for many applications, including teams, discord and slack. Basically the idea is to create a virtual webcam, which will receive processed images from the real webcam.



### DEPENDENCIES

You will need to install [v4l2loopback](https://github.com/umlaeute/v4l2loopback) on Linux to support virtual webcam. First step will be to install v4l2loopback, and then we will install Python dependencies.

```sh
$ sudo apt update
$ sudo apt install v4l2loopback-dkms
$ sudo modprobe v4l2loopback
$ python -m venv .env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```



### HOW TO WORKS

It takes 3 parameters, one with the address of the background image, another would be the address of the virtual webcam device and at the end the address of the webcam, in integer, format used by OpenCV.

```
$(.env) python vwebcam.py --background=./images/background.jpg --virtual-webcam-device=/dev/video4 --webcam-device=2
```

![](https://raw.githubusercontent.com/xxpauloxx/virtual-background/main/images/example.jpeg)

With the creativity to make many cool changes using OpenCV and have a differentiated image in video calls. `:sunglasses:`

### CONTACT

Any questions please contact us paulo.pinda@gmail.com

