from src.init import *

def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        re_list.append(temp_list)

    return re_list


def get_min_and_id_of_ch(myModel: Model, TotalCH, distance: list):
    min_dist_from_all_ch = []
    id_of_min_dist_ch = []

    total_nodes = myModel.n
    number_of_ch = len(TotalCH)

    for node in range(total_nodes):
        min_dist = inf
        ch_id = -1
        for ch in range(number_of_ch):
            if distance[ch][node] <= min_dist:
                min_dist = distance[ch][node]
                ch_id = ch

        min_dist_from_all_ch.append(min_dist)
        id_of_min_dist_ch.append(ch_id)

    return min_dist_from_all_ch, id_of_min_dist_ch


def start(Sensors: list[Sensor], myModel: Model, TotalCH):

    total_nodes = myModel.n
    number_of_ch = len(TotalCH)

    if number_of_ch > 0:
        distance = zeros(number_of_ch, total_nodes)

        for i in range(total_nodes):
            for j in range(number_of_ch):
                distance[j][i] = sqrt(
                    pow(Sensors[i].xd - Sensors[TotalCH[j]].xd, 2) + pow(Sensors[i].yd - Sensors[TotalCH[j]].yd, 2)
                )
        min_dist_from_all_ch, id_of_min_dist_ch = get_min_and_id_of_ch(myModel, TotalCH, distance)


        for i, sensor in enumerate(Sensors[:-1]):
            if sensor.E > 0:
                if min_dist_from_all_ch[i] <= myModel.RR and min_dist_from_all_ch[i] < sensor.dis2sink:
                    sensor.MCH = TotalCH[id_of_min_dist_ch[i]]
                    sensor.dis2ch = min_dist_from_all_ch[i]
                else:
                    sensor.MCH = total_nodes
                    sensor.dis2ch = sensor.dis2sink
