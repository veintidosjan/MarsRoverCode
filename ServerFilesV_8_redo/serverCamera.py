from picamera import PiCamera
from time import sleep, strftime


def cameraLocalSave():
    i = 0
    while True:
        with PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            serverFileName = '/home/pi/serverPhotos/ServerImage' + strftime('%Y%m%d-%H%M%S') + '.jpg'
            # Camera warm-up time
            sleep(2)
            # tells the camera where to store the file and the file name
            camera.capture(serverFileName)
            i+=1

def runCamera():
    #make the Picamera a usable object
    camera = PiCamera()
    print("Camera is starting and will record the next ten seconds")
    camera.start_preview()
    #the path can be set inside of the () of recording
    camera.start_recording('/home/pi/Desktop/videoTestFile.h264')
    sleep(9)
    camera.stop_recording()
    print("Camera is shutting down")
    camera.stop_preview()