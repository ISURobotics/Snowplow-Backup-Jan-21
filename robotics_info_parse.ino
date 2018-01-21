#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Servo.h>

const byte numChars = 32;
char receivedChars[numChars];
char xchars[numChars];
char ychars[numChars];
char zchars[numChars];
char lastchar = 'x';
int x = 0;
int y = 0;
int z = 0;

//wheel encoder variable
volatile float time1 = 0.0;
volatile float time2 = 0.0;
volatile bool has_time1 = false;
volatile float speed;
int forwardSpeed; 
char most_recent_char='s';

float heading = 0;
int directionTolerance = 10;
boolean newData = false;
/*
 * joystick stuff 
 */
//User configuration:
int percent = 0;  //between -100 and 100, indicates how fast the motor 
//will be moving when the arduino boots
int pins[] = {
  5, 6}; //the signal output pins (as many as you'd like)
int inputPins[] = {
  2,3};
volatile int pwm_val_left = 0;
volatile int prev_time_left = 0;
volatile int pwm_val_right = 0;
volatile int prev_time_right = 0;
int enablePin12 = 0;
const int arraySize = sizeof(pins)/sizeof(int);
const int inputSize = sizeof(pins)/sizeof(int);
Servo controllers[arraySize];
Adafruit_BNO055 bno = Adafruit_BNO055(55);
int userControlToggle = 0;

void setup() {
  Serial.begin(9600);

  //motor encoder setup
  speed = 0.0;
  pinMode(18, INPUT);
  attachInterrupt(INT5, get_speed, CHANGE);
  forwardSpeed = 1500;

  for (int i=0; i<arraySize; i++)
    controllers[i].attach(pins[i]); //associate the object to a pin
  //attachInterrupt(2,risingRight, RISING);
  //attachInterrupt(3,risingLeft, RISING);
  //attachInterrupt(digitalPinToInterrupt(18),risingEnable, RISING);
  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    //Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);
  //Serial.println("Hello world");
  bno.setExtCrystalUse(true);
}

void loop() {
  //data receieved from serial
  unsigned char data_received;
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
  heading = euler.x();
  heading = 360.0-heading;
  //  sensors_event_t event;
  //  bno.getEvent(&event);
  //  heading = event.orientation.x;
  Serial.print(heading);
  Serial.print("\n");
  //Serial.flush();
  //right and left power
  int power_left = 90; //dead
  int power_right = 90; //dead
  float setSpeed = 1.25;
  float dif = abs(speed-setSpeed);
  float Kp = 40;
  if(speed>setSpeed){
    forwardSpeed = forwardSpeed-round((dif*Kp));
  }
  else{
    forwardSpeed = forwardSpeed+round((dif*Kp));
  }
  if(forwardSpeed>2000){
    forwardSpeed = 2000;
  }
  if(forwardSpeed<1600){
    forwardSpeed = 1600;
  }



  //if there is a serial byte ready to read then read it
  if(Serial.available() > 0){
    //grab serial data
    data_received = Serial.read();
    //set the most recent received character so the power setting
    //statements will continue to be executed.

    most_recent_char = data_received;

  }
  if(most_recent_char == 's'){
    power_left = 1500;
    power_right = 1500;
  }
  else if(most_recent_char == 'f'){
    power_left = forwardSpeed;
    power_right = forwardSpeed;
  }
  else if (most_recent_char == 'r')
  {
    //power_left = sft;
    //power_right = sbt;
    power_left = forwardSpeed;
    //power_right = 1500-abs(forwardSpeed-1500);
    power_right = 1500 - abs(forwardSpeed - 1500);
  }
  else if (most_recent_char == 'l')
  {
    //power_left = sbt;
    //power_right = sft;
    power_left = 1500 - abs(forwardSpeed - 1500);
    power_right = forwardSpeed;
  }
  //controllers[0].writeMicroseconds(power_right);
  //controllers[1].writeMicroseconds(power_left);

  delay(50);
  controllers[0].writeMicroseconds(power_right);
  controllers[1].writeMicroseconds(power_left);
  //controllers[0].writeMicroseconds(1500);
  //controllers[1].writeMicroseconds(1500);
}

//this function is the ISR for the wheel encoder

void get_speed(){
  if(has_time1 == false && (digitalRead(18) == 0)){
    time1 = millis();
    has_time1 = true;
  }
  else{
    time2 = millis();
    float time_change = (float)(time2 - time1)/1000.0;
    speed = (3.25/time_change) * 0.0254;
    has_time1 = false;
    //Serial.print("s");
    //Serial.println(speed);
    //Serial.println(" m/s");
  }
}





