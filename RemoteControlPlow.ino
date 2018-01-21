
/* This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. */

#include <Servo.h>

//User configuration:
int percent = 0;  //between -100 and 100, indicates how fast the motor 
      //will be moving when the arduino boots
int pins[] = {5, 6}; //the signal output pins (as many as you'd like)
int inputPins[] = {2,3};
volatile int pwm_val_left = 0;
volatile int prev_time_left = 0;
volatile int pwm_val_right = 0;
volatile int prev_time_right = 0;
int enablePin12 = 0;
const int arraySize = sizeof(pins)/sizeof(int);
const int inputSize = sizeof(pins)/sizeof(int);
Servo controllers[arraySize];

void setup() {
  Serial.begin(9600);
  Serial.println("you called, master?\n");
  for (int i=0; i<arraySize; i++)
    controllers[i].attach(pins[i]); //associate the object to a pin
  attachInterrupt(INT0,risingRight, RISING);
  attachInterrupt(INT1,risingLeft, RISING);
 // attachInterrupt(digitalPinToInterrupt(18),risingEnable, RISING);
  delay(1000);
  Serial.println("type in a percent, and I will output your PWM.\n");
  
}

void risingRight(){
  attachInterrupt(INT0,fallingRight,FALLING);
  prev_time_right = micros();
}
void risingLeft(){
  attachInterrupt(INT1,fallingLeft,FALLING);
  prev_time_left = micros();
}
void fallingRight(){
  attachInterrupt(INT0,risingRight, RISING);
  pwm_val_right = micros()-prev_time_right;
}
void fallingLeft(){
  attachInterrupt(INT1,risingLeft, RISING);
  pwm_val_left = micros()-prev_time_left;
}

int leftPWMin = 0;
int rightPWMin = 0;
bool enableMotors = true;

void loop() {

  //if(abs(pwm_val_enable-1500)>100){
    controllers[0].writeMicroseconds(pwm_val_right);
    controllers[1].writeMicroseconds(pwm_val_left);
    //enableMotors = false;
    
  
  
      //Serial.println(pwm_val_enable);  
}

