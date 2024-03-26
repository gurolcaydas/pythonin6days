
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
key0 = Pin(15,Pin.IN,Pin.PULL_UP) 
key1 = Pin(17,Pin.IN,Pin.PULL_UP)
key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)

def colour(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((R&0b11111000)>>3)<<8) + (B&0b11111000)+((G&0b11100000)>>5)

def clear(c):
    lcd.fill(c)


# Define main colors
RED = colour(255, 40, 40)
GREEN = colour(40, 255, 40)
BLUE = colour(40, 40, 255)
YELLOW = colour(255, 255, 40)
CYAN = colour(40, 255, 255)
MAGENTA = colour(255, 40, 255)
DARK_ORANGE = colour(255, 165, 40)
PINK = colour(255, 192, 203)

# Define darker and lighter versions of main colors
RED_D = colour(128, 20, 20)
RED_L = colour(255, 128, 128)
GREEN_D = colour(20, 128, 20)
GREEN_L = colour(128, 255, 128)
BLUE_D = colour(20, 20, 128)
BLUE_L = colour(100, 100, 255)
YELLOW_D = colour(128, 128, 20)
YELLOW_L = colour(255, 255, 128)
CYAN_D = colour(20, 128, 128)
CYAN_L = colour(128, 255, 255)
MAGENTA_D = colour(128, 20, 128)
MAGENTA_L = colour(255, 128, 255)
DARK_ORANGE_D = colour(128, 82, 20)
DARK_ORANGE_L = colour(255, 207, 128)
PINK_D = colour(255, 174, 185)
PINK_L = colour(255, 219, 230)

# Define additional side colors
BROWN = colour(165, 42, 42)

# Define grayscale tones
WHITE = colour(255, 255, 255)
GRAY_L = colour(192, 192, 192)
GRAY = colour(128, 128, 128)
GRAY_D = colour(64, 64, 64)
BLACK = colour(0, 0, 0)

# ************************ game definitions ******************************************
# ************************ game definitions ******************************************
# ************************ game definitions ******************************************




# ************************ game definitions ******************************************
# ************************ game definitions ******************************************
# ************************ game definitions ******************************************
def puan_yaz(puan):
    text = str (puan)
    text_len = len (text) * 8
    print (text_len)
    print(len(text))
    lcd.fill_rect(0,0,127,8,BLACK)
    lcd.text (text,128 - text_len,1,PINK)
    
def oyun_reset():
    global running, bu_oyun_puan
    running=True
    bu_oyun_puan=0
    
def top_ciz(x,y):
    lcd.fill_rect(x,y+1,4,2,RED_D)
    lcd.fill_rect(x+1,y,2,4,RED_D)
    lcd.fill_rect(x+1,y+1,2,2,RED)
    lcd.fill_rect(x+1,y+1,1,1,RED_L)

def top_check_y(x,y):
    sonuc=True
    c=lcd.pixel(x,y+(dikey_git*4))
    if (c!=0):
        sonuc=False    
    if (y>limit_y1-4 or y<limit_y0):
        sonuc=False
    return(sonuc)
    
def top_check_x(x,y):
    sonuc=True
    c=lcd.pixel(x+(4*yatay_git),y)
    if (c!=0):
        sonuc=False
    if (x>limit_x1-4 or x<limit_x0):
        sonuc=False
    return(sonuc)
    
    
def cubuk_ciz(x,y,z):
    lcd.fill_rect(x,y,z,3,BLUE_D)
    lcd.fill_rect(x+1,y,z-2,2,BLUE)
        
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
if __name__=='__main__':


# örnek komutlar ------------------------------------------------------------------------
# lcd.vline(x, y, h, c)
# lcd.hline(x, y, w, c) 
# lcd.line(x1, y1, x2, y2, c)
# lcd.rect(x, y, w, h, c)
# lcd.fill_rect(x, y, w, h, c)
# lcd.text(s, x, y[, c])
# lcd.scroll(xstep, ystep)
# FrameBuffer.blit(fbuf, x, y, key=- 1, palette=None)
# örnek komutlar ------------------------------------------------------------------------
#     for i in range(128):
#         lcd.scroll(0,2)
#         lcd.show()
#         utime.sleep(0.1) # Delay  
# örnek komutlar ------------------------------------------------------------------------
   
    bu_oyun_puan=0
    yeni_oyun=0
    oyun_aktif=0
    yatay_git=1
    dikey_git=1
    
    yatay_adim=1
    dikey_adim=1
    
    top_x=10
    top_y=10
    top_aktif=True
    
    cubuk_x=60
    cubuk_y=120
    cubuk_en=12
    cubuk_adim=3
    
    limit_x0=0
    limit_x1=100
    
    limit_y0=0
    limit_y1=127
    
    oyun_reset()    

    clear(0) # Black background
    lcd.show()
# ******************************* MAIN **************************************************
# ******************************* MAIN **************************************************   

    while(running):      
        if (yeni_oyun==1):
            oyun_reset()
            lcd.text("Birriks",20,20,colour(50,150,255))
            lcd.show()
            utime.sleep(2)
            clear(0)
            yeni_oyun=0
        if(key0.value() == 0):
            yeni_oyun=1
            oyun_aktif=True
            
        if(key1.value() == 0):
            puan_yaz(10)
            lcd.fill_rect(100,70,20,20,colour(127,127,0))
        else :
            lcd.fill_rect(100,70,20,20,colour(0,0,0))
            lcd.rect(100,70,20,20,colour(0,110,110))
            
        if(key2.value() == 0):
            puan_yaz(bu_oyun_puan)
            lcd.fill_rect(100,40,20,20,colour(127,127,0))
        else :
            lcd.fill_rect(100,40,20,20,colour(0,0,0))
            lcd.rect(100,40,20,20,colour(0,110,110))
        if(key3.value() == 0):
            running=0
        lcd.show()

# ******************************* OYUN **************************************************  
# ******************************* OYUN **************************************************          
        while(oyun_aktif):

            if(top_aktif):
                top_x2=top_x+ yatay_adim * yatay_git
                top_y2=top_y+ dikey_adim * dikey_git
                if(top_check_x(top_x2,top_y2)):
                    top_x=top_x2
                    top_y=top_y2
                else:
                    yatay_git = yatay_git * (-1)
                    
                if(top_check_y(top_x2,top_y2)):
                    top_x=top_x2
                    top_y=top_y2
                else:
                    dikey_git = dikey_git * (-1)
            
            if(key0.value() == 0):
                cubuk_x = cubuk_x - cubuk_adim
                if (cubuk_x<limit_x0):
                    cubuk_x=limit_x0
            if(key1.value() == 0):
                cubuk_x = cubuk_x + cubuk_adim
                if (cubuk_x>limit_x1-cubuk_en):
                    cubuk_x=limit_x1-cubuk_en
            clear(0)
            top_ciz(top_x,top_y)
            cubuk_ciz(cubuk_x,cubuk_y,cubuk_en)
            lcd.rect(50,60,120,10,colour(0,110,110))
            lcd.show()
            
# ******************************* OYUN **************************************************  
# ******************************* OYUN **************************************************          
    utime.sleep(1)
    clear(0)
    lcd.show()






