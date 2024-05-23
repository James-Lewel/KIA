import cv2
import depthai as dai
import numpy as np

def getFrame(queue):
    frame = queue.get()
    return frame.getCvFrame()

def getMonoCamera(pipeline, isLeft):
    mono = pipeline.createMonoCamera()
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    
    if isLeft:
        # Get left camera
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
    else :
        # Get right camera
        mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    return mono

if __name__ == '__main__':
    pipeline = dai.Pipeline()
    
    monoLeft = getMonoCamera(pipeline, isLeft = True)
    monoRight = getMonoCamera(pipeline, isLeft = False)

    xoutLeft = pipeline.createXLinkOut()
    xoutLeft.setStreamName("left")

    xoutRight = pipeline.createXLinkOut()
    xoutRight.setStreamName("right")
 
    monoLeft.out.link(xoutLeft.input)
    monoRight.out.link(xoutRight.input)
    
    with dai.Device(pipeline) as device:
        leftQueue = device.getOutputQueue(name="left", maxSize=1)
        rightQueue = device.getOutputQueue(name="right", maxSize=1)

        cv2.namedWindow("Stereo Pair")
        sideBySide = True
        
        while True:
            leftFrame = getFrame(leftQueue)
            rightFrame = getFrame(rightQueue)

            if sideBySide:
                # Show side by side view
                imOut = np.hstack((leftFrame, rightFrame))
            else : 
                # Show overlapping frames
                imOut = np.uint8(leftFrame/2 + rightFrame/2)

            cv2.imshow("Stereo Pair", imOut)
            
            # Check for keyboard input
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('t'):
                sideBySide = not sideBySide
            

