# PyIMU_3Dvisualizer
IMU 3D visualizer with Python, OpenGL and NPX 9-DOF Breakout Board - FXOS8700 + FXAS21002 (originally MPU6050)

Note: In the original version the "Yaw" mode was not implemented yet.
It has now been modified to include Yaw in the visualizer and receive the data string (yaw, pitch, roll) from the serial already filtered out.

In this example the 9-DOF- FXOS8700 + FXAS21002 Breakout Board is used, but as long as you send a serial string with the following format this program should always work:

"Orientation: 347.66, 1.26, 1.38 (YAW, PITCH, ROLL)"

_Simulador 3D para acelerometro/gyroscopio MPU6050_
![](https://drive.google.com/uc?export=view&id=1g5SrGnZ_wfWsqmL7pKUehwe6HWRJV3sw)

![animacion_IMU_3](https://user-images.githubusercontent.com/41245794/182449319-c480960d-4ae6-4c68-b2c5-339afb2b033d.gif)

## Starting 🚀

### Pre-requisites 📋

* Python 3
* Tkinter
* pySerial
* pyOpenGL

* IMU unit (NPX 9-DOF Breakout Board - FXOS8700 + FXAS21002 used in this example, similar should work)
* Microcontroller (ESP32 used in my case, similar should work)
* USB-Serial Converter (in case the microcontroller doesn't have one on-board included)


## Wiki 📖

Tutorials followed for the setup of the 

"calibrated_orientation" sketch from Adafruit_AHRS library

Original article: https://learn.adafruit.com/how-to-fuse-motion-sensor-data-into-ahrs-orientation-euler-quaternions/overview

Original Visualizer: https://learn.adafruit.com/how-to-fuse-motion-sensor-data-into-ahrs-orientation-euler-quaternions/webserial-visualizer

Magnetic calibration performed with https://github.com/PaulStoffregen/MotionCal -> https://www.pjrc.com/store/prop_shield.html

---
Deprecated (original wiki):

Puedes ver más acerca del proyecto en el video [demo](https://www.youtube.com/watch?v=vh91z3-3ncE)

Para comenzar es necesario contar con el microcontrolador encargado adquirir los datos del
MPU6050 y enviarlos de forma serial.

Aqui hay algunos ejemplos de como hacerlo utilizando:
* [Microcip PIC16F1709 MCU](https://github.com/MA-Lugo/PIC16F1709_MPU6050_ex)
* [STM32F1 MCU](https://github.com/MA-Lugo/STM32F1_MPU6050_lib/blob/main/Core/Src/main.c)

### Formato de la trama de datos:
En la siguiente imagen se muestra el formato de la trama de datos necesarios.

![](https://drive.google.com/uc?export=view&id=1YwkYYE5qgLod-2wsBejAZDGvy2fpD29x)

## Pruebas 🛠️

![](https://drive.google.com/uc?export=view&id=1FfHM9EbRliaT2iBzzAqZF8uXnvBeMvwJ)


## Autors ✒️

Original author:
* **Mario A. Lugo**  [MA-Lugo](https://github.com/MA-Lugo)


Contributors:
* **Marco Farias**  [marcofariasmx](https://github.com/marcofariasmx)

