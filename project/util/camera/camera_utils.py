import subprocess
import sys
import threading
import urllib2

import cv2
import numpy

from project.util.image_utils import ImageUtils

try:
    import picamera
    import picamera.array
except:
    print 'No PiCamera module installed'

from flask import current_app

width = 800
height = 800


class CaptureThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.camera = picamera.PiCamera()

        player_cmdline = ['cvlc', '-vv', r'stream:///dev/stdin', '--sout', r'#rtp{sdp=rtsp://:8554/output.h264}', ':demux=h264', '--h264-fps', '15', '--noaudio', '--no-sout-audio']


        #player_cmdline_array = str.split(player_cmdline)

        #print player_cmdline_array

        self.player = subprocess.Popen(player_cmdline, stdin=subprocess.PIPE)

    def run(self):
        camera = self.camera
        player = self.player

        camera.resolution = (width, height)
        camera.framerate = 15

        camera.start_recording(player.stdin, format='h264', inline_headers=True)

        try:
            while True:
                camera.wait_recording(100000)
        finally:
            camera.stop_recording()
            player.terminate()
            camera.close()

    def capture(self):
        with picamera.array.PiYUVArray(self.camera) as stream:
            self.camera.capture(stream, 'yuv')

            rgb = cv2.cvtColor(stream.rgb_array, cv2.COLOR_RGB2BGR)

            cv2.imwrite(ImageUtils().getOutputFilename("capture.jpg"), rgb)

            return stream.rgb_array

class CameraService:
    def capture_image(self):
        file = urllib2.urlopen(current_app.config.get('CAMERA_ENDPOINT'))

        image = numpy.asarray(bytearray(file.read()), dtype="uint8")

        raw_image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return raw_image
