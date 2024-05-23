import cv2
import depthai as dai
import numpy as np

class Stereo_Camera:
    def __init__(self):
        self.pipeline = dai.Pipeline()
        self.crop_left = 0
        self.crop_right = 0
        self.crop_top = 0
        self.crop_bottom = 0
        self.mouseX = 0
        self.mouseY = 640
        self.sideBySide = False

        self.monoLeft = self.get_mono_camera(isLeft=True)
        self.monoRight = self.get_mono_camera(isLeft=False)
        self.stereo = self.get_stereo_pair(self.monoLeft, self.monoRight)
        
        self.disparityMultiplier = 255 / self.stereo.getMaxDisparity()

        self.setup_outputs()

    def get_mono_camera(self, isLeft):
        mono = self.pipeline.createMonoCamera()
        mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT if isLeft else dai.CameraBoardSocket.RIGHT)
        return mono

    def get_stereo_pair(self, monoLeft, monoRight):
        stereo = self.pipeline.createStereoDepth()
        stereo.setLeftRightCheck(True)
        monoLeft.out.link(stereo.left)
        monoRight.out.link(stereo.right)
        return stereo

    def setup_outputs(self):
        xoutDisp = self.pipeline.createXLinkOut()
        xoutDisp.setStreamName("disparity")
        self.stereo.disparity.link(xoutDisp.input)

        xoutRectifiedLeft = self.pipeline.createXLinkOut()
        xoutRectifiedLeft.setStreamName("rectifiedLeft")
        self.stereo.rectifiedLeft.link(xoutRectifiedLeft.input)

        xoutRectifiedRight = self.pipeline.createXLinkOut()
        xoutRectifiedRight.setStreamName("rectifiedRight")
        self.stereo.rectifiedRight.link(xoutRectifiedRight.input)

    def get_frame(self, queue):
        frame = queue.get()
        return frame.getCvFrame()
    
    
    def get_depth(self, frame):
        disparity = (frame * self.disparityMultiplier).astype(np.uint8)
        depth = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)
        return depth

    def crop_frame(self, frame):
        h, w = frame.shape[:2]
        return frame[self.crop_top:h-self.crop_bottom, self.crop_left:w-self.crop_right]

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouseX = x
            self.mouseY = y

    def process_frames(self):
        with dai.Device(self.pipeline) as device:
            disparityQueue = device.getOutputQueue(name="disparity", maxSize=1, blocking=False)
            rectifiedLeftQueue = device.getOutputQueue(name="rectifiedLeft", maxSize=1, blocking=False)
            rectifiedRightQueue = device.getOutputQueue(name="rectifiedRight", maxSize=1, blocking=False)

            cv2.namedWindow("Stereo Pair")
            cv2.setmouse_callback("Stereo Pair", self.mouse_callback)

            while True:
                disparity = self.get_frame(disparityQueue)
                disparity = self.crop_frame(disparity)
                disparity = (disparity * self.disparityMultiplier).astype(np.uint8)
                disparity = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)

                leftFrame = self.get_frame(rectifiedLeftQueue)
                rightFrame = self.get_frame(rectifiedRightQueue)
                leftFrame = self.crop_frame(leftFrame)
                rightFrame = self.crop_frame(rightFrame)

                if self.sideBySide:
                    imOut = np.hstack((leftFrame, rightFrame))
                else:
                    imOut = np.uint8(leftFrame/2 + rightFrame/2)

                imOut = cv2.cvtColor(imOut, cv2.COLOR_GRAY2RGB)
                imOut = cv2.line(imOut, (self.mouseX, self.mouseY), (1280, self.mouseY), (0, 0, 255), 2)
                imOut = cv2.circle(imOut, (self.mouseX, self.mouseY), 2, (255, 255, 128), 2)
                cv2.imshow("Stereo Pair", imOut)
                cv2.imshow("Disparity", disparity)

                key = cv2.waitKey(1)
                self.handle_keypress(key)

    def handle_keypress(self, key):
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(0)
        elif key == ord('t'):
            self.sideBySide = not self.sideBySide
        elif key == ord('w'):
            self.crop_top += 1
        elif key == ord('i'):
            self.crop_top = max(0, self.crop_top - 1)
        elif key == ord('a'):
            self.crop_left += 1
        elif key == ord('j'):
            self.crop_left = max(0, self.crop_left - 1)
        elif key == ord('l'):
            self.crop_right += 1
        elif key == ord('d'):
            self.crop_right = max(0, self.crop_right - 1)
        elif key == ord('s'):
            self.crop_bottom += 1
        elif key == ord('k'):
            self.crop_bottom = max(0, self.crop_bottom - 1)

if __name__ == '__main__':
    stereoCamera = Stereo_Camera()
    stereoCamera.process_frames()