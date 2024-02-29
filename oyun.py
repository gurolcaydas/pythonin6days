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
    saga_git=0.8
    alta_git=0.7
    sag_sol=1
    alt_ust=1
    level = 1
    
    yandi = 0
    bonus_var=0
    bonus_y=45
    bonus_x=60
    
    

    LCD = LCD_1inch44()
    #color BRG
    LCD.fill(BLACK)
     
    LCD.show()
    
    def sifirla ():
        global raket_x, raket_y, dusman_x, dusman_y, dusman_x2, dusman_y2, oyuna_devam, kac_can_var, bu_oyun_puan, raket_en, yandi, tuglalar1, tuglalar2, tuglalar3
        raket_en=12
        raket_x = 60
        raket_y = 110
        dusman_x = 60
        dusman_y = 45 
        dusman_x2 = 60
        dusman_y2 = 45 
        oyuna_devam=0
        kac_can_var = 3
        bu_oyun_puan = 0
        yandi = 0
        saga_git=0.8
        alta_git=0.7
        sag_sol=1
        alt_ust=1
        level = 1
        tuglalar1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        tuglalar2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        tuglalar3 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    
        LCD.text('Bricks',50,14,WHITE)
        LCD.show()
        
        LCD.text('Play->',70,110,WHITE)
        LCD.show() 
        while (key0.value() != 0):
            calistir=1
        LCD.fill_rect(4,10,120,120,BLACK)
        
        tuglalar_ciz()
        LCD.text('Ready!',42,50,SKY)
        LCD.show()
        time.sleep(2)
        LCD.fill_rect(4,10,120,120,BLACK)
        
    def can_kaybi ():
        global raket_x, raket_y, dusman_x, dusman_y, dusman_x2, dusman_y2, oyuna_devam, kac_can_var, bu_oyun_puan, raket_en, yandi, level
        raket_x = 60
        raket_y = 110
        dusman_x = 60
        dusman_y = 45 
        dusman_x2 = 60
        dusman_y2 = 45 
        oyuna_devam=0
        yandi = 0
        level=1
        saga_git=0.7
        alta_git=0.8
        alt_ust=1
        LCD.fill_rect(4,10,120,120,BLACK)
        
        tuglalar_ciz()
        LCD.text('Ready!',42,50,SKY)
        LCD.show()
        time.sleep(2)
        LCD.fill_rect(4,10,120,120,BLACK)
                
    def raket_ciz(): 
        LCD.fill_rect(raket_x, raket_y , raket_en, 4, WHITE)  # Wings

        return    
    def raket_sil(): 
        LCD.fill_rect(raket_x, raket_y , raket_en, 4, BLACK)  # Wings

        return
    def topu_ciz():
        # Define colors
        global sag_sol, alt_ust, dusman_x, dusman_y, dusman_x2, dusman_y2, saga_git, kac_can_var, yandi, alta_git
        
        
            
            
        #LCD.rect(dusman_x2 +1 , dusman_y2 , 2, 4, BLACK)
        #LCD.rect(dusman_x2 , dusman_y2 +1 , 4, 2, BLACK)
        if (dusman_x2>118):
            sag_sol=-1
        if (dusman_x2<6):
            sag_sol=+1
        if (dusman_y2>125):
            #alt_ust=-1
            kac_can_var = kac_can_var - 1
            yandi=1
        if (dusman_y2<3):
            alt_ust=+1
        if (dusman_x2>=raket_x -3 and dusman_x2<= raket_x + raket_en +1 and raket_y <= dusman_y2 +2  ):
            alt_ust=-1
            if (dusman_x2<raket_x + 3 and sag_sol == -1):
                saga_git = 1.25
                alta_git = 0.8
            else:
                saga_git = 1.1
                alta_git = 1
            if (dusman_x2 > raket_x + 4 and sag_sol == 1):
                saga_git = 0.8
                alta_git = 1.25
        dusman_x = dusman_x + saga_git * sag_sol * level
        dusman_y = dusman_y + alta_git * alt_ust * level
        dusman_x2 = int(dusman_x)
        dusman_y2 = int(dusman_y)
        LCD.rect(dusman_x2 +1 , dusman_y2 , 2, 4, BROWN)
        LCD.rect(dusman_x2 , dusman_y2 +1 , 4, 2, BROWN)
        LCD.rect(dusman_x2 +1 , dusman_y2 +1 , 2, 2, YELLOW)
            
        
        return

    def puan_yaz():
        #LCD.fill_rect(4,1,120,10,BLACK)
        LCD.text(str(kac_can_var),60,2,YELLOW)
        LCD.text(str(bu_oyun_puan),6,2,BROWN)
        LCD.text(str(rekor_puan),100,2,BLUE)
        #LCD.text(str(saga_git),6,2,BROWN)
        #LCD.text(str(alta_git),100,2,BLUE)
            
    def tuglalar_ciz():
        global alt_ust, dusman_x2, dusman_y2, bonus_var, bonus_y, bonus_x
        # Iterate over the tuglalar list
        for tugla in tuglalar1:
            # Draw a rectangle for each element in tuglalar list
            if (dusman_x2>=tugla - 8 and dusman_x2 <= tugla and dusman_y <= 41 and dusman_y >= 36 ):
                eksik_tugla1(tugla)
                alt_ust = alt_ust * (-1)
                random_bonus=random.randint(0, 1)
                if (bonus_var==0 and random_bonus==1):
                    bonus_x = tugla - 5                    
                    bonus_var=1
                
            LCD.fill_rect(tugla - 6, 40, 9, 4, RED)
            
        for tugla in tuglalar2:
            # Draw a rectangle for each element in tuglalar list
            if (dusman_x2>=tugla - 8 and dusman_x2 <= tugla and dusman_y <= 31 and dusman_y >= 26 ):
                eksik_tugla2(tugla)
                alt_ust = alt_ust * (-1)
            LCD.fill_rect(tugla - 6, 30, 9, 4, BROWN)
        
        for tugla in tuglalar3:
            # Draw a rectangle for each element in tuglalar list
            if (dusman_x2>=tugla - 8 and dusman_x2 <= tugla and dusman_y <= 21 and dusman_y >= 16 ):
                eksik_tugla3(tugla)
                alt_ust = alt_ust * (-1)
            LCD.fill_rect(tugla - 6, 20, 9, 4, SKY)
        if ((len(tuglalar3) + len (tuglalar2) + len (tuglalar3))==0):
            yeni_level()

    def yeni_level():
        global raket_x, raket_y, dusman_x, dusman_y, oyuna_devam, kac_can_var, bu_oyun_puan, raket_en, yandi, tuglalar1, tuglalar2, tuglalar3, level
        raket_en=12
        raket_x = 60
        raket_y = 110
        dusman_x = 60
        dusman_y = 45 
        dusman_x2 = 60
        dusman_y2 = 45
        level = 1
        oyuna_devam=0
        yandi = 0
        tuglalar1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        tuglalar2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        tuglalar3 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        LCD.fill_rect(4,10,120,120,BLACK)
        tuglalar_ciz()
        LCD.text('Ready!',42,50,SKY)
        LCD.show()
        time.sleep(2)
        LCD.fill_rect(4,10,120,120,BLACK) 
            
    # Call the function to draw rectangles for each element in tuglalar list
    def eksik_tugla1(element):
        global bu_oyun_puan, level
        level = level + 0.1
        if element in tuglalar1:
            tuglalar1.remove(element)
            bu_oyun_puan=bu_oyun_puan + 10
    def eksik_tugla2(element):
        global bu_oyun_puan
        if element in tuglalar2:
            tuglalar2.remove(element)
            bu_oyun_puan=bu_oyun_puan + 11
    def eksik_tugla3(element):
        global bu_oyun_puan
        if element in tuglalar3:
            tuglalar3.remove(element)
            bu_oyun_puan=bu_oyun_puan + 12
    def bonus_gelsin():
        global bonus_var, bonus_x, bonus_y, bu_oyun_puan
        if (bonus_x>=raket_x -8 and bonus_x<= raket_x + raket_en +1 and raket_y <= bonus_y +2  ):
            bonus_var=0
            bonus_y=45
            bu_oyun_puan=bu_oyun_puan + 100
        if(bonus_var==1):
            bonus_y = bonus_y + 1
            LCD.rect(bonus_x +1 , bonus_y , 6, 4, DARKBLUE)
            LCD.rect(bonus_x , bonus_y +1 , 8, 2, SKY)
        if(bonus_y>126):
            bonus_var=0
            bonus_y=45            
            
                        
