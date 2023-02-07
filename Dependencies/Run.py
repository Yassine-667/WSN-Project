from src import init
from src import election
from src import find
from src import join
import copy

def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)
    return re_list


class Simulation:

    def __init__(self, n=100,p=0.1,Eo=5.0,No=10, state=1):
        self.n = n
        self.p=p
        self.Eo=Eo
        self.No=No
        self.state=state
        self.dead_num = 0
        self.no_of_ch = 0
        self.flag_first_dead = 0
        self.initEnergy = 0

        self.my_model = init.Model(self.n,self.p,self.Eo) 
        self.SRP = zeros(1, self.my_model.rmax + 1) 
        self.RRP = zeros(1, self.my_model.rmax + 1)
        self.SDP = zeros(1, self.my_model.rmax + 1)
        self.RDP = zeros(1, self.my_model.rmax + 1)

        self.srp = 0
        self.rrp = 0
        self.sdp = 0
        self.rdp = 0

        self.dead_num = []
        self.packets_to_base_station = 0
        self.first_dead_in = -1
        
 
        self.alive = self.n

        self.sum_dead_nodes = zeros(1, self.my_model.rmax + 1)
        self.ch_per_round = zeros(1, self.my_model.rmax + 1)


        self.alive_sensors = zeros(1, self.my_model.rmax + 1)
        self.alive_sensors[0] = self.n

        self.sum_energy_left_all_nodes = zeros(1, self.my_model.rmax + 1)
        self.avg_energy_All_sensor = zeros(1, self.my_model.rmax + 1)
        self.consumed_energy = zeros(1, self.my_model.rmax + 1)
        self.Enheraf = zeros(1, self.my_model.rmax + 1)


    def start(self):

        self.__create_sen()

        self.__start_simulation()

        noeuds,model,tour = self.__main_loop()

        return self.n,self.my_model,self.alive_sensors,self.sum_energy_left_all_nodes,noeuds,model,tour

    def __check_dead_num(self, round_number):

        for sensor in self.Sensors:
            if sensor.E <= 0 and sensor not in self.dead_num:
                sensor.df = 1
                self.dead_num.append(sensor)


        if len(self.dead_num) > 0 and self.flag_first_dead == 0:

            self.first_dead_in = round_number
            self.flag_first_dead = 1

    def __create_sen(self):


        self.Sensors = init.create_sensors(self.my_model)

        for sensor in self.Sensors[:-1]:
            self.initEnergy += sensor.E

        self.sum_energy_left_all_nodes[0] = self.initEnergy
        self.avg_energy_All_sensor[0] = self.initEnergy / self.n


    def __start_simulation(self):

        self.sender = [self.n]
        self.receivers = [_ for _ in range(self.n)]

        self.srp, self.rrp, self.sdp, self.rdp = find.start(
            self.Sensors, self.my_model, self.sender, self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
            packet_type='Hello'
        )

        self.SRP[0] = self.srp
        self.RRP[0] = self.rrp
        self.SDP[0] = self.sdp
        self.RDP[0] = self.rdp


    def __main_loop(self):

        for round_number in range(1, self.my_model.rmax + 1):

            self.srp, self.rrp, self.sdp, self.rdp = init.reset(self.Sensors, self.my_model, round_number)
 
            self.__cluster_head_selection_phase(round_number)
            self.no_of_ch = len(self.list_CH)

            if(round_number==self.No):                
                noeuds,model,tour = copy.deepcopy(self.Sensors),copy.deepcopy(self.my_model),round_number
                
            self.__steady_state_phase()

            self.__check_dead_num(round_number)


            self.__statistics(round_number)

            if len(self.dead_num) >= self.n:
                self.lastPeriod = round_number
                break
        
        return noeuds,model,tour

    def __cluster_head_selection_phase(self, round_number):

        self.list_CH = election.start(self.Sensors, self.my_model, round_number, self.state)
        self.no_of_ch = len(self.list_CH)

        self.__broadcast_cluster_head()


        join.start(self.Sensors, self.my_model, self.list_CH)

    def __broadcast_cluster_head(self):

        for ch_id in self.list_CH:
            self.receivers: list = find.findReceivers(self.Sensors, self.my_model, sender=ch_id,
                                                      sender_rr=self.Sensors[ch_id].RR)

          
            self.srp, self.rrp, self.sdp, self.rdp = find.start(
                self.Sensors, self.my_model, [ch_id], self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                packet_type='Hello'
            )


    def __steady_state_phase(self):

        for i in range(self.my_model.NumPacket): 

            for receiver in self.list_CH:
                sender = find.findSenders(self.Sensors, receiver)

                self.srp, self.rrp, self.sdp, self.rdp = find.start(
                    self.Sensors, self.my_model, sender, [receiver], self.srp, self.rrp, self.sdp, self.rdp,
                    packet_type='Data'
                )

        for sender in self.Sensors:
            
            if sender.MCH == self.n and sender.id != self.n and sender.E > 0:
                self.receivers = [self.n] 
                sender = [sender.id]

                self.srp, self.rrp, self.sdp, self.rdp = find.start(
                    self.Sensors, self.my_model, sender, self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                    packet_type='Data'
                )

        for sender in self.list_CH:
            self.receivers = [self.n]

            self.srp, self.rrp, self.sdp, self.rdp = find.start(
                self.Sensors, self.my_model, [sender], self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                packet_type='Data'
            )

    def __statistics(self, round_number):

        self.sum_dead_nodes[round_number] = len(self.dead_num)
        self.ch_per_round[round_number] = self.no_of_ch
        self.SRP[round_number] = self.srp
        self.RRP[round_number] = self.rrp
        self.SDP[round_number] = self.sdp
        self.RDP[round_number] = self.rdp

        self.alive = 0
        sum_energy_left_all_nodes_in_curr_round = 0
        for sensor in self.Sensors[:-1]:
            if sensor.E > 0:
                self.alive += 1
                sum_energy_left_all_nodes_in_curr_round += sensor.E

        self.alive_sensors[round_number] = self.alive
        self.sum_energy_left_all_nodes[round_number] = sum_energy_left_all_nodes_in_curr_round
        if self.alive:
            self.avg_energy_All_sensor[round_number] = sum_energy_left_all_nodes_in_curr_round / self.alive
        else:
            self.avg_energy_All_sensor[round_number] = 0
        self.consumed_energy[round_number] = (self.initEnergy - self.sum_energy_left_all_nodes[round_number]) / self.n

        En = 0
        for sensor in self.Sensors:
            if sensor.E > 0:
                En += pow(sensor.E - self.avg_energy_All_sensor[round_number], 2)

        if self.alive:
            self.Enheraf[round_number] = En / self.alive
        else:
            self.Enheraf[round_number] = 0
        
