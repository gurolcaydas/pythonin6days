# WS128x128 1.44" lcd Minimum
# Called Pico-LCD-1.44" 
# Tony Goodhew 21st April 2022 for thepihut.com
from machine import Pin,SPI,PWM
import machine
import framebuf
import utime
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
width = 128 # Screen size in pixels
height = 128
# ==== Board now setup ========== MAIN BELOW====================
lcd.text("Red",5,5,colour(255,0,0))
lcd.text("Green",5,15,colour(0,255,0))
lcd.text("Blue",5,25,colour(0,0,255))
lcd.text('1.44" 128x128"',5,35,colour(255,255,0))
lcd.show()
utime.sleep(3)

# Tidy Up ============
pwm.duty_u16(32768)# HALF BRIGHTNESS
clear(0)
lcd.show()
