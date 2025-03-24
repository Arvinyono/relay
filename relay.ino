// Pin Definitions
const int buttonPin = 2;    // Pin untuk the push button
const int relayPin = 3;     // Pin untuk the relay control

// Variables
bool buttonState = LOW;     // kondisi awal button
bool lastButtonState = LOW; // 

void setup() {
  // Initialize Serial communication for DB9 (9600 baud rate is common for barcode printers)
  Serial.begin(9600);

  // Configure pin modes
  pinMode(buttonPin, INPUT);  // Push button di tekan
  pinMode(relayPin, OUTPUT);  // Relay open

  // pastikan relay normaly off
  digitalWrite(relayPin, LOW);
}

void loop() {
  // Read the current state of the button
  buttonState = digitalRead(buttonPin);

  // Periksa apakah tombol baru saja ditekan 
  if (buttonState == HIGH && lastButtonState == LOW) {
    // 
    delay(50);

    // konfirmasi button setelah di tekan
    if (digitalRead(buttonPin) == HIGH) {
      // Step 1: Send barcode data to the printer via Serial
      printBarcode();

      // Step 2: Turn on the relay
      digitalWrite(relayPin, HIGH);
      delay(500); //relay menyala dalam 1 detik

      // Step 3: Turn off  relay
      digitalWrite(relayPin, LOW);
    }
  }

  // Update the last button state
  lastButtonState = buttonState;
}

// Function to send barcode data to the printer
void printBarcode() {
  // contoh ESC/POS command untuk print Code 128 barcode
  String barcodeData = "123456789012";

  // Send alignment command (center align)
  Serial.write(0x1B); // ESC
  Serial.write(0x61); // 'a'
  Serial.write(0x01); // Center align

  // Send barcode command (GS k m d1...dk NUL)
  Serial.write(0x1D); // GS
  Serial.write(0x6B); // 'k'
  Serial.write(0x49); // Barcode type (Code 128)
  Serial.print(barcodeData); // Barcode data
  Serial.write(0x00); // Null terminator
}
