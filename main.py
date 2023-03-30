import contour

if __name__ == "__main__":
    tracker = contour.Tracker('vid.mp4')
    tracker.track()