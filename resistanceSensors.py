import numpy as np
import adcUtil as adc
import time
import pandas as pd

class ResistanceSensors():
    def __init__(self, dev, n = 2, vin = 3.3, r2 = 10.0):
        self.dev = dev
        self.n = n
        self.vin = vin
        self.r2 = r2 
        self.tref = 0
        self.data = np.zeros( [ 0, 1 + self.n ], dtype=float) # cols = time + accelerometer amount
    
    def calibrate(self, tref):
        self.tref = tref
        
    def table(self):
        return pd.DataFrame(data=self.data)
        
    def record(self):
        self.data.resize((len(self.data) + 1, 1 + self.n))
        row = self.data[-1]
        row[0] = time.time() - self.tref
        for i in range(self.n):
            vou = adc.readADC(channel=i, device=self.dev)
            row[i + 1] = vou
    
    def save(self, filename):
         np.save(filename, self.data)