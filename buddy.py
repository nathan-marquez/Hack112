# Analytics Collector

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def startCam():
    import cv2
    from gaze_tracking import GazeTracking
    import time

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    startTime = time.time()
    totalFrames = 0
    framesDistracted = 0
    framesFocused = 0

    while True:
        _, frame = webcam.read()
        totalFrames += 1
        gaze.refresh(frame)
        frame = gaze.annotated_frame()

        if gaze.is_blinking():
            framesDistracted += 1
        elif gaze.is_right():
            framesDistracted += 1
        elif gaze.is_left():
            framesDistracted += 1
        elif gaze.is_center():
            framesFocused += 1
        else:
            framesDistracted += 1

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()

    totalTime = truncate(time.time() - startTime, 2)
    percentFocused = truncate((framesFocused / totalFrames) * 100, 2) 
    percentDistracted = truncate((framesDistracted / totalFrames) * 100, 2)

    return totalTime, percentFocused, percentDistracted
