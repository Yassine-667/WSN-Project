
import random
from math import *


class Model:
    def __init__(self, n,p,Eo):
        self.n = n
        self.x = 1000
        self.y = 1000
        self.sink_x = self.x * 0.5
        self.sink_y = self.y * 0.5
        self.sinkE = 100 
        self.p: float = p
        self.Eo: float = Eo
        self.Eelec: float = 50 * 0.000000001
        self.ETX: float = 50 * 0.000000001
        self.ERX: float = 50 * 0.000000001
        self.Efs: float = 10e-12
        self.Emp: float = 0.0013 * 0.000000000001
        self.EDA: float = 5 * 0.000000001
        self.do: float = sqrt(self.Efs / self.Emp)
        self.rmax = 200
        self.data_packet_len = 4000
        self.hello_packet_len = 100
        self.NumPacket = 10
        self.RR: float = 0.5 * self.x * sqrt(2)


class Sensor:
    def __init__(self):
        self.xd = 0
        self.yd = 0
        self.G = 0
        self.df = 0
        self.type = 'N'
        self.rs=0
        self.Eo=5
        self.E: float = 0
        self.id = 0
        self.dis2sink: float = 0
        self.dis2ch: float = 0
        self.MCH = 0  # Member of which CH
        self.RR = 0


def create_sensors(my_model: Model):
    n = my_model.n
    sensors = [Sensor() for _ in range(n + 1)]

    sensors[n].xd = my_model.sink_x
    sensors[n].yd = my_model.sink_y
    sensors[n].E = my_model.sinkE
    sensors[n].id = my_model.n
    sensors[n].type = 'S'

    for i, sensor in enumerate(sensors[:-1]):

        sensor.xd = random.randint(1, my_model.x)
        sensor.yd = random.randint(1, my_model.y)
 
        sensor.G = 0
        sensor.df = 0
        sensor.type = 'N'
        sensor.E = my_model.Eo
        sensor.id = i
        sensor.RR = my_model.RR
        sensor.MCH = n
        sensor.dis2sink = sqrt(pow((sensor.xd - sensors[-1].xd), 2) + pow((sensor.yd - sensors[-1].yd), 2))


    return sensors



def reset(Sensors: list[Sensor], my_model: Model, round_number):
    for sensor in Sensors[:-1]:


        AroundClear = 1 / my_model.p 
        if round_number % AroundClear == 0:
            sensor.G = 0
        sensor.MCH = my_model.n

        if sensor.type != 'S':
            sensor.type = 'N'
        sensor.dis2ch = inf

    srp = 0  
    rrp = 0 
    sdp = 0 
    rdp = 0  

    return srp, rrp, sdp, rdp
