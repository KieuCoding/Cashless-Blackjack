import cv2          #the opencv library
import os

folder_name = "trash_pictures" # this folder will have the save trash photos
cap = cv2.VideoCapture(0) #connect to a cetain capture device port
img_counter = 0

while cap.isOpened():
    ret, frame = cap.read()
    #ret is a warning telling user if camera is in use by other software
    #frame = cap.read() is a command to capture a frame from the camera
    if not ret: 
        print("frame not grabbed")
        break 
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)  #set waitkey to letter k
    if k%256 == 27:     #if k is pressed stop capture device
        print("Escape capture")
        break
    elif k%256 == 32:   #if spacebar is pressed start image capture on device
        while True:
            img_name = os.path.join(folder_name, "opencv_frame_{}.png".format(img_counter))
            if not os.path.exists(img_name):
                cv2.imwrite(img_name, frame)  
                print("Screenshot taken and saved as:", img_name)
                img_counter += 1
                break
            else:
                img_counter += 1
        #cap.release()           #releases capture device from current occupied software
        #cap.destroyAllWindows() #closes all capture windows
        
