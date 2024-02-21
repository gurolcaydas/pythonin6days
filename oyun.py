import machine
from machine import Pin,SPI,PWM
import framebuf
import time
from time import sleep
import random

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10    
CS = 9


class LCD_1inch44(framebuf.FrameBuffer):
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
        #Turn on the LCD display
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
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535
    PINK = 0xFFE0
    BLACK = 0x0000
    WHITE = 0xFFFF
    RED = 0xFF00
    DARKBLUE = 0x07E0
    SKY = 0x07FF
    BLUE = 0x07FA
    GREEN = 0x000D
    LIGHTGREEN = 0x000F
    YELLOW = 0xFF0F
    BROWN = 0xFA02
    CYAN = 0x40FFFF     # Cyan color (combination of green and blue)
    

    LCD = LCD_1inch44()
    #color BRG
    LCD.fill(BLACK)
     
    LCD.show()

    
    bizim_gemi_x = 60
    bizim_gemi_y = 100
    dusman_x = 60
    dusman_y = 1 
    bu_oyun_puan=0
    rekor_puan=0
    kacanlar = 0
    kac_can_var = 3
    oyuna_devam=0
    
    bizim_gemi_en = 12
    bizim_gemi_boy = 12
   
    def tuttum():
        if (bizim_gemi_x >= dusman_x - 9 and bizim_gemi_x<=dusman_x +9 and bizim_gemi_y >= dusman_y - 11 and bizim_gemi_y <= dusman_y +11):
            return 1
        return 0        

    def bizim_gemiyi_ciz():
        # Draw bounding box
        # Define the dimensions of the X-Wing

        global bizim_gemi_x, bizim_gemi_y
        # Draw the X-Wing body
        LCD.fill_rect(bizim_gemi_x + 4, bizim_gemi_y, 4, bizim_gemi_boy, BLUE)  # Main body
        LCD.fill_rect(bizim_gemi_x, bizim_gemi_y + 4, bizim_gemi_en, 4, BLUE)  # Wings

        # Draw the engines
        LCD.fill_rect(bizim_gemi_x, bizim_gemi_y + 2, 2, 2, DARKBLUE)  # Left engine
        LCD.fill_rect(bizim_gemi_x, bizim_gemi_y + 8, 2, 2, SKY)  # Right engine
        LCD.fill_rect(bizim_gemi_x + 10, bizim_gemi_y + 2, 2, 2, DARKBLUE) # Left engine
        LCD.fill_rect(bizim_gemi_x + 10, bizim_gemi_y + 8, 2, 2, SKY) # Right engine

        # Draw the cockpit
        LCD.fill_rect(bizim_gemi_x + 5, bizim_gemi_y + 4, 2, 2, BLACK)  # Cockpit

        return
    def dusman_gemisini_ciz():
        # Define colors
        global dusman_y, dusman_x, bu_oyun_puan, kacanlar
        if dusman_x < 8:
            fark = 3
        elif dusman_x > 105:
            fark = -3
        else:
            fark = 0
            pass
        level_speed = round((bu_oyun_puan / 5)) + 1
        dusman_y = dusman_y + random.randint(0 ,level_speed)
        dusman_x = dusman_x + random.randint(0 ,4) - 2
        
        LCD.vline(dusman_x + 4 , dusman_y + 3, 6 , YELLOW)
        LCD.vline(dusman_x + 2 , dusman_y + 3, 6 , YELLOW)
        LCD.fill_rect(dusman_x + 2, dusman_y , 3, 8, BROWN)
        LCD.fill_rect(dusman_x , dusman_y + 1, 4, 5, BLACK)
        LCD.fill_rect(dusman_x + 4, dusman_y + 0, 4, 5, BLACK)
        LCD.rect(dusman_x , dusman_y + 1, 4, 5, BROWN)
        LCD.rect(dusman_x + 4, dusman_y + 0, 4, 5, BROWN)

        if (dusman_y>114):
            dusman_y=1
            dusman_x= random.randint(30,80) 
            kacanlar = kacanlar + 1
            LCD.fill_rect(1, 120, 125, 7, WHITE)
            
        
        return
            
    def sinek ():
        # Define colors
        
        COL1 = 0xFFE0
        COL2 = 0xF83F
        COL3 = 0x003F
        COL4 = 0xFFC0
        COL5 = 0xD80F
        COL6 = 0x900F
        SOL1 = 0x1006
        SOL2 = 0x5006
        SOL3 = 0x00FF
        SOL4 = 0x04FF
        SOL5 = 0xF8FF
        SOL6 = 0xFCFF
        # Fill inner area with black
        LCD.hline(99,55,3,YELLOW)
        LCD.hline(99,54,3,YELLOW)
        LCD.hline(99,49,3,YELLOW)
        LCD.hline(99,48,3,YELLOW)
        LCD.hline(99,47,2,YELLOW)
        LCD.hline(99,40,3,YELLOW)
        LCD.hline(99,31,3,YELLOW)
        LCD.hline(99,30,7,YELLOW)
        LCD.hline(98,56,3,YELLOW)
        LCD.hline(98,41,3,YELLOW)
        LCD.hline(98,29,5,YELLOW)
        LCD.hline(97,46,3,YELLOW)
        LCD.hline(97,28,3,YELLOW)
        LCD.hline(97,27,2,YELLOW)
        LCD.hline(97,26,2,YELLOW)
        LCD.hline(97,25,2,YELLOW)
        LCD.hline(97,21,11,YELLOW)
        LCD.hline(96,57,4,YELLOW)
        LCD.hline(96,42,3,YELLOW)
        LCD.hline(96,33,12,YELLOW)
        LCD.hline(95,45,4,YELLOW)
        LCD.hline(95,32,6,YELLOW)
        LCD.hline(95,22,4,YELLOW)
        LCD.hline(94,34,5,YELLOW)
        LCD.hline(93,58,6,YELLOW)
        LCD.hline(93,35,4,YELLOW)
        LCD.hline(93,31,5,YELLOW)
        LCD.hline(93,30,3,YELLOW)
        LCD.hline(93,23,4,YELLOW)
        LCD.hline(92,29,2,YELLOW)
        LCD.hline(92,28,2,YELLOW)
        LCD.hline(91,75,3,YELLOW)
        LCD.hline(91,42,2,YELLOW)
        LCD.hline(91,24,3,YELLOW)
        LCD.hline(90,74,2,YELLOW)
        LCD.hline(90,41,3,YELLOW)
        LCD.hline(90,40,3,YELLOW)
        LCD.hline(89,60,3,YELLOW)
        LCD.hline(89,39,3,YELLOW)
        LCD.hline(89,25,4,YELLOW)
        LCD.hline(88,73,3,YELLOW)
        LCD.hline(88,72,2,YELLOW)
        LCD.hline(88,62,2,YELLOW)
        LCD.hline(88,61,3,YELLOW)
        LCD.hline(88,43,10,YELLOW)
        LCD.hline(88,38,4,YELLOW)
        LCD.hline(88,35,3,YELLOW)
        LCD.hline(88,34,3,YELLOW)
        LCD.hline(87,71,2,YELLOW)
        LCD.hline(87,37,4,YELLOW)
        LCD.hline(87,26,4,YELLOW)
        LCD.hline(86,70,2,YELLOW)
        LCD.hline(86,69,2,YELLOW)
        LCD.hline(86,68,1,YELLOW)
        LCD.hline(86,67,1,YELLOW)
        LCD.hline(86,66,2,YELLOW)
        LCD.hline(86,63,3,YELLOW)
        LCD.hline(86,59,10,YELLOW)
        LCD.hline(86,36,8,YELLOW)
        LCD.hline(85,64,4,YELLOW)
        LCD.hline(85,62,2,YELLOW)
        LCD.hline(85,27,4,YELLOW)
        LCD.hline(84,60,3,YELLOW)
        LCD.hline(83,65,5,YELLOW)
        LCD.hline(83,44,15,YELLOW)
        LCD.hline(83,28,4,YELLOW)
        LCD.hline(82,66,3,YELLOW)
        LCD.hline(82,61,5,YELLOW)
        LCD.hline(82,58,10,YELLOW)
        LCD.hline(82,35,5,YELLOW)
        LCD.hline(82,29,3,YELLOW)
        LCD.hline(81,67,3,YELLOW)
        LCD.hline(81,45,6,YELLOW)
        LCD.hline(80,68,2,YELLOW)
        LCD.hline(80,34,5,YELLOW)
        LCD.hline(79,57,6,YELLOW)
        LCD.hline(79,30,3,YELLOW)
        LCD.hline(78,69,3,YELLOW)
        LCD.hline(78,62,6,YELLOW)
        LCD.hline(78,46,5,YELLOW)
        LCD.hline(78,33,5,YELLOW)
        LCD.hline(77,70,3,YELLOW)
        LCD.hline(76,76,1,YELLOW)
        LCD.hline(76,72,2,YELLOW)
        LCD.hline(76,71,2,YELLOW)
        LCD.hline(76,56,6,YELLOW)
        LCD.hline(76,47,5,YELLOW)
        LCD.hline(75,75,2,YELLOW)
        LCD.hline(75,74,2,YELLOW)
        LCD.hline(75,73,2,YELLOW)
        LCD.hline(75,55,4,YELLOW)
        LCD.hline(75,48,4,YELLOW)
        LCD.hline(73,54,4,YELLOW)
        LCD.hline(73,32,8,YELLOW)
        LCD.hline(71,50,5,YELLOW)
        LCD.hline(71,49,6,YELLOW)
        LCD.hline(71,48,3,YELLOW)
        LCD.hline(71,47,3,YELLOW)
        LCD.hline(70,66,4,YELLOW)
        LCD.hline(70,53,6,YELLOW)
        LCD.hline(70,52,6,YELLOW)
        LCD.hline(70,51,6,YELLOW)
        LCD.hline(70,46,4,YELLOW)
        LCD.hline(70,45,3,YELLOW)
        LCD.hline(69,71,6,YELLOW)
        LCD.hline(69,70,6,YELLOW)
        LCD.hline(69,69,5,YELLOW)
        LCD.hline(69,68,4,YELLOW)
        LCD.hline(69,67,4,YELLOW)
        LCD.hline(69,65,5,YELLOW)
        LCD.hline(68,64,7,YELLOW)
        LCD.hline(68,54,4,YELLOW)
        LCD.hline(68,44,4,YELLOW)
        LCD.hline(67,55,3,YELLOW)
        LCD.hline(65,56,5,YELLOW)
        LCD.hline(63,63,18,YELLOW)
        LCD.hline(63,57,5,YELLOW)
        LCD.hline(61,62,5,YELLOW)
        LCD.hline(60,58,6,YELLOW)
        LCD.hline(59,61,3,YELLOW)
        LCD.hline(59,31,22,YELLOW)
        LCD.hline(57,43,14,YELLOW)
        LCD.hline(57,32,4,YELLOW)
        LCD.hline(56,30,5,YELLOW)
        LCD.hline(55,33,4,YELLOW)
        LCD.hline(54,74,3,YELLOW)
        LCD.hline(54,73,3,YELLOW)
        LCD.hline(54,72,3,YELLOW)
        LCD.hline(54,71,2,YELLOW)
        LCD.hline(54,70,2,YELLOW)
        LCD.hline(54,44,6,YELLOW)
        LCD.hline(53,76,2,YELLOW)
        LCD.hline(53,75,3,YELLOW)
        LCD.hline(53,69,3,YELLOW)
        LCD.hline(53,68,2,YELLOW)
        LCD.hline(53,67,2,YELLOW)
        LCD.hline(53,34,5,YELLOW)
        LCD.hline(52,77,2,YELLOW)
        LCD.hline(52,66,2,YELLOW)
        LCD.hline(52,65,2,YELLOW)
        LCD.hline(52,45,6,YELLOW)
        LCD.hline(52,35,4,YELLOW)
        LCD.hline(52,29,5,YELLOW)
        LCD.hline(51,64,2,YELLOW)
        LCD.hline(51,63,2,YELLOW)
        LCD.hline(51,61,2,YELLOW)
        LCD.hline(51,60,9,YELLOW)
        LCD.hline(51,46,5,YELLOW)
        LCD.hline(51,36,3,YELLOW)
        LCD.hline(50,62,2,YELLOW)
        LCD.hline(50,59,14,YELLOW)
        LCD.hline(50,47,4,YELLOW)
        LCD.hline(49,48,3,YELLOW)
        LCD.hline(49,28,6,YELLOW)
        LCD.hline(48,58,4,YELLOW)
        LCD.hline(47,67,1,YELLOW)
        LCD.hline(47,66,2,YELLOW)
        LCD.hline(47,65,2,YELLOW)
        LCD.hline(47,64,1,YELLOW)
        LCD.hline(47,57,4,YELLOW)
        LCD.hline(47,56,3,YELLOW)
        LCD.hline(47,55,2,YELLOW)
        LCD.hline(47,54,2,YELLOW)
        LCD.hline(47,53,2,YELLOW)
        LCD.hline(47,52,2,YELLOW)
        LCD.hline(47,39,4,YELLOW)
        LCD.hline(47,37,6,YELLOW)
        LCD.hline(47,36,3,YELLOW)
        LCD.hline(46,69,2,YELLOW)
        LCD.hline(46,68,2,YELLOW)
        LCD.hline(46,63,2,YELLOW)
        LCD.hline(46,62,2,YELLOW)
        LCD.hline(46,49,5,YELLOW)
        LCD.hline(46,42,2,YELLOW)
        LCD.hline(46,41,3,YELLOW)
        LCD.hline(46,40,4,YELLOW)
        LCD.hline(46,30,1,YELLOW)
        LCD.hline(46,27,6,YELLOW)
        LCD.hline(45,70,2,YELLOW)
        LCD.hline(45,61,2,YELLOW)
        LCD.hline(45,60,2,YELLOW)
        LCD.hline(45,51,5,YELLOW)
        LCD.hline(45,48,2,YELLOW)
        LCD.hline(45,47,2,YELLOW)
        LCD.hline(45,44,2,YELLOW)
        LCD.hline(45,43,3,YELLOW)
        LCD.hline(45,32,2,YELLOW)
        LCD.hline(45,31,2,YELLOW)
        LCD.hline(44,71,2,YELLOW)
        LCD.hline(44,59,2,YELLOW)
        LCD.hline(44,46,3,YELLOW)
        LCD.hline(44,33,3,YELLOW)
        LCD.hline(43,58,3,YELLOW)
        LCD.hline(43,38,9,YELLOW)
        LCD.hline(43,26,6,YELLOW)
        LCD.hline(42,72,3,YELLOW)
        LCD.hline(42,57,3,YELLOW)
        LCD.hline(42,56,2,YELLOW)
        LCD.hline(42,50,9,YELLOW)
        LCD.hline(42,45,5,YELLOW)
        LCD.hline(42,37,4,YELLOW)
        LCD.hline(41,73,3,YELLOW)
        LCD.hline(41,55,2,YELLOW)
        LCD.hline(40,54,2,YELLOW)
        LCD.hline(40,44,4,YELLOW)
        LCD.hline(40,35,5,YELLOW)
        LCD.hline(40,25,5,YELLOW)
        LCD.hline(39,74,3,YELLOW)
        LCD.hline(39,53,2,YELLOW)
        LCD.hline(39,49,4,YELLOW)
        LCD.hline(39,34,7,YELLOW)
        LCD.hline(38,75,2,YELLOW)
        LCD.hline(38,43,4,YELLOW)
        LCD.hline(38,33,3,YELLOW)
        LCD.hline(37,52,3,YELLOW)
        LCD.hline(36,51,3,YELLOW)
        LCD.hline(36,42,4,YELLOW)
        LCD.hline(36,36,8,YELLOW)
        LCD.hline(36,28,3,YELLOW)
        LCD.hline(36,27,3,YELLOW)
        LCD.hline(36,26,2,YELLOW)
        LCD.hline(36,24,6,YELLOW)
        LCD.hline(35,50,3,YELLOW)
        LCD.hline(35,41,3,YELLOW)
        LCD.hline(35,37,5,YELLOW)
        LCD.hline(35,29,4,YELLOW)
        LCD.hline(34,49,2,YELLOW)
        LCD.hline(34,47,2,YELLOW)
        LCD.hline(34,31,5,YELLOW)
        LCD.hline(33,48,7,YELLOW)
        LCD.hline(33,40,3,YELLOW)
        LCD.hline(33,30,5,YELLOW)
        LCD.hline(33,23,5,YELLOW)
        LCD.hline(31,39,3,YELLOW)
        LCD.hline(31,32,9,YELLOW)
        LCD.hline(30,29,4,YELLOW)
        LCD.hline(29,38,4,YELLOW)
        LCD.hline(29,34,3,YELLOW)
        LCD.hline(29,33,5,YELLOW)
        LCD.hline(28,37,4,YELLOW)
        LCD.hline(27,28,6,YELLOW)
        LCD.hline(27,22,7,YELLOW)
        LCD.hline(26,36,4,YELLOW)
        LCD.hline(24,35,4,YELLOW)
        LCD.hline(24,24,2,YELLOW)
        LCD.hline(22,34,4,YELLOW)
        LCD.hline(21,27,9,YELLOW)
        LCD.hline(21,21,9,YELLOW)
        LCD.hline(20,33,4,YELLOW)
        LCD.hline(20,26,7,YELLOW)
        LCD.hline(19,28,4,YELLOW)
        LCD.hline(18,32,5,YELLOW)
        LCD.hline(17,31,4,YELLOW)
        LCD.hline(17,25,9,YELLOW)
        LCD.hline(15,30,4,YELLOW)
        LCD.hline(14,20,11,YELLOW)
        LCD.hline(13,29,4,YELLOW)
        LCD.hline(13,21,4,YELLOW)
        LCD.hline(12,28,3,YELLOW)
        LCD.hline(12,22,3,YELLOW)
        LCD.hline(11,27,3,YELLOW)
        LCD.hline(11,26,2,YELLOW)
        LCD.hline(11,25,2,YELLOW)
        LCD.hline(11,24,2,YELLOW)
        LCD.hline(11,23,3,YELLOW)
        LCD.hline(109,26,2,YELLOW)
        LCD.hline(109,25,2,YELLOW)
        LCD.hline(109,24,2,YELLOW)
        LCD.hline(108,28,2,YELLOW)
        LCD.hline(108,27,3,YELLOW)
        LCD.hline(108,23,3,YELLOW)
        LCD.hline(107,30,3,YELLOW)
        LCD.hline(107,29,3,YELLOW)
        LCD.hline(106,31,3,YELLOW)
        LCD.hline(106,22,4,YELLOW)
        LCD.hline(105,35,2,YELLOW)
        LCD.hline(105,34,2,YELLOW)
        LCD.hline(105,32,3,YELLOW)
        LCD.hline(104,36,2,YELLOW)
        LCD.hline(102,37,3,YELLOW)
        LCD.hline(102,26,3,YELLOW)
        LCD.hline(102,25,3,YELLOW)
        LCD.hline(102,24,3,YELLOW)
        LCD.hline(101,38,3,YELLOW)
        LCD.hline(101,28,3,YELLOW)
        LCD.hline(101,27,4,YELLOW)
        LCD.hline(100,53,3,YELLOW)
        LCD.hline(100,52,3,YELLOW)
        LCD.hline(100,51,3,YELLOW)
        LCD.hline(100,50,3,YELLOW)
        LCD.hline(100,39,3,YELLOW)
        LCD.hline(100,20,5,YELLOW)
