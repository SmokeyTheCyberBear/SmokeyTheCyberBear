// #include <SPI.h>
// #include <LoRa.h>

// void setup() {
//   Serial.begin(115200);
//   while (!Serial);

//   //Serial.println("LoRa Gateway");

//   if (!LoRa.begin(868E6)) {
//     //Serial.println("Starting LoRa failed!");
//     while (1);
//   }
// }
// int counter = 0;
// void loop() 

// {
  
//   String teststr;
//   int incomingByte = 0;
//   if (Serial.available() > 0)
//   {
//     // read the incoming byte:
//     teststr = Serial.readString();
//     teststr[teststr.length()] = '\n';
//     //Serial.print("Sending packet: ");
//     LoRa.beginPacket();
//     LoRa.print(teststr);
//     LoRa.endPacket();
//     // say what you got:
//     //Serial.print("I received: ");
//     //Serial.println(teststr);
//     counter++;

//     delay(1000);
//   }
//   // try to parse packet
//   int packetSize = LoRa.parsePacket();
//   if (packetSize) 
//   {
//     // received a packet
//     //Serial.print("Received packet '");

//     // read packet
//     while (LoRa.available()) 
//     {
//       Serial.println((char)LoRa.read());
//     }
//   }
//   delay(100);
// }
