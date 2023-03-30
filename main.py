import cv2

def generate_contours(image, nimage=None):
    if len(image.shape)>2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    if nimage is None:
        nimage = image

    # Apply threshold to convert grayscale image to binary image
    ret, thresh = cv2.threshold(gray, 20, 255, 0)

    # Find contours in binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Create copy of input image to overlay contours on
    output = nimage.copy()

    # Draw contours on output image
    cv2.drawContours(output, contours, -1, (255, 255, 255), 2)

    return output

def main():
    # Load video file
    cap = cv2.VideoCapture('vid.mp4')

    # Get frame rate
    fpms = cap.get(cv2.CAP_PROP_FPS)/1000
    
    old = None

    # Loop through frames
    while True:
        # Read frame
        ret, frame = cap.read()

        # If there are no more frames, break out of loop
        if not ret:
            break
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
        
        if old is not None:
            nframe = cv2.absdiff(frame, old)
        else:
            nframe = frame
        old = frame

        # Display frame
        cv2.imshow('Frame', generate_contours(nframe, frame))

        # Wait for 1 millisecond
        # If the 'q' key is pressed, break out of loop
        if cv2.waitKey(int(1//fpms)) & 0xFF == ord('q'):
            break

    # Release video file and close window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()