import numpy as np
import cv2
umbral_minimo = 100
umbral_maximo = 200

class detectorPlaga:
    """A simple example class"""
    frame = 0
    ##Se definen los kernel con el que se haran las operaciones de dilatacion y expansion de la mascara
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((7,7),np.uint8)
    def __init__(self, cap):
    	self.frame= cap
    	#self.mostrarVideo()
    	self.mostrarImagen(self.frame)

    def detectarBichos(self,imagen):
        contador=0
        copia=imagen.copy()
        mask=0
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        naranja_bajos = np.array([0,89,238])###Entrar a http://colorizer.org/ para hacer el calculo de colores
        naranja_altos = np.array([201,241,255])
        mascara_naranja = cv2.inRange(hsv, naranja_bajos, naranja_altos)
        ###Aqui se crea la mascara
        mask = cv2.add(mask, mascara_naranja)
        mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,self.kernel2)
        ##se crean los umbrales para definir rangos de color
        transformacion = cv2.erode(mask,self.kernel,iterations = 1)
        transformacion = cv2.morphologyEx(transformacion,cv2.MORPH_CLOSE,self.kernel2)
        transformacion = cv2.GaussianBlur(transformacion, (5, 5), 0)
        #transformacion = cv2.erode(mask,kernel,iterations = 1)
        transformacion2 = cv2.dilate(transformacion,self.kernel,iterations = 1)
        cv2.imshow('transformacion',transformacion2)
        ##Como queremos eliminar
        gaussiana = cv2.GaussianBlur(transformacion2, (3, 3), 0)
        canny = cv2.Canny(gaussiana, umbral_minimo, umbral_maximo)
        (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.imshow('frame',mask)
        cv2.imshow('Canny',canny)
        #print("He encontrado {} objetos".format(len(contornos)))
        cv2.drawContours(copia,contornos,-1,(0,0,255), 2)
        rects=[0,0,0,0]
        contador=0
        #rects=array[0,0,0,0]
        for c in contornos:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            if h >= 10:
                contador=contador+1
            # if height is enough
            # create rectangle for bounding
                rect = (x, y, w, h)
                rects.append(rect)
                cv2.rectangle(copia, (x, y), (x+w, y+h), (0, 255, 0), 2);
        font = cv2.FONT_HERSHEY_SIMPLEX
        if contador>1:
            pass
            cv2.putText(copia,'Hay Plaga!!!! 帮助!!!',(30,60), font, 1,(0,0,255),2,cv2.LINE_AA)
        else:
            cv2.putText(copia,'No hay Plaga',(30,60), font, 1,(0,255,0),2,cv2.LINE_AA)
        cv2.imshow("Contornos", copia)

    def detectarHongos(self,imagen):
        contador=0
        copia=imagen.copy()
        mask=0
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        naranja_bajos = np.array([32,36,61])###Entrar a http://colorizer.org/ para hacer el calculo de colores
        naranja_altos = np.array([185,130,130])
        mascara_naranja = cv2.inRange(hsv, naranja_bajos, naranja_altos)
        ###Aqui se crea la mascara
        mask = cv2.add(mask, mascara_naranja)
        cv2.imshow('frame',mask)
        mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,self.kernel2)
        ##se crean los umbrales para definir rangos de color
        transformacion = cv2.erode(mask,self.kernel,iterations = 1)
        transformacion = cv2.morphologyEx(transformacion,cv2.MORPH_CLOSE,self.kernel2)
        transformacion = cv2.GaussianBlur(transformacion, (5, 5), 0)
        #transformacion = cv2.erode(mask,kernel,iterations = 1)
        transformacion2 = cv2.dilate(transformacion,self.kernel,iterations = 1)
        cv2.imshow('transformacion',transformacion2)
        ##Como queremos eliminar
        gaussiana = cv2.GaussianBlur(transformacion2, (3, 3), 0)
        canny = cv2.Canny(gaussiana, umbral_minimo, umbral_maximo)
        (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.imshow('Canny',canny)
        #print("He encontrado {} objetos".format(len(contornos)))
        cv2.drawContours(copia,contornos,-1,(0,0,255), 2)
        rects=[0,0,0,0]
        contador=0
        #rects=array[0,0,0,0]
        for c in contornos:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            if h >= 10:
                contador=contador+1
            # if height is enough
            # create rectangle for bounding
                rect = (x, y, w, h)
                rects.append(rect)
                cv2.rectangle(copia, (x, y), (x+w, y+h), (0, 255, 0), 2);
        font = cv2.FONT_HERSHEY_SIMPLEX
        if contador>1:
            pass
            cv2.putText(copia,'Hay Hongos!!!!',(30,60), font, 1,(0,0,255),2,cv2.LINE_AA)
        else:
            cv2.putText(copia,'No hay Hongos!! ',(30,60), font, 1,(0,255,0),2,cv2.LINE_AA)
        cv2.imshow("Contornos", copia)
    	

    def mostrarImagen(self,image):
    	while(True):
    		# Capture frame-by-frame
    		# Our operations on the frame come here
    		# gray = cv2.cvtColor(frameX, cv2.COLOR_BGR2GRAY)
    		# Display the resulting frame
    		#frameX=self.detectarBichos(image)
            frameX=self.detectarHongos(image)
    		#cv2.imshow('GRIS',image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    	


    def mostrarVideo(self):
    	while(True):
    		# Capture frame-by-frame
    		ret, frameX = self.frame.read()
    		# Our operations on the frame come here
    		# gray = cv2.cvtColor(frameX, cv2.COLOR_BGR2GRAY)
    		# Display the resulting frame
    		cv2.imshow('frame',frameX)
    		if cv2.waitKey(1) & 0xFF == ord('q'):
    			break

#Aqui va el inicio del codigo
#cap = cv2.VideoCapture(0)
#cap = cv2.imread('plaga2.jpg')
cap = cv2.imread('plaga4.jpg')
plaga = detectorPlaga(cap)

