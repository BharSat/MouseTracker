import cv2


class Tracker:
    contours = None
    old = None

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
        cv2.drawContours(output, self.contours, -1, (127, 127, 127), 2)
        for cnt in self.contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(output, center, radius, (255, 255, 255), 2)

        return output

    def track(self):
        print(self.file_path)
        # Load video file
        cap = cv2.VideoCapture(self.file_path)

        # Get frame rate
        fpms = cap.get(cv2.CAP_PROP_FPS) / 1000
        while cap.isOpened():
            a = self.next_frame(cap, int(1 // fpms))
            if a is None:
                break
            elif ord("q") == a & 0xFF:
                break
        self.next_frame(cap=cap)
        cap.release()
        cv2.destroyAllWindows()

    def next_frame(self, cap, t=0):

        old = None
        ret, frame = cap.read()

        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))

        if old is not None:
            nframe = cv2.absdiff(frame, old)
        else:
            nframe = frame
        old = frame

        cv2.imshow('Frame', self.generate_contours(nframe, frame))

        return cv2.waitKey(t)
