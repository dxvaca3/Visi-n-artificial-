#include <Servo.h>

Servo servoX;
Servo servoY;

const int pinX = 9;
const int pinY = 10;

const int pulsoMin = 580;
const int pulsoMax = 2500;

char buffer[16];
int idx = 0;

int anguloX = 90;
int anguloY = 90;

void setup() {
  Serial.begin(9600);

  servoX.attach(pinX, pulsoMin, pulsoMax);
  servoY.attach(pinY, pulsoMin, pulsoMax);

  servoX.write(anguloX);
  servoY.write(anguloY);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      buffer[idx] = '\0';
      procesarComando(buffer);
      idx = 0;
    } else if (idx < 15) {
      buffer[idx++] = c;
    }
  }
}

void procesarComando(const char* cmd) {

  // ===== EJE X =====
  if      (!strcmp(cmd, "izq1"))  moverX(0);
  else if (!strcmp(cmd, "izq2"))  moverX(30);
  else if (!strcmp(cmd, "izq3"))  moverX(60);
  else if (!strcmp(cmd, "ctrX"))  moverX(90);
  else if (!strcmp(cmd, "der3"))  moverX(120);
  else if (!strcmp(cmd, "der2"))  moverX(150);
  else if (!strcmp(cmd, "der1"))  moverX(180);

  // ===== EJE Y =====
  else if (!strcmp(cmd, "up1"))    moverY(0);
  else if (!strcmp(cmd, "up2"))    moverY(30);
  else if (!strcmp(cmd, "up3"))    moverY(60);
  else if (!strcmp(cmd, "ctrY"))   moverY(90);
  else if (!strcmp(cmd, "down3"))  moverY(120);
  else if (!strcmp(cmd, "down2"))  moverY(150);
  else if (!strcmp(cmd, "down1"))  moverY(180);
}

void moverX(int nuevoAngulo) {
  if (nuevoAngulo != anguloX) {
    anguloX = nuevoAngulo;
    servoX.write(anguloX);
  }
}

void moverY(int nuevoAngulo) {
  if (nuevoAngulo != anguloY) {
    anguloY = nuevoAngulo;
    servoY.write(anguloY);
  }
}
