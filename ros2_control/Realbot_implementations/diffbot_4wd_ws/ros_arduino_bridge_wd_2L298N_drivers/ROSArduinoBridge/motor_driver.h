/***************************************************************
   Motor driver function definitions - by James Nugen
   *************************************************************/

#ifdef L298_MOTOR_DRIVER
  #define BACK_RIGHT_MOTOR_BACKWARD 5
  #define BACK_LEFT_MOTOR_BACKWARD  6
  #define BACK_RIGHT_MOTOR_FORWARD  9
  #define BACK_LEFT_MOTOR_FORWARD   10
  #define BACK_RIGHT_MOTOR_ENABLE 12
  #define BACK_LEFT_MOTOR_ENABLE 13

  #define FRONT_RIGHT_MOTOR_BACKWARD 3
  #define FRONT_LEFT_MOTOR_BACKWARD  4
  #define FRONT_RIGHT_MOTOR_FORWARD  7
  #define FRONT_LEFT_MOTOR_FORWARD   8
  #define FRONT_RIGHT_MOTOR_ENABLE 12
  #define FRONT_LEFT_MOTOR_ENABLE 13

#endif

void initMotorController();
void setMotorSpeed(int i, int spd);
void setMotorSpeeds(int leftSpeed, int rightSpeed);
