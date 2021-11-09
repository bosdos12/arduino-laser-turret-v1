// Imports;
#include <Servo.h>




// Global Data;

// Servo Initializations;
Servo SG995_XAXISSERVO; // MG995 12KG HIGH SPEED METAL GEAR SERVO; 
Servo SG90_YAXISSERVO;  // SG90 1.5KG MICRO SERVO;

// Servo Global Positions;
int XXX_POSITION = 0;
int YYY_POSITION = 0;

// THE LED INDICATOR FOR KNOWING SERIAL COMMUNICATION MODE IS TURNED ON;
int SERIALMODEINDICATORLED = A2;


// Controls;
int LEFT                = 3;
int RIGHT               = 2;
int UP                  = 4;
int DOWN                = 5;
int SETSPEEDOFTURRETPIN = 6;
int SWITCHOFSERIALORDIRECTCONTROL = A3;

// Setting up the LED PIN names for the pins for easier coding;
int CENTERPIN      = 7;
int TOPLEFTPIN     = 8;
int TOPPIN         = 9;
int TOPRIGHTPIN    = 10;
int BOTTOMLEFTPIN  = 11;
int BOTTOMPIN      = 12;
int BOTTOMRIGHTPIN = 13;

// Servo speed setting;
int GLOBALSERVOSPEED = 1;

// Setting up the number shapes;
int numberShapesArray[10][7] = {
  {TOPLEFTPIN, TOPPIN, TOPRIGHTPIN, BOTTOMLEFTPIN, BOTTOMPIN, BOTTOMRIGHTPIN, 404},
  {TOPRIGHTPIN, BOTTOMRIGHTPIN, 404, 404, 404, 404, 404},
  {TOPPIN, TOPRIGHTPIN, CENTERPIN, BOTTOMLEFTPIN, BOTTOMPIN, 404, 404},
  {TOPPIN, TOPRIGHTPIN, CENTERPIN, BOTTOMPIN, BOTTOMRIGHTPIN, 404, 404},
  {TOPLEFTPIN, CENTERPIN, TOPRIGHTPIN, BOTTOMRIGHTPIN, 404, 404, 404},
  {TOPLEFTPIN, TOPPIN, CENTERPIN, BOTTOMPIN, BOTTOMRIGHTPIN, 404, 404},
  {TOPLEFTPIN, TOPPIN, CENTERPIN, BOTTOMLEFTPIN, BOTTOMPIN, BOTTOMRIGHTPIN, 404},
  {TOPPIN, TOPRIGHTPIN, BOTTOMRIGHTPIN, 404, 404, 404, 404},
  {TOPLEFTPIN, TOPPIN, TOPRIGHTPIN, CENTERPIN, BOTTOMLEFTPIN, BOTTOMPIN, BOTTOMRIGHTPIN},
  {TOPLEFTPIN, TOPPIN, TOPRIGHTPIN, CENTERPIN, BOTTOMPIN, BOTTOMRIGHTPIN, 404}
};

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
// Functions;


// Controls;

// X-AXIS movement;
void XXX_AxisMovemet (int leftOrRightMovement) {
  // If leftOrRightMovementnSide is 1, turning right, 
  // otherwise if leftOrRightMovement is 0 turning left;
  if (leftOrRightMovement) {
    // Right;
    if (XXX_POSITION < 179) {
      XXX_POSITION += 1;
    };
  } else {
    // Left;
    if (XXX_POSITION > 0) {
      XXX_POSITION -= 1;
    }
  };
  // Position Updated, spinning the servo now;
  SG995_XAXISSERVO.write(XXX_POSITION);
  
};


// Y-AXIS movemet;
void YYY_AxisMovement (int upOrDownMovement) {
  // If upOrDownMovement is 1, turning up, 
  // otherwise if upOrDownMovement is 0 turning down;
  if (upOrDownMovement) {
    // Up;
    if (YYY_POSITION < 179) {
      YYY_POSITION += 1;
    };
  } else {
    // Down;
    if (YYY_POSITION > 0) {
      YYY_POSITION -= 1;
    }
  };
  // Position Updated, spinning the servo now;
  SG90_YAXISSERVO.write(YYY_POSITION);
};


// Servo Speed Controls;
void changeServoSpeedF() {
    // Clearing the screen;
    digitalWrite(CENTERPIN, LOW);
    digitalWrite(TOPLEFTPIN, LOW);
    digitalWrite(TOPPIN, LOW);
    digitalWrite(TOPRIGHTPIN, LOW);
    digitalWrite(BOTTOMLEFTPIN, LOW);
    digitalWrite(BOTTOMPIN, LOW);
    digitalWrite(BOTTOMRIGHTPIN, LOW);

    // Writing the new value;
    if (GLOBALSERVOSPEED <= 9) {
      GLOBALSERVOSPEED++;
    } else {
      GLOBALSERVOSPEED=1;
    };

    for (int x = 0; x < 7; x++) {
      if (numberShapesArray[GLOBALSERVOSPEED][x] != 404) {
        digitalWrite(numberShapesArray[GLOBALSERVOSPEED][x], HIGH);
      }
    }

    // Making a small delay to prevent control craziness;
    delay(100);
};



