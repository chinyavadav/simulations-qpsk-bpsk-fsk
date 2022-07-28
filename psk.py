import matplotlib.pyplot as plot
import numpy as np
import sys

class BaseClass:
	def __init__(self, file="image", freq=10):
		self.file = file
		self.m = 0.2
		self.freq = freq
		self.freqs = 2

		self.Fs = 150.0  # sampling rate
		self.Ts = 1.0/self.Fs # sampling interval
		self.t = np.arange(0, 2, self.Ts)
	
	def calculate_signal_properties(self, y):
		self.n = len(y) # length of the signal
		self.k = np.arange(self.n)
		self.T = self.n/self.Fs
		self.frq = self.k/self.T # two sides frequency range
		self.frq = self.frq[range(self.n//2)] # one side frequency range
		self.Y = np.fft.fft(y)/self.n # fft computing and normalization
		self.Y = self.Y[range(self.n//2)]
	
	def plot(self, carrier, y, data):
		fig, myplot = plot.subplots(4, 1)

		xs = np.repeat(range(len(data)), 2)
		ys = np.repeat(data, 2)
		xs = xs[1:]
		ys = ys[:-1]
		xs = list(xs)
		ys = list(ys)
		xs.append(xs[-1]+1)
		ys.append(ys[-1])
		myplot[0].plot(xs, ys, color='dodgerblue')
		myplot[0].set_title("Data")

		myplot[1].plot(self.t, carrier)
		myplot[1].set_xlabel('Time')
		myplot[1].set_ylabel('Amplitude')
		myplot[1].set_title("Carrier wave")

		myplot[2].plot(self.t, y)
		myplot[2].set_xlabel('Time')
		myplot[2].set_ylabel('Amplitude')
		myplot[2].set_title("Modulated signal")

		myplot[3].plot(self.frq, abs(self.Y),'r') # plotting the spectrum
		myplot[3].set_xlabel('Freq (Hz)')
		myplot[3].set_ylabel('|Y(freq)|')
		myplot[3].set_title("Frequency domain")	
		

		plot.tight_layout()
		plot.savefig(self.file)
		plot.show()


class Ask(BaseClass):
	def __init__(self, freq=10):
		super().__init__("ask", freq)
		self.data = np.array([1, 0, 1, 1, 0, 1]) # <- Input bit rate
		self.samples_per_bit = 2*self.Fs/self.data.size 
		self.dd = np.repeat(self.data, self.samples_per_bit)
		self.carrier = np.sin(2 * np.pi * self.freq * self.t)
		self.modulated = self.dd*self.carrier
		super().calculate_signal_properties(self.modulated)
		super().plot(self.carrier, self.modulated, self.data)


class Fsk(BaseClass):
	def __init__(self, freq=10):
		super().__init__("fsk", freq)	
		self.data = np.array([5, 5, -5, 5, -5, -5])
		self.samples_per_bit = 2*self.Fs/self.data.size 
		self.dd = np.repeat(self.data, self.samples_per_bit)
		self.carrier = np.sin(2 * np.pi * self.freq * self.t)
		self.modulated = np.sin(2 * np.pi * (self.freq + self.dd) * self.t)
		super().calculate_signal_properties(self.modulated)
		super().plot(self.carrier, self.modulated, self.data)


class Psk(BaseClass):
	def __init__(self, freq=10):
		super().__init__("psk", freq)	
		self.data = np.array([180,180,0,180,0])
		self.samples_per_bit = 2*self.Fs/self.data.size 
		self.dd = np.repeat(self.data, self.samples_per_bit)
		self.modulated = np.sin(2 * np.pi * (self.freq) * self.t+(np.pi*self.dd/180))
		self.carrier = np.sin(2 * np.pi * self.freq * self.t)
		super().calculate_signal_properties(self.modulated)
		super().plot(self.carrier, self.modulated, self.data)
	

if __name__ == "__main__":
	print("\nWORKING...")
	len_argv = len(sys.argv)
	if (len_argv>2):

		type=(sys.argv[1].lower())
		if type in ["ask", "fsk", "psk"]:
			if type == "ask":
				A = Ask(float(sys.argv[2]))
			elif type == "fsk":
				F = Fsk(float(sys.argv[2]))
			else:
				P = Psk(float(sys.argv[2]))			
		else:
			print("We currently do not supprt that modulation")

	else:
		print("⚠️  Usage [ask|fsk|psk] number1")
		print("   number1=frequency, recommended is 10")

	print("...DONE\n")