while True:

    LCD.fill_rect(0,0,127,127,BLACK)
    LCD.fill_rect(0,0,4,127,YELLOW)
    LCD.fill_rect(124,0,4,127,YELLOW)
    LCD.hline(0,0,128,YELLOW)
    #LCD.vline(0,0,127,YELLOW)
    #LCD.vline(127,5,17,YELLOW)
    

    
    limit_start = 4
    limit_end = 112
    step_size = 3
    tuglalar1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    tuglalar2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    tuglalar3 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    
   
    key0 = Pin(15,Pin.IN,Pin.PULL_UP) 
    key1 = Pin(17,Pin.IN,Pin.PULL_UP)
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)
    sifirla()
    

    while(1):
        
        if (kac_can_var<0):
            if (rekor_puan<bu_oyun_puan):
                rekor_puan=bu_oyun_puan
            LCD.fill_rect(4,10,120,120,BLACK)
            LCD.text('Game Over.',20,20,YELLOW)
            LCD.text('Puan  :' + str(bu_oyun_puan),20,40,WHITE)
            LCD.text('Rekor :' + str(rekor_puan),20,60,BLUE)
            bu_oyun_puan=0
            kac_can_var=3
            raket_x = 60
            raket_y = 110
            dusman_x = 60
            dusman_y = 45
            dusman_x2 = 60
            dusman_y2 = 45
            tuglalar1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
            tuglalar2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
            tuglalar3 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
            LCD.show()
            time.sleep(1)
            LCD.text('Play->',70,110,WHITE)
            LCD.show()
            while (key0.value() != 0):
                calistir=1
             

        puan_yaz()           
        if (yandi>0):
            can_kaybi()
       
        while(yandi<1):
            
            raket_sil()
            if(key0.value() == 0):
                raket_x=raket_x + step_size
                if (raket_x>limit_end):
                    raket_x=limit_end                
            if(key1.value() == 0):
                raket_x=raket_x- step_size
                if (raket_x<limit_start):
                    raket_x=limit_start
            LCD.fill_rect(4,1,120,127,BLACK)
            puan_yaz()
            tuglalar_ciz()
            topu_ciz() 
            raket_ciz()
            bonus_gelsin()
            
                
                  
            LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)








