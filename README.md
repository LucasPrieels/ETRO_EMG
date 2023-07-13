# ETRO_EMG
Code to use the ADC of a PSoC6 device and transmit the digitized values to a computer via UART, as part of an EMG sensor

The TopDesign.cysch and main_cm4.c are the files to use in the PSoC Creator software to program the PSoC6 device. The exact device used for the prototype is a CY8CPROTO-063-BLE. It reads a value from the ADC every 1ms then sends it along with the current time in ms via UART to a host computer.

The computer_script.py code is a Python script to run on the host computer to receive and plot data from the PSoC to which it is connected. The UART port name must be set in the "port" variable in the first lines of the script. The number of points to plot can be set with the POINTS_PLOT variable. The Fourier transform of the received signal can be plotted along the time domain if the PLOT_FFT variable is set to True. The Baud rate should not be changed unless it is changed accordingly on the PSoC device.

Please refer to the report associated to this repository for more details.
