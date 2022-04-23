import RPi.GPIO as GPIO
import time
import argparse
from rpi_pins import motorPins as mPins

class MotorDriver(object):
  speedRight = 0
  speedLeft = 0


  def _initMotorPins(self):
    """Initializing Pins used for the motor.
    IN pins are logic GPIO.OUT values, used for steering the direction.
    EN pins are used for initializing the speed of the motors by modulating the PWM signal.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(IO.BCM)

    #IN pins
    GPIO.setup(mPins.MOTOR_LEFT_IN1, GPIO.OUT)
    GPIO.setup(mPins.MOTOR_LEFT_IN2, GPIO.OUT)
    GPIO.setup(mPins.MOTOR_RIGHT_IN1, GPIO.OUT)
    GPIO.setup(mPins.MOTOR_RIGHT_IN2, GPIO.OUT)

    #EN pins
    self.speedRight = GPIO.PWM(mPins.MOTOR_RIGHT_EN, 1000)
    self.speedLeft = GPIO.PWM(mPins.MOTOR_LEFT_EN, 1000)

    #default values - stand still
    GPIO.output(mPins.MOTOR_LEFT_IN1, GPIO.LOW)
    GPIO.output(mPins.MOTOR_LEFT_IN2, GPIO.LOW)
    GPIO.output(mPins.MOTOR_RIGHT_IN1, GPIO.LOW)
    GPIO.output(mPins.MOTOR_RIGHT_IN2, GPIO.LOW)
    self.speedRight.start(0)
    self.speedLeft.start(0)


  def _goForward(self):
    mPins.MOTOR_LEFT_IN1(GPIO.HIGH)
    mPins.MOTOR_LEFT_IN2(GPIO.LOW)
    mPins.MOTOR_RIGHT_IN1(GPIO.HIGH)
    mPins.MOTOR_RIGHT_IN2(GPIO.LOW)


  def _goReverse(self):
    mPins.MOTOR_LEFT_IN1(GPIO.LOW)
    mPins.MOTOR_LEFT_IN2(GPIO.HIGH)
    mPins.MOTOR_RIGHT_IN1(GPIO.LOW)
    mPins.MOTOR_RIGHT_IN2(GPIO.HIGH)


  def _goRight(self):
    mPins.MOTOR_LEFT_IN1(GPIO.HIGH)
    mPins.MOTOR_LEFT_IN2(GPIO.LOW)
    mPins.MOTOR_RIGHT_IN1(GPIO.LOW)
    mPins.MOTOR_RIGHT_IN2(GPIO.LOW)


  def _goLeft(self):
    mPins.MOTOR_LEFT_IN1(GPIO.LOW)
    mPins.MOTOR_LEFT_IN2(GPIO.LOW)
    mPins.MOTOR_RIGHT_IN1(GPIO.HIGH)
    mPins.MOTOR_RIGHT_IN2(GPIO.LOW)


  def _rampSpeed(self, speed = 100):
    """Method ramping up speed to avoid loss of control

    Args:
        speed (int): PWM Duty Cycle, from 0 do 100%
    """
    x = 0
    while(x <= speed):
      self.speedRight.ChangeDutyCycle(x)
      self.speedLeft.ChangeDutyCycle(x)
      x += 2
      time.sleep(0.01)


  def goDirection(self, direction):
    self._initMotorPins()
    #forward
    if(direction == "forward"):
      self._goForward()
      self._rampSpeed()
    #reverse
    elif(direction == "reverse"):
      self._goReverse()
      self._rampSpeed()
    #left
    elif(direction == "left"):
      self._goLeft()
      self._rampSpeed(70)
    #right
    elif(direction == "right"):
      self._goRight()
      self._rampSpeed(70)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('direction')
  args = parser.parse_args()
  motorDriver = MotorDriver()
  motorDriver.goDirection(args.direction)

if __name__ == "__main__":
  main()