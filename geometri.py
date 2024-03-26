# WS128x128 1.44" GFX 
# Tony Goodhew 23rd May 2022 for thepihut.com - TESTED
# Demonstrates 65K colours, text/fonts and graphics
from machine import Pin,SPI,PWM
import machine
import framebuf
import utime
import math
import random
import gc

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10    
CS = 9

class lcd_1inch44(framebuf.FrameBuffer): # WS 128 x 128 Display
    def __init__(self):
        self.width = 128
        self.height = 128
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
    def write_cmd(self, cmd):    
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36);
        self.write_data(0x70); 
        
        self.write_cmd(0x3A);
        self.write_data(0x05);

         #ST7735R Frame Rate
        self.write_cmd(0xB1);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB2);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB3);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB4); #Column inversion
        self.write_data(0x07);

        #ST7735R Power Sequence
        self.write_cmd(0xC0);
        self.write_data(0xA2);
        self.write_data(0x02);
        self.write_data(0x84);
        self.write_cmd(0xC1);
        self.write_data(0xC5);

        self.write_cmd(0xC2);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0xC3);
        self.write_data(0x8A);
        self.write_data(0x2A);
        self.write_cmd(0xC4);
        self.write_data(0x8A);
        self.write_data(0xEE);

        self.write_cmd(0xC5); #VCOM
        self.write_data(0x0E);

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0);
        self.write_data(0x0f);
        self.write_data(0x1a);
        self.write_data(0x0f);
        self.write_data(0x18);
        self.write_data(0x2f);
        self.write_data(0x28);
        self.write_data(0x20);
        self.write_data(0x22);
        self.write_data(0x1f);
        self.write_data(0x1b);
        self.write_data(0x23);
        self.write_data(0x37);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x02);
        self.write_data(0x10);

        self.write_cmd(0xe1);
        self.write_data(0x0f);
        self.write_data(0x1b);
        self.write_data(0x0f);
        self.write_data(0x17);
        self.write_data(0x33);
        self.write_data(0x2c);
        self.write_data(0x29);
        self.write_data(0x2e);
        self.write_data(0x30);
        self.write_data(0x30);
        self.write_data(0x39);
        self.write_data(0x3f);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x03);
        self.write_data(0x10);

        self.write_cmd(0xF0); #Enable test command
        self.write_data(0x01);

        self.write_cmd(0xF6); #Disable ram power save mode
        self.write_data(0x00);
            #sleep out
        self.write_cmd(0x11);
        #Turn on the lcd display
        self.write_cmd(0x29);

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0x80)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x82)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
# ====================== End of screen driver ===============
pwm = PWM(Pin(BL))
pwm.freq(1000)
#pwm.duty_u16(32768)#max 65535 ========= HALF BRIGHTNESS
pwm.duty_u16(65535)#max 65535  ==========   FULL BRIGHTNESS
lcd = lcd_1inch44() # Start screen
width = 128   # Display size in pixels
height = 128
# Set up buttons
key0 = Pin(15,Pin.IN,Pin.PULL_UP) # Buttons for 1.44 display
key1 = Pin(17,Pin.IN,Pin.PULL_UP)
key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)

def colour(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((R&0b11111000)>>3)<<8) + (B&0b11111000)+((G&0b11100000)>>5)

def clear(c):
    lcd.fill(c)
    
clear(colour(0,0,0))
lcd.show()
# ==== Board now setup ========== 
# ========== Start of Triangles code =============
# Modified from https://github.com/SpiderMaf/PiPicoDsply/blob/main/filled-triangles.py
# To work on WaveShare Pi Pico displays
# ========== Version 2 FIXED ! 23 May 2022 ==========
class Point:
    def __init__(self,x,y):
        self.X=x
        self.Y=y
    def __str__(self):
        return "Point(%s,%s)"%(self.X,self.Y)
        
