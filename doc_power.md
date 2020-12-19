# Xilinx Power Advantage Tool Documentation

- Date 2020.10.09
  
## Installation

Power Advantage Tool Official User Guide: [link](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841681/Zynq+UltraScale+MPSoC+Power+Advantage+Tool+part+1+-+Introduction+to+the+Power+Advantage+Tool)

The official guide is somewhat miss-leading. Follow this documentation instead.

### Note

Xilinx Power Advantage Tool is a power data recording software provided by Xilinx.
You need a Windows 7/10 PC to run this software. Power data is read from MSP430 controller and is transported to PC through a UART serial port on the ZCU102 board.

The GUI does not function properly, but power data is recorded into `datalog.csv`

1. Prepare SD Card

The boot SD card's Linux kernel must have `pl-power app`. Otherwise it would not be able to retrieve data from MSP430 controllder. The DPU SD card image provided by Xilinx can be used with this tool.

2. Download **2019.1 ZCU102** version of Xilinx Power Advantage Tool. 

Decompress this folder to Disk C root directory according to this [guide](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842495/Zynq+UltraScale+MPSoC+Power+Advantage+Tool+part+2+-+Installing+the+Pre-Built+Power+Advantage+Tool). Also copy the demo folder to Disk C's root directory.

3. We have tested that setting static IP address is not necessary.

4. Install the following tools

    -	Open the `CP210x_VCP_Windows` folder, and install `CP210xVCPInstaller_x64.exe` USB to UART driver from Silicon Labs.
    - 	Install `CDM v2.12.10 WHQL Certified.exe` USB to UART driver from FTDI if included in the tools directory.
    - 	Install `AutoHotkey112203_Install.exe`
    - 	Install `teraterm-4.87.exe` (Tera Term)

## Connect board with PC

The software reads data from serial port. We connect the UART port **J83** to PC's USB port. 

![](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236514/doc/image001_zstjbv.jpg)

The official document indicates that we also need to connect Ethernet port to PC. However, this is not necessary according to our experiment. The Ethernet connection in the above image is to connect the board with internal network.

Next we test if the connection is successful.

Start the software on PC. Choose `Select > About`. If the `MSP430 version` shows None, the software failed to retrieve MSP430 version number. In this case, we verify if the connection is unsuccessful.
![Verify MSP430 Version](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236518/doc/image002_noipal.png)

Exit the software. We use MobaXTerm to start serial port sessions.  

Set the parameters exactly as the following image:

![](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236513/doc/image003_v7m2uu.png)

We see that there are 4 ports. One of them is a connection to the Linux system (COM10 in this case). Another one of them does not have any output when opened, but the cursor moves when you type, this port is connected to MSP430 (COM11 in this case). The other two ports do not have response when opened.


We connect to COM11, and type `@ver` to see if there are any output.

The following result means that the MSP430 version is correct and the connection is successful.
![](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236513/doc/image004_qv3ykm.png)

In this case, the connection is established, but the power advantage tool software cannot get MSP430 version number. Observing the log at `Log：C:\\ZynqUS_Demos\\ZynqusPowerToolDeployment\\log `:
![](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236516/doc/image005_r7bryb.png)


When the software is launched, the return value of `@ver` command was not successfully processed. This could be a bug of this software.



### Solution 

After numerous trail-and-error, we found that we must keep the connection between the board and PC, and also make sure the software is open. Then, we reboot the board while keeping the connection alive and sofware open. Then we see that the About page has the correct MSP430 version:
![](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236515/doc/image006_gqlviy.png)

However, the System Monitor page still shows no data. Later we verified that this is the bug of GUI software. The data is actually stored.
![](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236518/doc/image007_ewpolc.png)

## Result path

The power readings are stored at `C:\\ZynqUS_Demos\\ZynqusPowerToolDeployment\\datalog.csv`
![](https://res.cloudinary.com/dxzx2bxch/image/upload/v1602236516/doc/image008_z6xo7l.png)

These values are the power readings from MSP430 controller. The unit is `1e-6` W.