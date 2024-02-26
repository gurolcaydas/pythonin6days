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
    
    rekor_puan=0
    oyun_bitti=0
    saga_git=1
    alta_git=1
    sag_sol=1
    alt_ust=1
    

    LCD = LCD_1inch44()
    #color BRG
    LCD.fill(BLACK)
     
    LCD.show()
    
    def sifirla ():
        global raket_x, raket_y, dusman_x, dusman_y, oyuna_devam, kac_can_var, bu_oyun_puan, raket_en
        raket_en=12
        raket_x = 60
        raket_y = 110
        dusman_x = 60
        dusman_y = 45 
        oyuna_devam=0
        kac_can_var = 3
        bu_oyun_puan = 0
    
    def raket_ciz(): 
        LCD.fill_rect(raket_x, raket_y , raket_en, 4, WHITE)  # Wings

        return    
    def raket_sil(): 
        LCD.fill_rect(raket_x, raket_y , raket_en, 4, BLACK)  # Wings

        return
    def topu_ciz():
        # Define colors
        global sag_sol, alt_ust, dusman_x, dusman_y, saga_git
        
        
            
            
        LCD.rect(dusman_x +1 , dusman_y , 2, 4, BLACK)
        LCD.rect(dusman_x , dusman_y +1 , 4, 2, BLACK)
        if (dusman_x>119):
            sag_sol=-1
        if (dusman_x<5):
            sag_sol=+1
        if (dusman_y>125):
            alt_ust=-1
        if (dusman_y<2):
            alt_ust=+1
        if (dusman_x>=raket_x -3 and dusman_x<= raket_x + raket_en +2 and raket_y <= dusman_y +2 and raket_y >= dusman_y +2 ):
            alt_ust=-1
            LCD.fill_rect(4,4,120,120,BLACK)
            LCD.text(str(raket_x)+' '+str(dusman_x),2,2,BLUE)
            LCD.text(str(raket_y)+' '+str(dusman_y),2,12,BLUE)
            if (dusman_x==raket_x -3):
                saga_git = 2
            if (dusman_x<= raket_x + raket_en +2 ):
                saga_git = 1
        dusman_x = dusman_x + saga_git * sag_sol
        dusman_y = dusman_y + alta_git * alt_ust
        LCD.rect(dusman_x +1 , dusman_y , 2, 4, BROWN)
        LCD.rect(dusman_x , dusman_y +1 , 4, 2, YELLOW)
            
        
        return

    def tuglalar_ciz():
        global alt_ust
        # Iterate over the tuglalar list
        for tugla in tuglalar:
            # Draw a rectangle for each element in tuglalar list
            if (dusman_x>=tugla - 8 and dusman_x <= tugla and dusman_y <= 41 and dusman_y >= 36 ):
                eksik_tugla(tugla)
                alt_ust = alt_ust * (-1)
            LCD.fill_rect(tugla - 6, 40, 9, 4, RED)

    # Call the function to draw rectangles for each element in tuglalar list
    def eksik_tugla(element):
        if element in tuglalar:
            tuglalar.remove(element)
            
while True:

    LCD.fill_rect(0,0,127,127,BLACK)
    LCD.fill_rect(0,0,4,127,YELLOW)
    LCD.fill_rect(124,0,4,127,YELLOW)
    LCD.hline(0,0,128,YELLOW)
    #LCD.vline(0,0,127,YELLOW)
    #LCD.vline(127,5,17,YELLOW)
    

    
    limit_start = 1
    limit_end = 115
    step_size = 2
    tuglalar = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    
   
    key0 = Pin(15,Pin.IN,Pin.PULL_UP) 
    key1 = Pin(17,Pin.IN,Pin.PULL_UP)
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)
    sifirla()
    while(1):
        if (oyun_bitti>0):
            if (rekor_puan<bu_oyun_puan):
                rekor_puan=bu_oyun_puan
            LCD.fill_rect(4,4,120,120,BLACK)
            LCD.text('Game Over.',20,20,YELLOW)
            LCD.text('Puan  :' + str(bu_oyun_puan),20,40,WHITE)
            LCD.text('Rekor :' + str(rekor_puan),20,60,BLUE)
            bu_oyun_puan=0 
            raket_x = 60
            raket_y = 110
            dusman_x = 60
            dusman_y = 45
            LCD.show()
            time.sleep(1)
            LCD.text('Play ->',90,110,WHITE)
            LCD.show()
            
        else:

            LCD.text('Bricks',50,4,WHITE)
            LCD.show()
            
            LCD.text('Play ->',90,110,WHITE)
            LCD.show() 
            while (key0.value() != 0):
                calistir=1
            LCD.fill_rect(4,4,120,120,BLACK) 
            LCD.text('Ready!',42,50,SKY)
            LCD.show()
            time.sleep(2)
            LCD.fill_rect(4,4,120,120,BLACK)

       
        while(1):
            
            raket_sil()
            if(key0.value() == 0):
                raket_x=raket_x + step_size
                if (raket_x>limit_end):
                    raket_x=limit_end                
            if(key1.value() == 0):
                raket_x=raket_x- step_size
                if (raket_x<limit_start):
                    raket_x=limit_start
            LCD.fill_rect(4,4,120,120,BLACK)                    
            tuglalar_ciz()
            topu_ciz() 
            raket_ciz()
                
                  
            LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)








