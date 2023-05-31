1.Importing Libraries
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape, y_train.shape)
2.Reshaping the dataset and converting Numpy Array into Binary Values
import tensorflow
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)
num_classes=10
# “convert class vectors to binary class matrices”
y_train = tensorflow.keras.utils.to_categorcical(y_train, num_classes)
y_test = tensorflow.keras.utils.to_categorical(y_test, num_classes)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
3.Applying Convolutional Neural Network
import tensorflow as tf
from tensorflow import keras
tf.keras.optimizers.Adam()
batch_size = 128
num_classes = 10
epochs = 10
model = Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
4.Going for Accuracy check
from keras.callbacks import EarlyStopping,ModelCheckpoint
es=EarlyStopping(monitor='val_acc',min_delta=0.01,patience=4,verbose=1)
mc=ModelCheckpoint("./bestmodel.h5",monitor="val_acc",verbose=1,save_best_only=True)
cb=[es,mc]
his=model.fit(x_train,y_train,epochs=1,validation_split=0.3)
Output: 1313/1313 [==============================] - 145s 109ms/step - loss: 0.1798 - accuracy: 0.9434 - val_loss: 0.0668 - val_accuracy: 0.9799
5.Loading the model into a variable
model_s=keras.models.load_model("mnist.h5")
6.Evaluating the Training model and knowing the Accuracy
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
Output: Test loss: 2.3118209838867188
Test accuracy: 0.10939999669790268
7.Pygame code
8.Importing the Pygame related modules
%reset -f # After executing the pygame module the kernel gets dead so to restart itself this the line
from tokenize import Number
from numpy import testing
from numpy.lib.type_check import imag
from tensorflow.python.keras.backend import constant
import pygame ,sys
from pygame import image
from pygame.locals import *
import numpy as np
#”pip install pyttsx3” # for converting text to speech should install pyttsx3 on command prompt
import pyttsx3
import numpy.testing as npt
from keras.models import load_model
import cv2
Output: pygame 2.1.2 (SDL 2.0.18, Python 3.9.7)
Hello from the pygame community. https://www.pygame.org/contribute.html
9.Declerations of the variables used in the pygame
WINDOWSIZEX=640
WINDOWSIZEY=480
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
IMAGESAVE=False
MODEL=load_model("mnist.h5")
LABELS = {0:"Zero",1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine"}
text_speech = pyttsx3.init()
voices=text_speech.getProperty("voices")
text_speech.setProperty("voice",voices[1].id)
10.Code on the digit recognition output on pygame
pygame.init()
FONT = pygame.font.SysFont('Comic Sans Ms', 20)
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
WHITE_INT = DISPLAYSURF.map_rgb(WHITE)
pygame.display.set_caption("Digit Board")
iswriting = False
number_xcord = []
number_ycord = []
image_cnt = 1
while True:
      for event in pygame.event.get():
if event.type == QUIT:
pygame.quit()
           		sys.exit()
           if event.type == MOUSEMOTION and iswriting:
                      xcord, ycord = event.pos 
                    pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)
                    number_xcord.append(xcord)
                   number_ycord.append(ycord)
            if event.type == MOUSEBUTTONDOWN:
                     iswriting = True
            if event.type == MOUSEBUTTONUP:
                   iswriting = False
                 number_xcord = sorted(number_xcord)
                 number_ycord = sorted(number_ycord)
     rect_min_x, rect_max_x = max(number_xcord[0]- BOUNDRYINC, 0 ), min(WINDOWSIZEX, number_xcord[-1]+BOUNDRYINC)
   rect_min_Y, rect_max_Y = max(number_ycord[0]- BOUNDRYINC, 0 ), min( number_ycord[-1]+BOUNDRYINC, WINDOWSIZEX)
          number_xcord = [] 
           number_ycord = [] 
          img_arr =np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_Y:rect_max_Y].T.astype(np.float32)
                     if IMAGESAVE:
cv2.imwrite("image.png")
               		 image_cnt +=1
               	if PREDICT:
                          	image = cv2.resize(img_arr, (28,28))
                        	image = np.pad(image, (10,10),'constant',constant_values=0)
                        	image = cv2.resize(image, (28,28))/255
                       	 label=str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                		text_speech.say(label)
                		text_speech.runAndWait()
                		textSurface = FONT.render(label, True, RED, WHITE)
                		textRecObj = textSurface.get_rect() 
                		textRecObj.left , textRecObj.bottom = rect_min_x, rect_max_Y
                
               		 DISPLAYSURF.blit(textSurface, textRecObj)
                
            	if event.type == KEYDOWN:
                		if event.unicode == "n":
                    			DISPLAYSURF.fill(BLACK)
                  
                  
        pygame.display.update()
