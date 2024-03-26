from machine import Pin, SPI
import time

# Define SPI pins (you need to adjust these pins according to your setup)
spi = SPI(0)
spi.init(baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3))

# Define LCD control pins
cs = Pin(0, Pin.OUT)  # Chip select pin
dc = Pin(1, Pin.OUT)  # Data/command pin
rst = Pin(2, Pin.OUT) # Reset pin

# Reset the LCD
rst.low()
time.sleep_ms(50)
rst.high()
time.sleep_ms(50)

# Send commands to initialize the LCD
cs.low()  # Select the LCD
dc.low()  # Send command
spi.write(b'\x01')  # Command to set address mode (e.g., for setting horizontal addressing mode)
dc.high()  # Send data
spi.write(b'\x00')  # Data byte (e.g., horizontal addressing mode)
cs.high()  # Deselect the LCD

# Send bitmap data to the LCD
cs.low()  # Select the LCD
dc.low()  # Send command
spi.write(b'\x22')  # Command to set column address
dc.high()  # Send data
spi.write(b'\x00')  # Start column
spi.write(b'\x0F')  # End column
dc.low()  # Send command
spi.write(b'\x20')  # Command to set page address
dc.high()  # Send data
spi.write(b'\x00')  # Start page
spi.write(b'\x0F')  # End page
dc.low()  # Send command
spi.write(bytes(sinek_map))  # Send bitmap data
cs.high()  # Deselect the LCD