class Triangle:
    def __init__(self,p1,p2,p3):
        self.P1=p1
        self.P2=p2
        self.P3=p3

    def __str__(self):
        return "Triangle(%s,%s,%s)"%(self.P1,self.P2,self.P3)
    
    def draw(self):
        print("I should draw now")
        self.fillTri()
    # Filled triangle routines ported from http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html      
    def sortVerticesAscendingByY(self):    
        if self.P1.Y > self.P2.Y:
            vTmp = self.P1
            self.P1 = self.P2
            self.P2 = vTmp
        
        if self.P1.Y > self.P3.Y:
            vTmp = self.P1
            self.P1 = self.P3
            self.P3 = vTmp

        if self.P2.Y > self.P3.Y:
            vTmp = self.P2
            self.P2 = self.P3
            self.P3 = vTmp
        
    def fillTri(self):
        self.sortVerticesAscendingByY()
        if self.P2.Y == self.P3.Y:
            fillBottomFlatTriangle(self.P1, self.P2, self.P3)
        else:
            if self.P1.Y == self.P2.Y:
                fillTopFlatTriangle(self.P1, self.P2, self.P3)
            else:
                newx = int(self.P1.X + (float(self.P2.Y - self.P1.Y) / float(self.P3.Y - self.P1.Y)) * (self.P3.X - self.P1.X))
                newy = self.P2.Y                
                pTmp = Point( newx,newy )
#                print(pTmp)
                fillBottomFlatTriangle(self.P1, self.P2, pTmp)
                fillTopFlatTriangle(self.P2, pTmp, self.P3)

def fillBottomFlatTriangle(p1,p2,p3):
    
#    print("BF",p1,p2,p3)
    if p2.Y > p3.Y:
        ty = p3.Y
        p3.Y = p2.Y
        p2.Y = ty
        tx = p3.X
        p3.X = p2.X
        p2.X = tx
        print(p1,p2,p3)
    
    slope1 = float(p2.X - p1.X) / float (p2.Y - p1.Y)
    slope2 = float(p3.X - p1.X) / float (p3.Y - p1.Y)

    x1 = p1.X
    x2 = p1.X + 0.5
#    print("B",p1.Y,p2.Y)
    for scanlineY in range(p1.Y,p2.Y):
#        print(scanlineY)
#        lcd.pixel_span(int(x1), scanlineY, int(x2)-int(x1))   # Switch pixel_span() to hline() / Pimoroni to WS
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1),c)        
        lcd.hline(int(x2),scanlineY, -(int(x2)-int(x1)),c)
#        lcd.show()          #                  Here and below        
#        utime.sleep(0.1)    #     <===== Uncomment to see how graphic elements are drawn
        x1 += slope1
        x2 += slope2
#    lcd.show()              #                  lcd.show() and utime.sleep(0.1)
def fillTopFlatTriangle(p1,p2,p3):
#    print("TF",p1,p2,p3)
    slope1 = float(p3.X - p1.X) / float(p3.Y - p1.Y)
    slope2 = float(p3.X - p2.X) / float(p3.Y - p2.Y)

    x1 = p3.X
    x2 = p3.X + 0.5
#    print("T",p3.Y,p1.Y-1)
    for scanlineY in range (p3.Y,p1.Y-1,-1):
#        print(scanlineY)
#        lcd.pixel_span(int(x1), scanlineY, int(x2)-int(x1))  # Switch pixel_span() to hline() / Pimoroni to WS
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1)+1,c)        
        lcd.hline(int(x2),scanlineY, -(int(x2)-int(x1)-1),c)
#        lcd.show()
#        utime.sleep(0.1)
        x1 -= slope1
        x2 -= slope2
#    lcd.show()            
# ============== End of Triangles Code ===============

# =========== New GFX Routines ============
def triangle(x1,y1,x2,y2,x3,y3,c): # Draw outline triangle
    lcd.line(x1,y1,x2,y2,c)
    lcd.line(x2,y2,x3,y3,c)
    lcd.line(x3,y3,x1,y1,c)
    
def tri_filled(x1,y1,x2,y2,x3,y3,c): # Draw filled triangle
 
    t=Triangle(Point(x1,y1),Point(x2,y2),Point(x3,y3)) # Define corners
    t.fillTri() # Call main code block  

def circle(x,y,r,c):
    lcd.hline(x-r,y,r*2,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Pythagoras!
        lcd.hline(x-a,y+i,a*2,c) # Lower half
        lcd.hline(x-a,y-i,a*2,c) # Upper half

def ring(x,y,r,c):
    lcd.pixel(x-r,y,c)
    lcd.pixel(x+r,y,c)
    lcd.pixel(x,y-r,c)
    lcd.pixel(x,y+r,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i))
        lcd.pixel(x-a,y-i,c)
        lcd.pixel(x+a,y-i,c)
        lcd.pixel(x-a,y+i,c)
        lcd.pixel(x+a,y+i,c)
        lcd.pixel(x-i,y-a,c)
        lcd.pixel(x+i,y-a,c)
        lcd.pixel(x-i,y+a,c)
        lcd.pixel(x+i,y+a,c)

