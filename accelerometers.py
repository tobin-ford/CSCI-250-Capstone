import time                         # Time access and conversion package
import qwiic_i2c                    # I2C bus driver package
import qwiic_tca9548a
import accUtil as acc
import numpy as np
import time
import pandas as pd


class Accelerometers():
    def __init__(self, n = 5):
        self.n = n
        self.data = np.zeros( [ 0, 1 + self.n * 3 ]) # cols = time + accelerometer amount
        self.calibration = np.zeros(1 + self.n * 3)
        self.mux = qwiic_tca9548a.QwiicTCA9548A(address=0x70, i2c_driver=qwiic_i2c.getI2CDriver())
        self.tref = 0
        self.absolute = np.zeros(1 + self.n * 3)
       
    def calibrate(self, tref, absolute = np.array([ 0, 0, 9.81 ])):
        self.tref = tref
        self.absolute = np.pad(np.tile(absolute, self.n), (1, 0), constant_values=(0))
        self.__read(self.calibration)

    def table(self):
        return pd.DataFrame(data=self.data)
        
    def record(self):
        self.data.resize((len(self.data) + 1, 1 + self.n * 3))
        self.data[-1][0] = time.time() - self.tref
        self.__read(self.data[-1])
        self.data[-1] = self.data[-1] - self.calibration + self.absolute
        
    def __read(self, row):
        for i in range(self.n):
            self.mux.disable_all()
            self.mux.enable_channels([i])
            x, y, z = acc.readACC(model="MMA8452Q")
            row[i * 3 + 1] = x
            row[i * 3 + 2] = y
            row[i * 3 + 3] = z
        return row
    
    def save(self, filename="accelerometers.npy"):
         np.save(filename, self.data)