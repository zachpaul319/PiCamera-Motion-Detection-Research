import picamera
import picamera.array
import numpy as np

motionList = []
class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 40, then say we've detected motion and append motionList
        if (a > 40).sum() > 10:
            motionList.append((a > 40).sum())
            print('Motion detected!')

with picamera.PiCamera() as camera:
    camera.rotation = 180
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.start_recording(
        'motion.h264', format='h264',
        motion_output = MyMotionDetector(camera)
        )
    camera.wait_recording(7)
    camera.stop_recording()
    print(motionList)


