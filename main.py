import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from figure import *
from tkinter import *
from tkinter import ttk
import time
import serial
import threading

ApplicationGL = False

class PortSettings:
    Name = "COM3"
    Speed = 115200
    Timeout = 2

class IMU:
    Roll = 0
    Pitch = 0
    Yaw = 0

myport = PortSettings()
myimu  = IMU()

def RunAppliction():
    global ApplicationGL
    myport.Name = Port_entry.get()
    myport.Speed = Baud_entry.get()
    ApplicationGL = True
    ConfWindw.destroy()

ConfWindw = Tk()
ConfWindw.title("Configure Serial Port")
ConfWindw.configure(bg = "#2E2D40") 
ConfWindw.geometry('300x150')
ConfWindw.resizable(width=False, height=False)
positionRight = int(ConfWindw.winfo_screenwidth()/2 - 300/2)
positionDown = int(ConfWindw.winfo_screenheight()/2 - 150/2)
ConfWindw.geometry("+{}+{}".format(positionRight, positionDown))

Port_label = Label(text = "Port:", font =("",12), justify= "right", bg = "#2E2D40", fg = "#FFFFFF")
Port_label.place(x = 50, y =30, anchor = "center")
Port_entry = Entry(width = 20, bg = "#37364D", fg = "#FFFFFF", justify = "center")
Port_entry.insert(INSERT,myport.Name)
Port_entry.place(x = 180, y = 30,anchor = "center")

Baud_label = Label(text = "Speed:", font =("",12), justify= "right", bg = "#2E2D40", fg = "#FFFFFF")
Baud_label.place(x = 50, y =80, anchor = "center")
Baud_entry = Entry(width = 20,bg = "#37364D", fg = "#FFFFFF", justify = "center")
Baud_entry.insert(INSERT,str(myport.Speed))
Baud_entry.place(x = 180, y = 80, anchor = "center")

ok_button = Button(text = "Ok",width = 8,command = RunAppliction,bg="#135EF2",fg ="#FFFFFF")
ok_button.place(x = 150, y = 120, anchor="center")

def InitPygame():
    global display
    pygame.init()
    display = (1280,960)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('IMU visualizer   (Press Esc to exit)')


def InitGL():
    glClearColor((1.0/255*46),(1.0/255*45),(1.0/255*64),1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    gluPerspective(100, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)


def DrawText(textString):     
    font = pygame.font.SysFont ("Courier New",25, True)
    textSurface = font.render(textString, True, (255,255,0), (46,45,64,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)         
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)    

def DrawBoard():
    
    glBegin(GL_QUADS)
    x = 0
    
    for surface in surfaces:
        
        for vertex in surface:  
            glColor3fv((colors[x]))          
            glVertex3fv(vertices[vertex])
        x += 1
    glEnd()

def DrawGL():

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() 
    gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)   

    glRotatef(round(myimu.Pitch,1), 0, 0, 1)
    glRotatef(round(myimu.Roll,1), -1, 0, 0)
    glRotatef(round(myimu.Yaw,1), 0, 1, 0)

    DrawText(" Roll: {}°     Pitch: {}°      Yaw: {}°".format(round(myimu.Roll,1),round(myimu.Pitch,1),round(myimu.Yaw,1)))
    DrawBoard()
    pygame.display.flip()

def SerialConnection ():
    global serial_object
    serial_object = serial.Serial( myport.Name, baudrate= myport.Speed, timeout = myport.Timeout)

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    
    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

def ReadData():

    rl = ReadLine(serial_object)

    while True:
        
        data = rl.readline().decode('unicode_escape')

        # Received dataframe example:
        # Orientation: 347.66, 1.26, 1.38 (YAW, PITCH, ROLL)
        # Quaternion: 0.1076, -0.0097, 0.0132, 0.9941

        if data[0] == 'O': #Orientation
            data = data[13:].rstrip('\n')
            orientationData = data.split(', ')
            yaw = orientationData[0]
            pitch = orientationData[1]
            roll = orientationData[2]

            print(yaw, pitch, roll)

            #Convert string values to float
            myimu.Roll = float(roll)
            myimu.Pitch = float(pitch)
            myimu.Yaw = float(yaw)


def main():
    ConfWindw.mainloop()
    if ApplicationGL == True:
        InitPygame()
        InitGL()
 
        try:
            SerialConnection()
            myThread1 = threading.Thread(target = ReadData)
            myThread1.daemon = True
            myThread1.start() 
            while True:
                event = pygame.event.poll()
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    break 

                DrawGL()
                pygame.time.wait(10)

        except:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            DrawText("Sorry, something is wrong :c")
            pygame.display.flip()
            time.sleep(5)

                 


if __name__ == '__main__': main()