void setup() {
  // Starting the Serial;
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Setting the pins modes;
  pinMode(LEFT,  INPUT);
  pinMode(RIGHT, INPUT);
  pinMode(UP,    INPUT);
  pinMode(DOWN,  INPUT);
  // Turret Speed
  pinMode(SETSPEEDOFTURRETPIN, INPUT);
  // Serial or direct control switch;
  pinMode(SWITCHOFSERIALORDIRECTCONTROL, INPUT);

  // REVERSE-LOGIC to prevent floating input;
  digitalWrite(LEFT,  HIGH);
  digitalWrite(RIGHT, HIGH);
  digitalWrite(UP,    HIGH);
  digitalWrite(DOWN,  HIGH);
  digitalWrite(SETSPEEDOFTURRETPIN, HIGH);
  digitalWrite(SWITCHOFSERIALORDIRECTCONTROL, HIGH);

  // Setting the LED PIN's to output;
  pinMode(CENTERPIN, OUTPUT);
  pinMode(TOPLEFTPIN, OUTPUT);
  pinMode(TOPPIN, OUTPUT);
  pinMode(TOPRIGHTPIN, OUTPUT);
  pinMode(BOTTOMLEFTPIN, OUTPUT);
  pinMode(BOTTOMPIN, OUTPUT);
  pinMode(BOTTOMRIGHTPIN, OUTPUT);

  // Servo PWM Connections;
  SG995_XAXISSERVO.attach(A5);
  SG90_YAXISSERVO.attach(A4);

  // Serial mode indicator LED;
  pinMode(SERIALMODEINDICATORLED, OUTPUT);


  // Displaying the one on the screen at start;
  digitalWrite(TOPRIGHTPIN,  HIGH);
  digitalWrite(BOTTOMRIGHTPIN, HIGH);
};

void SerialCommunicationF() {
  // THIS FUNCTION IS CALLED ONLY IF THE SERIALCOMMUNICATIONF SWITCH IS TURNED ON;
  // IN THIS MODE THE TURRET DOESNT WORK BY DIRECT CONTROLS AND ONLY WORKS BY DESKTOP CONTROL;

  int DesktopReceivedSerialmessage = 0;
  // PC-ARDUINO serial communication;
  if (Serial.available()) {
    
    int DesktopReceivedSerialmessage = Serial.readString().toInt();

    // COMUNICATION CODES:
    // 1 - Move Turret Left;
    // 2 - Move Turret Right;
    // 3 - Move Turret Top;
    // 4 - Move Turret Bottom;
    if (DesktopReceivedSerialmessage == 1) {
      XXX_AxisMovemet(0);  // Left;
    } else if (DesktopReceivedSerialmessage == 2) {
      XXX_AxisMovemet(1);  // Right;
    } else if (DesktopReceivedSerialmessage == 3) {
      YYY_AxisMovement(1); // Too;
    } else if (DesktopReceivedSerialmessage == 4) {
      YYY_AxisMovement(0); // Bottom;
    }

      delay(100); 
  }
}


void loop() {

  // Checking if serial communication is desired;
  if (!digitalRead(SWITCHOFSERIALORDIRECTCONTROL)) {
    // Serial communication desired;
    Serial.write("HAHAHAHA");
    digitalWrite(SERIALMODEINDICATORLED, HIGH); // Serial info led;
    SerialCommunicationF(); // Serial control functions;
  } else {
    // Serial communication NOT desired;
    digitalWrite(SERIALMODEINDICATORLED, LOW); // Serial info led;
    
    // Control Movements;
    // Running an IF-CHECK on each axis to allow movements on both X and Y at the same input loop check;
    if (!digitalRead(LEFT)) {
      XXX_AxisMovemet(0);
    };
  
    if (!digitalRead(RIGHT)) {
      XXX_AxisMovemet(1);
    };

    if (!digitalRead(UP)) {
      YYY_AxisMovement(1);
    };

    if (!digitalRead(DOWN)) {
      YYY_AxisMovement(0);
    };

    // Servo speed adjustment;
    if (!digitalRead(SETSPEEDOFTURRETPIN)) {
      changeServoSpeedF();
    }; 

    // Movement Delay;
    delay(100-(GLOBALSERVOSPEED*10));  
  }
};
