import RPi.GPIO as GPIO
import pigpio
import time

PIN_SWITCH = 7

#Sensor ECHO pins
PIN_TRIG_FRONT = 11
PIN_TRIG_RIGHT = 13
PIN_TRIG_BACK  = 15

#Sensor TRIG pins
PIN_ECHO_FRONT = 36
PIN_ECHO_RIGHT = 38
PIN_ECHO_BACK  = 40


PIN_STEERING = 26 #BCM
PIN_THROTTLE = 19 #BCM

PWM_STEERING_NEUTRAL = 9.5 # %
PWM_STEERING_LEFT = 11.3 # %
PWM_STEERING_RIGHT = 8.2 # %

PWM_THROTTLE_NEUTRAL = 9.1 # %
#PWM_THROTTLE_FWD = 9.8 # %
PWM_THROTTLE_FWD = 9.5 # %
#PWM_THROTTLE_REV = 8.9 # %
PWM_THROTTLE_REV = 8.7 # %
#GPIO.setmode(GPIO.BOARD)

PWM_RANGE = 10000
PWM_FACTOR = PWM_RANGE / 100 
PWM_FREQ = 61

steering = None
throttle = None

def isPressed():
    pin_state = GPIO.input(PIN_SWITCH)
    return pin_state

def gpioInit(callbackFunction):
    
    print ("GPIO initialization started.")
    GPIO.setwarnings(False)
    ###Initialize the switch
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(PIN_SWITCH, GPIO.FALLING, callback=callbackFunction, bouncetime = 200) # Setup event on pin 10 rising edge
    
    print ("Sensor GPIO initialization started.")
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PIN_TRIG_FRONT, GPIO.OUT)
    GPIO.setup(PIN_TRIG_RIGHT, GPIO.OUT)
    GPIO.setup(PIN_TRIG_BACK,  GPIO.OUT)
    
    GPIO.setup(PIN_ECHO_FRONT, GPIO.IN)
    GPIO.setup(PIN_ECHO_RIGHT, GPIO.IN)
    GPIO.setup(PIN_ECHO_BACK,  GPIO.IN)

    global steering
    global throttle
    
    #Initialize steering and throttle PWM channels
    steering = pigpio.pi()      
    throttle = pigpio.pi()

    steering.set_PWM_range(PIN_STEERING, PWM_RANGE)
    throttle.set_PWM_range(PIN_THROTTLE, PWM_RANGE)
        
    throttle.set_PWM_dutycycle(PIN_THROTTLE, 0)
    time.sleep(2)
    
    steering.set_PWM_frequency(PIN_STEERING, PWM_FREQ)
    throttle.set_PWM_frequency(PIN_THROTTLE, PWM_FREQ)

    steering.set_PWM_dutycycle(PIN_STEERING, PWM_STEERING_NEUTRAL * PWM_FACTOR)

    print ("Steering PWM frequency is set to", steering.get_PWM_frequency(PIN_STEERING), "Hz.")
    print ("Throttle PWM frequency is set to", throttle.get_PWM_frequency(PIN_THROTTLE), "Hz.")
    
    steering.set_PWM_dutycycle(PIN_STEERING, PWM_STEERING_NEUTRAL * PWM_FACTOR )
    throttle.set_PWM_dutycycle(PIN_THROTTLE, PWM_THROTTLE_NEUTRAL * PWM_FACTOR )
    time.sleep(0.5)
    print ("GPIO initialization ended.")
    
def read_sensor(name):
    
    if name == 'right':
        PIN_TRIGGER = PIN_TRIG_RIGHT
        PIN_ECHO    = PIN_ECHO_RIGHT
        #print("Reading sensor (RIGHT)")
    elif name == 'front':
        PIN_TRIGGER = PIN_TRIG_FRONT
        PIN_ECHO    = PIN_ECHO_FRONT
        #print("Reading sensor (FRONT)")
    elif name == 'back':
        PIN_TRIGGER = PIN_TRIG_BACK
        PIN_ECHO    = PIN_ECHO_BACK
        #print("Reading sensor (BACK)")
    else:
        print("ERROR in reading sensor (passing arg)")
    
    
    read_start_time = time.time()

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    #print("Waiting for sensor to settle")

   # time.sleep(2)

    #print("Calculating distance")

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
        global pulse_start_time
        pulse_start_time = time.time()
        if pulse_start_time - read_start_time > 0.1:
            return -1
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()
        if pulse_end_time - read_start_time > 0.1:
            return -1

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    #print("Distance:",distance,"cm")
    #print("Read time:",(time.time() - read_start_time)*1000,"ms")
    #time.sleep(0.01)
   
    return distance
       

def steerLeft():
    steering.set_PWM_dutycycle(PIN_STEERING, PWM_STEERING_LEFT * PWM_FACTOR)

def steerRight():
    steering.set_PWM_dutycycle(PIN_STEERING, PWM_STEERING_RIGHT * PWM_FACTOR)

def steerNeutral():
    steering.set_PWM_dutycycle(PIN_STEERING, PWM_STEERING_NEUTRAL * PWM_FACTOR)


def moveForward():
    steering.set_PWM_dutycycle(PIN_THROTTLE, PWM_THROTTLE_FWD * PWM_FACTOR)

def moveBackward():
    steering.set_PWM_dutycycle(PIN_THROTTLE, PWM_THROTTLE_REV * PWM_FACTOR)

def moveNeutral():
    steering.set_PWM_dutycycle(PIN_THROTTLE, PWM_THROTTLE_NEUTRAL * PWM_FACTOR)

def moveBrake(forward):
    time_to_brake = 0.2
    if forward:
        moveBackward()
    else:
        moveForward()
    time.sleep(time_to_brake)
    moveNeutral()
   
def testSteering():
    print ("Steering Test started")
    print ("Steering: NEUTRAL")
    steerNeutral()
    time.sleep(1)
    
    print ("Steering: FULL RIGHT")
    steerRight()
    time.sleep(1)
    
    print ("Steering: NEUTRAL")
    steerNeutral()
    time.sleep(1)
    
    print ("Steering: FULL LEFT")
    steerLeft()
    time.sleep(1)
    
    print ("Steering: NEUTRAL")
    steerNeutral()
    time.sleep(1)
    
    print ("Steering Test ended")

def testThrottle():
    
    print ("Throttle Test started")
    moveForward()
    time.sleep(0.2)
    moveNeutral()
    time.sleep(0.2)

    moveBackward()
    time.sleep(0.2)
    moveNeutral()
    print ("Throttle Test ended")