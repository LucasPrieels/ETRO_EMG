import serial
import matplotlib.pyplot as plt
import scipy.fftpack
import time
import numpy as np

PLOT_FFT = False
POINTS_PLOT = 1500 # Number of points to show on the plot at the same time

def get_time_ms():
	return time.time()*1000

# Configure the serial port
port = "COM3"  # Replace with the actual port name
baudrate = 115200  # Replace with the baud rate used in your application

# Open the serial port
ser = serial.Serial(port, baudrate)

# Create lists to store the data
t_data = []
t_received = []
x_data = []
y_data = []
e_data = []

# Set up the plot
plt.ion()  # Enable interactive mode
axs = 0
if PLOT_FFT:
    fig, axs = plt.subplots(2)
    fig.tight_layout(pad=3.0)
    ax = axs[0]
    axs[0].title.set_text("Evolution of the EMG signal")
    axs[1].title.set_text("Fourier transform of the EMG signal")
    axs[0].grid(True, which="both")
    axs[1].grid(True, which="both")
    axs[1].set_yscale('log')
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Digitized voltage")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel("Amplitude (log)")
else:
    fig, ax = plt.subplots()
    ax.title.set_text("Evolution of the EMG signal")
    ax.grid(True, which="both")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Digitized voltage")
line, = ax.plot(t_data, x_data)
if PLOT_FFT:
    lineFFT, = axs[1].plot(t_data, x_data)
t = 0

last_x = [0]*4
initial_time = 0

# Continuously read and plot data
while True:
    try:
        # Read a line of data from the serial port
        try:
            l = ser.readline().decode().strip().split()
            if len(l) == 2:
                if t == 0:
                    initial_time = int(l[0])/1000
                t_received.append(int(l[0])/1000-initial_time)
                x_data.append(int(l[1]))
            else:
                print(l)
                continue
        except:
            try:
                print(l)
            except:
                print("Error")
            continue        

        # Append the data to the lists
        t += 1
        if PLOT_FFT:
            t_data.append(t)
        else:
            t_data.append(t)

        if t % 200 == 0:

            # Update the plot
            t_axis = t_received#np.linspace(0.0, time_t, len(t_data))
            line.set_data(t_axis[-POINTS_PLOT :-1], x_data[-POINTS_PLOT:-1])
            ax.relim()  # Recalculate the data limits
            ax.autoscale_view()  # Autoscale the plot
            if PLOT_FFT:
                f = np.linspace(0.0, 1.0/(t_axis[-1]/len(t_axis)), min(POINTS_PLOT, len(t_axis))-1)
                fft = np.abs(scipy.fftpack.fft(x_data[-min(POINTS_PLOT, len(t_axis)):-1]))
                clean_fft = [fft[a] for a in range(len(fft))]# if a%2==0] # Keep only one value out of 2 to clean the curve
                clean_f = [f[a] for a in range(len(f))]# if a%2==0]
                lineFFT.set_data(clean_f[:len(clean_f)//2], np.log(clean_fft[:len(clean_fft)//2]))

                axs[1].relim()
                axs[1].autoscale_view()
             
            fig.canvas.draw()  # Redraw the plot
            # Pause to allow time for the plot to update
            plt.pause(0.001)
    
    except KeyboardInterrupt:
        # Stop reading and plotting data if Ctrl+C is pressed
        break

# Close the serial port
ser.close()

# Display the plot
plt.ioff()
plt.show()