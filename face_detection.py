import cv2

detect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
imp_img = cv2.VideoCapture(0)
#address = "http://192.168.66.165:8080/video"
#imp_img.open(address)


while True:
    res, img = imp_img.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = detect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h),(255, 255, 0),2)




    cv2.imshow("Face Detection", img)

    k = cv2.waitKey(10) & 0xff
    if k==27:
        break

imp_img.release()
cv2.destroyAllWindows()