import cv2
import time


class Tracker:
    contours = []
    paths = []
    old = None
    tracking = False
    cap = None

    def __init__(self, file_path=""):
        self.file_path = file_path

    def generate_contours(self, image, nimage=None):
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        if nimage is None:
            nimage = image

        # Apply threshold to convert grayscale image to binary image
        ret, thresh = cv2.threshold(gray, 20, 255, 0)

        # Find contours in binary image
        self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Create copy of input image to overlay contours on
        output = nimage.copy()

        # Draw contours on output image
        cv2.drawContours(output, self.contours, -1, (0, 0, 0), 2)
        for cnt in self.contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(output, center, radius, (255, 255, 255), 2)

        return output

    def track(self, show=True, start_call=lambda fpms: None, loop_call=lambda frame: None, end_call=lambda: None,
              dfpms=None):

        print(self.file_path)
        # Load video file
        self.cap = cap = cv2.VideoCapture(self.file_path)

        # Get frame rate
        fpms = cap.get(cv2.CAP_PROP_FPS) / 1000
        if not dfpms: dfpms = (1 // fpms) / 1000
        start_call(fpms)
        cont = True
        while cap.isOpened():
            if not cont:
                cont = loop_call(a)
                time.sleep((1 // dfpms) / 1000)
                continue
            a = self.next_frame(cap, show, int(1 // fpms))
            if show:
                if a is None:
                    break
                elif ord("q") == a & 0xFF:
                    break
                elif ord("t") == a & 0xFF:
                    self.tracking = not self.tracking
            else:
                cont = loop_call(a)
                time.sleep((1 // dfpms) / 1000)
        cap.release()
        if show:
            cv2.destroyAllWindows()
        end_call()

    def next_frame(self, show=True, t=0):
        ret, frame = self.cap.read()

        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))

        if self.tracking: frame = self.generate_contours(frame)

        if show:
            cv2.imshow('Frame', frame)

            return cv2.waitKey(t)
        return frame
