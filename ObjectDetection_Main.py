import cv2
import  numpy as np
from  gui_buttons import Buttons

#intilize buton
button =Buttons()
button.add_button("person",20,20)
button.add_button("cell phone" ,20,100)
button.add_button("keyborad",20,180)
button.add_button("remote",20,260)
button.add_button("scissors",20,340)
#opencv dnn
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights","dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320),scale=1/255)

#load class list
class_list =[]

with open("dnn_model/classes.txt","r") as file_object:
    for class_name in file_object.readlines():
        #print(class_name)
        class_name = class_name.strip()
        class_list.append(class_name)
print("object list ")
print(class_list)

#intlize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT ,1280)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)
#button_person = 0
#CRATE WINDOW

def click_button(event ,x,y ,flags ,params):
    global  button_person
    if event ==cv2.EVENT_LBUTTONDOWN:
        #print(x,y)
        button.button_click(x,y)
        # polygon=np.array([[(20,20),(220,20),(220,70),(20,70)]])
        #
        # is_inside =cv2.pointPolygonTest(polygon,(x,y),False)
        # if is_inside >0:
        #     #print("we are cliking inside the buton")
        #     if button_person is False :
        #         button_person = True
        #     else:
        #         button_person=False
        #     print("now button is : " ,button_person)


cv2.namedWindow("frame")
cv2.setMouseCallback("frame",click_button)



while True:
    #get frame
    ret , frame = cap.read()

#active buton list
    active_butons = button.active_buttons_list()
    print("active butons " ,active_butons)

    #object detection

    (class_id,scores,bboxes)= model.detect(frame ,confThreshold=0.3, nmsThreshold=.4)
    for class_id,scores,bboxes in zip(class_id,scores,bboxes ):
         (x,y,w,h ) = bboxes
        #print(x,y,w, h)
         class_name = class_list[class_id]
         #print(class_name)
         #if class_name =="person" and button_person is True:
         if class_name in active_butons:
            cv2.putText(frame,class_name,(x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(200,0,50),2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,50),3)

    # print("class id : ", class_id)
    # print("scores : ",scores)
    # print("bboxes : " ,bboxes)

    #crate button

    #cv2.rectangle(frame,(20,20),(220,70),(0,0,200),-1)

    # polygon=np.array([[(20,20),(220,20),(220,70),(20,70)]])
    # cv2.fillPoly(frame,polygon,(0,0,255))
    # cv2.putText(frame,"Person",(30,60),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)

#display button

    button.display_buttons(frame)
    cv2.imshow("frame" , frame)

    key = cv2.waitKey(1)

    if key ==27:
        break
cap.release()
cv2.destroyAllWindows()
