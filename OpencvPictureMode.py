import cv2
import os

# Create a directory to store the captured images if it doesn't exist
if not os.path.exists('captured_images'):
    os.makedirs('captured_images')

# Create a directory to store the discarded images if it doesn't exist
if not os.path.exists('trash_pictures'):
    os.makedirs('trash_pictures')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the counter for unique filenames
count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Check if the spacebar is pressed
    if cv2.waitKey(1) & 0xFF == ord(' '):
        # Save the image with a unique filename
        img_name = f'captured_images/image_{count}.png'
        cv2.imwrite(img_name, frame)
        print(f'Image saved as {img_name}')

        # Increment the counter for the next image
        count += 1

    # Check if the 'd' key is pressed to discard the image
    elif cv2.waitKey(1) & 0xFF == ord('d'):
        # Save the image to the trash folder with a unique filename
        img_name = f'trash_pictures/image_{count}.png'
        cv2.imwrite(img_name, frame)
        print(f'Image discarded and saved as {img_name}')

        # Increment the counter for the next image
        count += 1

    # Check if the 'q' key is pressed to exit the loop
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()