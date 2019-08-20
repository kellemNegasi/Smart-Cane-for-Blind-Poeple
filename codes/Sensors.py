import pygame
pygame.mixer.init(frequency=19000, size=-16, channels=2, buffer=4096)
pygame.init()
import RPi.GPIO as GPIO
import time
#pin definition ............................................

GPIO.setmode(GPIO.BCM)
Buzzer =15 # pin number assigned to the buzzer signal
IR_pin = 16 # pin number assined to Infrared signal
TRIG_front = 2 # trig pin for the front ultrasonic sensor
ECHO_front = 3 # echo pin for the front ultrasonic sensor
TRIG_left = 14  # trig pin for the left ultrasonic sensor
ECHO_left = 15  # echo pin for the left ultrasonic sensor
TRIG_right = 17  # trig pin for the right ultrasonic sensor
ECHO_right = 27 # echo pin for the l eft ultrasonic sensor
LED_pin = 21 # LED pin number
LDR_pin = 20 #pin from the LDR
moisture_pin =23
#...........................................................
def LED_on():
    GPIO.output(LED_pin, True)
def LED_off():
    GPIO.output(LED_pin, False)
def play_sound(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(0)
    clock = pygame.time.Clock()
    clock.tick(10)
    while pygame.mixer.music.get_busy():
        pygame.event.poll()
        clock.tick(10)
        time.sleep(0.5)
def GPIO_setup():
    GPIO.setwarnings(False)
    GPIO.setup(Buzzer,GPIO.OUT)
    GPIO.setup(TRIG_front,GPIO.OUT)
    GPIO.setup(ECHO_front,GPIO.IN)
    GPIO.setup(IR_pin,GPIO.IN)
    GPIO.setup(TRIG_left,GPIO.OUT)
    GPIO.setup(ECHO_left,GPIO.IN)
    GPIO.setup(TRIG_right,GPIO.OUT)
    GPIO.setup(ECHO_right,GPIO.IN)
    GPIO.setup(LED_pin,GPIO.OUT)
#claculate the charging time of the capacitor 
def rc_time_moisture (pin_to_circuit):
    count = 0 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin_to_circuit, GPIO.IN)
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        time.sleep(0.000001)
        count += 1
    return count
def check_moisture():
    time.sleep(0.5)
    t = rc_time(rc_pin)
    if t>45:
        return True
    else:
        return False
def rc_time (pin_to_circuit):
    GPIO.setup(LED_pin, GPIO.OUT)
    GPIO.output(LED_pin,GPIO.LOW)
    count = 0 
    GPIO.setup(pin_to_circuit, GPIO.OUT)

    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin_to_circuit, GPIO.IN)
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count
def check_darkness():
    if rc_time(LDR_pin)>3000:
        ptint(rc_time(LDR_pin))
        return True
    else:
        return False 
def get_distance(trig,echo):
    pulse_start =0
    pulse_end = 0
    GPIO.output(trig, False)                 
    time.sleep(0.5)                            
    GPIO.output(trig, True)                  
    time.sleep(0.00001)                      
    GPIO.output(trig, False)                 
    while GPIO.input(echo)==0:                
        pulse_start = time.time()
    while GPIO.input(echo)==1:
        pulse_end = time.time()      
    pulse_duration = pulse_end - pulse_start     
    distance = pulse_duration * 17150        
    distance = round(distance, 2)            
    if distance > 2 and distance < 400:      
        return distance - 0.5
    else:
        return -1

def obstacle_detected(distance):
    if distance<=200:
        return True
    else:
        return False
def buzzer_beep():
    GPIO.output(15, True)
    time.sleep(0.001)
    GPIO.output(15, False)
def decide_direction(front,left,right):
    if (front>0 and left>0) and right>0:
        if left>200 and left>right:
            play_sound("/home/pi/voices/Turn Left.wav")
        elif right>200 and right>left:
            #print("turn right")
            play_sound("/home/pi/voices/Turn Right.wav")
        else:
            #print("there is no safe turn return back")
            play_sound("/home/pi/voices/step back.wav")
def small_obstacle():
    return GPIO.input(IR_pin)
def destroy():
    GPIO.cleanup() # Release resource
def loop():
    while True:
        time.sleep(1)
        print("starting")
        front_dis = 100
        left_dis =20
        right_dis =50
        front_dis = get_distance(TRIG_front,ECHO_front)
        left_dis = get_distance(TRIG_left,ECHO_left)
        right_dis = get_distance(TRIG_right,ECHO_right)
        print('Distance front: {} centimeters'.format(front_dis))
        print('Distance Left: {} centimeters'.format(left_dis))
        print('Distance right: {} centimeters'.format(right_dis))
        if obstacle_detected(front_dis):
            buzzer_beep()
            decide_direction(front_dis,left_dis,right_dis)
        if small_obstacle():
            buzzer_beep()
           play_sound("/home/pi/voices/small obstacles.wav")
        if moisture_check():
           buzzer_beep()
            play_sound("/home/pi/voices/water.wav")
        if check_darkness():
            LED_on()
        else:
            LED_off()
def sense():          
    try:
        GPIO_setup()
        loop()
    except KeyboardInterrupt:
        pass
    finally:
        destroy()
if __name__ == '__main__':
    sense()