# =================== Main =======================     
# Title screen
clear(0)
lcd.show()
lcd.text("Graphics",5,10,colour(200,0,0))
cc = colour(200,200,0)
lcd.text("Triangles",24,30,cc) 
lcd.text("Circles",24,40,cc)     
lcd.text("Rings",24,50,cc)
lcd.text("Rectangles",24,60,cc)
lcd.text("and Lines",24,70,cc)
for y in range(5):
    lcd.text("*",13,y*10 + 30,colour(0,0,255))
lcd.show()
utime.sleep(2)
lcd.fill(0)

# Built into framebuf library with the basic font
lcd.rect(0,80,128,47,colour(255,0,0))
lcd.show()
utime.sleep(0.6)
for x in range(4,125,5):
    lcd.vline(x,82,40,colour(0,0,255))
for y in range(82,125,5):
    lcd.hline(4,y,121,colour(0,0,255))
lcd.fill_rect(20,88,89,29,colour(50,50,50))
lcd.text("Graphics",32,98,colour(0,255,255))
lcd.show()
utime.sleep(1)
# Triangle
x1 = 2
y1=5
x2=15
y2=45
x3=120
y3=75
c = colour(90,90,90)
triangle(x1,y1,x2,y2,x3,y3,c)
lcd.show()
utime.sleep(1)
tri_filled(x1,y1,x2,y2,x3,y3,c)
lcd.show()
utime.sleep(1)
triangle(10,30,50,2,70,70,colour(255,255,255))
lcd.show()
utime.sleep(1)

# Circle & Ring
c = colour(0,0,255)
ring(90,30,25,c)
lcd.show()
utime.sleep(1)
circle(90,30,25,c)
lcd.show()
utime.sleep(1)
c = colour(0,255,0)
ring(90,30,25,c)
lcd.show()
utime.sleep(1)
c=colour(255,0,0)
ring(90,30,30,c)
lcd.show()
utime.sleep(1)
c = colour(255,0,0)
circle(90,30,15,c)
lcd.text(chr(227),85,25,colour(225,0,0)) 
lcd.show()

# Thread art
for i in range(0,61,4):
    lcd.line(0,10+i,i,70,colour(255,255,0))
    lcd.show()
utime.sleep(1)

clear(0)
lcd.text("Pixel",10,10,colour(200,200,200))
lcd.text("Plotting",10,20,colour(200,200,200))
lcd.show()
utime.sleep(1)

# Graphs - Sine and Cosine
clear(0)
lcd.show()
c = colour(80,80,80)
factor = 361 / width
lcd.hline(0,40,160,c)    
lcd.show()
c = colour(255,0,0)
for x in range(0,width):
    y = int ((math.sin(math.radians(x * factor)))* -30) + 40
    lcd.pixel(x,y,c)
    lcd.show()
lcd.text("Sine", 5, 65, colour(255,0,0))
lcd.show()
utime.sleep(1)

lcd.show()
c = colour(80,80,80)
lcd.hline(0,40,160,c)    
lcd.show()
c = colour(0,255,0)
for x in range(0,width):
    y = int((math.cos(math.radians(x * factor)))* -30) + 40
    lcd.pixel(x,y,c)
lcd.text("Cosine",60,10,colour(0,255,0))
lcd.show()
utime.sleep(3)

clear(0)
lcd.text("Scrolling",2,2,colour(255,255,0))
lcd.show()
utime.sleep(0.8)
for i in range(15):
    lcd.scroll(2 * i, i)
    lcd.show()
    utime.sleep(0.3)

# 30 random triangles
c = colour(200,0,0)
for i in range(30):
    clear(0)
    c=colour(200,0,0)
    x1 = random.randint(2,width-3)
    x2 = random.randint(2,width-3)
    x3 = random.randint(2,width-3)
    y1 = random.randint(2,height-3)
    y2 = random.randint(2,height-3)
    y3 = random.randint(2,height-3)
    tri_filled(x1,y1,x2,y2,x3,y3,c)    
    c=colour(0,200,0)
    triangle(x1,y1,x2,y2,x3,y3,c)
    c=colour(0,0,200)
    lcd.text(str(i),110,5,c)
    lcd.show()
    utime.sleep(0.6)

clear(0)
lcd.text("Done",45,40,colour(255,0,0))
lcd.show()
utime.sleep(3)

clear(0)
lcd.show()
