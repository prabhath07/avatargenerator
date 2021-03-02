import cv2
import os
from PIL import Image
import py_avataaars as pa
import matplotlib.pyplot as plt
import numpy as np
from random import randrange
import math


gender=""
while(1):
    gender = input("please input your gender m if male and f if female")
    if(gender=="male" or gender=="m" or gender=="f" or gender=="female"):
        break
    else :
        print("please give your gender")
print(gender)


list_skin_color = ['PALE','LIGHT','BROWN','DARK_BROWN']
list_hair_color = ['AUBURN','BLACK','BROWN', 'BROWN_DARK']

# creating avatar
if(gender=="male"or gender=="m"):
    list_top_type = ['SHORT_HAIR_DREADS_01',
                 'SHORT_HAIR_DREADS_02','SHORT_HAIR_FRIZZLE',
                 'SHORT_HAIR_SHAGGY_MULLET','SHORT_HAIR_SHORT_CURLY',
                 'SHORT_HAIR_SHORT_FLAT','SHORT_HAIR_SHORT_ROUND',
                 'SHORT_HAIR_SHORT_WAVED','SHORT_HAIR_SIDES',
                 'SHORT_HAIR_THE_CAESAR','SHORT_HAIR_THE_CAESAR_SIDE_PART']
else:
    list_top_type = ['LONG_HAIR_BIG_HAIR','LONG_HAIR_BOB',
                 'LONG_HAIR_BUN','LONG_HAIR_CURLY','LONG_HAIR_CURVY',
                 'LONG_HAIR_DREADS','LONG_HAIR_FRIDA','LONG_HAIR_FRO',
                 'LONG_HAIR_FRO_BAND','LONG_HAIR_NOT_TOO_LONG',
                 'LONG_HAIR_SHAVED_SIDES','LONG_HAIR_MIA_WALLACE',
                 'LONG_HAIR_STRAIGHT','LONG_HAIR_STRAIGHT2',
                 'LONG_HAIR_STRAIGHT_STRAND']
    
clothe = ['BLAZER_SHIRT','BLAZER_SWEATER','COLLAR_SWEATER','GRAPHIC_SHIRT','HOODIE','OVERALL','SHIRT_CREW_NECK','SHIRT_SCOOP_NECK','SHIRT_V_NECK']
clotheg = ['BAT','CUMBIA','DEER','DIAMOND','HOLA','PIZZA','RESIST','SELENA','BEAR','SKULL_OUTLINE','SKULL']

index_skin_color = randrange(0, len(list_skin_color) )
index_hair_color = randrange(0, len(list_hair_color) )
index_clothe = randrange(0, len(clothe) )
index_clotheg = randrange(0, len(clotheg) )
index_top_type = randrange(0, len(list_top_type) )



acceptance=""
while(1):
    acceptance = input("Do you want to access your camera y if yes and n if no")
    if(acceptance=="yes" or acceptance=="y" or acceptance=="n" or acceptance=="no"):
        break
    else :
        print("please give your acceptance")
print(acceptance)




if(acceptance=="y" or acceptance=="yes"):
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()

    # detecting fac and facial properties
    def detectface(frame):
        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
        img=frame.copy()
        cordinates=[]

        for (x, y, w, h) in faces:
            cordinates.append((x,y-50))
            cordinates.append((x+w,y-50))
            cordinates.append((x,y+h+10))
            cordinates.append((x+w,y+h+10))
            img=cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 0,0), 3)   
        return img,cordinates,x,y,w,h
    img,crd,x,y,w,h= detectface(frame)

    hairimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    h2 = img[y-50:y+h+10,x:x+w]
    he=int(0.3*(h+60))
    he2=int(0.15*(h+60))
    width=int(0.15*w)
    hair=h2[0:he,:]
    body=h2[he:(h+60)-he2,width:w-width]

    def avgcolour(img):
        b,g,r=(0,0,0)
        b=int(np.mean(img[:,:,0]))
        g=int(np.mean(img[:,:,1]))
        r=int(np.mean(img[:,:,2]))
        return math.sqrt( r*r+g*g+b*b)

    black=math.sqrt(44*44+34*34+43*43)
    darkbrown=math.sqrt(89*89+47*47+43*43)
    brown = math.sqrt(161*161+102*102+94*94)
    light=math.sqrt(209*209+163*163+164)

    #c58c85	rgb(197, 140, 133)
    #ecbcb4	rgb(236, 188, 180)
    #d1a3a4	rgb(209, 163, 164)
    #a1665e	rgb(161, 102, 94)
    #503335	rgb(80, 51, 53)
    #592f2a	rgb(89, 47, 42)


    haircolour=avgcolour(hair)
    bodycolour=avgcolour(body)
    def hair(c):
        if(c<=black):
            colour='BLACK'
        elif(c<=darkbrown):
            colour='BROWN_DARK'
        elif(c<=brown):
            colour='BROWN'
        else:
            colour='AUBURN'
        return colour
    hc=hair(haircolour)

    def body(c):
        if(c<=darkbrown):
            colour='DARK_BROWN'
        elif(c<=brown):
            colour='BROWN'
        elif(c<=light):
            colour='LIGHT'
        else:
            colour='PALE'
        return colour

    bc=body(bodycolour)
    
else:
    bc=list_skin_color[index_skin_color]
    hc=list_hair_color[index_hair_color]




#creating avatar
    

avatar = pa.PyAvataaar(
    style=pa.AvatarStyle.CIRCLE,
    
    skin_color=eval('pa.SkinColor.%s' % bc),
    hair_color=eval('pa.HairColor.%s' % hc),
#     skin_color=eval('pa.SkinColor.%s' % skincolourfinal),
#     hair_color=eval('pa.HairColor.%s' % haicolourfinal),
    facial_hair_type=pa.FacialHairType.DEFAULT,
    facial_hair_color=pa.HairColor.BLACK,
    top_type=eval('pa.TopType.SHORT_HAIR_SHORT_FLAT.%s' % list_top_type[index_top_type]),
    hat_color=pa.Color.BLACK,
    mouth_type=pa.MouthType.SMILE,
    eye_type=pa.EyesType.DEFAULT,
    eyebrow_type=pa.EyebrowType.DEFAULT,
    nose_type=pa.NoseType.DEFAULT,
    accessories_type=pa.AccessoriesType.DEFAULT,
    clothe_type=eval('pa.ClotheType.%s' % clothe[index_clothe]),
    clothe_graphic_type=eval('pa.ClotheGraphicType.%s' % clotheg[index_clotheg])
)


rendered_avatar = avatar.render_png_file('avatar2.png')
imglast = cv2.imread('avatar2.png')
while (1):
        cv2.imshow('YOUR AVATAR',imglast)
        if cv2.waitKey(10000)& 0XFF==27 :
            break
cv2.destroyAllWindows()