while True:

    LCD.hline(0,0,127,YELLOW)
    LCD.hline(0,127,128,YELLOW)
    LCD.vline(0,0,127,YELLOW)
    LCD.vline(127,0,127,YELLOW)
    
    LCD.fill_rect(1,1,126,126,BLACK)

    
    limit_start = 1
    limit_end = 115
    step_size = 2
    
   
    key0 = Pin(15,Pin.IN,Pin.PULL_UP) 
    key1 = Pin(17,Pin.IN,Pin.PULL_UP)
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)
    while(1):
        if (kacanlar>kac_can_var):
            oyuna_devam=0
            if (rekor_puan<bu_oyun_puan):
                rekor_puan=bu_oyun_puan
            LCD.fill_rect(1,1,126,126,BLACK)
            LCD.text('Game Over.',20,20,YELLOW)
            LCD.text('Puan  :' + str(bu_oyun_puan),20,40,WHITE)
            LCD.text('Rekor :' + str(rekor_puan),20,60,BLUE)
            bu_oyun_puan=0 
            bizim_gemi_x = 60
            bizim_gemi_y = 100
            dusman_x = 60
            dusman_y = 1
            LCD.show()
            time.sleep(3)
            LCD.text('Play ->',90,110,WHITE)
            LCD.show()
            
        else:

            sinek()
            LCD.show()
            time.sleep(3)
            LCD.text('Saldirilardan',10,84,BROWN)
            LCD.text('Dunyayi',10,96,BROWN)
            LCD.text('Kurtarin',10,108,BROWN)
            LCD.show()
            time.sleep(1)
            LCD.text('SiNEK',50,4,WHITE)
            LCD.show()
            time.sleep(1)
            
            LCD.text('Play ->',90,110,WHITE)
            LCD.show() 

        while(oyuna_devam<1):
            if(key0.value() == 0):
                kacanlar=0
                oyuna_devam=1
                LCD.fill_rect(1,1,126,126,BLACK)
                sinek()
                LCD.show()
                time.sleep(2)
                LCD.fill_rect(1,1,126,126,BLACK)
                LCD.text('3',62,62,WHITE)
                LCD.show() 
                time.sleep(1)
                LCD.fill_rect(1,1,126,126,BLACK)
                LCD.text('2',62,62,WHITE)
                LCD.show() 
                time.sleep(1)
                LCD.fill_rect(1,1,126,126,BLACK)
                LCD.text('1',62,62,WHITE)
                LCD.show() 
                time.sleep(1)
                
                
       
        while(kacanlar<=kac_can_var and oyuna_devam>0):
            
            LCD.rect(0,0,128,128,BLUE)
            if(key3.value() == 0):
                bizim_gemi_y=bizim_gemi_y- step_size
                if (bizim_gemi_y<limit_start):
                    bizim_gemi_y=limit_start           
            if(key2.value() == 0):
                bizim_gemi_y=bizim_gemi_y+ step_size
                if (bizim_gemi_y>limit_end):
                    bizim_gemi_y=limit_end  
            if(key0.value() == 0):
                bizim_gemi_x=bizim_gemi_x + step_size
                if (bizim_gemi_x>limit_end):
                    bizim_gemi_x=limit_end                
            if(key1.value() == 0):
                bizim_gemi_x=bizim_gemi_x- step_size
                if (bizim_gemi_x<limit_start):
                    bizim_gemi_x=limit_start     
            #show_space_view(space_view_data)
            LCD.fill_rect(1,1,126,126,BLACK)
            
            LCD.text(str(bu_oyun_puan),4,4,WHITE)
            LCD.text(str(rekor_puan),60,4,BLUE)
            LCD.text(str(kac_can_var - kacanlar),116,4,YELLOW)
            
            dusman_gemisini_ciz()
            bizim_gemiyi_ciz()        
            if (tuttum() == 1):
                LCD.rect(0,0,128,128,WHITE)
                bu_oyun_puan = bu_oyun_puan + 1 
                dusman_y = 1 
                  
            LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)








