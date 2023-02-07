from src import Run
from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.init import *
import tkinter.font as font


#Mise en Place de l'interface graphique :

root = tk.Tk()
root.geometry('1300x800')
root.title("Projet WSN")
right_frame = tk.Frame(root, bg='#121111', bd=1)
right_frame.place(relx=0.3, rely=0.05, relwidth=0.65, relheight=0.9)
left_frame = tk.Frame(root, bg='#4C4E52')
left_frame.place(relx=0.03, rely=0.05, relwidth=0.30, relheight=0.9)

#Gestion du Placement du Graphe :

figure = plt.Figure(figsize=(4, 6),dpi=80)
figure.set_size_inches(10.5, 5.5)
ay = figure.add_subplot(111)
line = FigureCanvasTkAgg(figure, right_frame)
line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH,expand=1)


#La Fonction Principale : 


def Clustering(state:int):
    global App, n, my_model, alive_sensors,sum_energy_left_all_nodes
    n=int(entry1.get())
    p=float(entry2.get())
    En_max=float(entry3.get())
    roundReseau=int(entry4.get())
    App=Run.Simulation(n,p,En_max,roundReseau,state)
    n,my_model,alive_sensors,sum_energy_left_all_nodes,noeuds,model,tour=App.start()
    ay.clear()
    capture(noeuds,model,tour)
    line.draw()


#Cette Fonction nous dessine le graphe : 

def capture(Sensors: list[Sensor], model, round_number):
    n = model.n
    ay.set_xlim(left=0, right=model.x)
    ay.set_ylim(bottom=0, top=model.y)
    n_flag = True
    c_flag = True
    d_flag = True

    for sensor in Sensors:
        if sensor.E > 0:
            if sensor.type == 'N':
                if n_flag:
                    ay.scatter([sensor.xd], [sensor.yd],s=70, c='#88B04B', edgecolors='none', label='Noeud Vivant')
                    n_flag = False
                else:
                    ay.scatter([sensor.xd], [sensor.yd],s=70, c='#88B04B', edgecolors='none')
            elif sensor.type == 'C':
                if c_flag:
                    ay.scatter([sensor.xd], [sensor.yd], c='#D65076',s=110, edgecolors='none', label='Cluster Head')
                    c_flag = False
                else:
                    ay.scatter([sensor.xd], [sensor.yd], c='#D65076',s=110, edgecolors='none')
        else:
            if d_flag:
                ay.scatter([sensor.xd], [sensor.yd], c='#5A5A5A',s=70, edgecolors='none', label='Noeud Mort')
                d_flag = False
            else:
                ay.scatter([sensor.xd], [sensor.yd], c='#5A5A5A',s=70, edgecolors='none')

    ay.scatter([Sensors[n].xd], [Sensors[n].yd], s=130, c='#5B5EA6', edgecolors='b', label="Station de Base")
    ay.grid(TRUE)
    ay.set_title('Round N°: %d' %round_number, y=-0.25)
    ay.legend(loc='upper right',  bbox_to_anchor=(1.0, 1),prop={'size': 13})
    ay.set_xlabel('Longueur:m'),ay.set_ylabel('Largeur:m')
    


#On intègre ces deux fonctions dans nos bouttons :

def Suppression():
    ay.clear()
    line.draw()


def commande_lancement():
    Clustering(2)


#Mise en Place des Bouttons ainsi que les zones texte de notre UI :

RH = 0.095
myFont = font.Font(size=16)

Button1 = tk.Button(left_frame,text="Execute", bg="#88B04B",fg='white', borderwidth=2,command = commande_lancement)
Button1['font'] = myFont
Button1.place(relx=0.16,rely=5*(0.1 + RH*0.54) ,relheight=0.5*RH, relwidth=0.5)



Button2 = tk.Button(left_frame,text="Clean Up",bg="#D65076",fg='white', borderwidth=2,command = Suppression)
Button2['font'] = myFont
Button2.place(relx=0.15,rely= 5.5*(0.1 + RH*0.54) ,relheight=0.5*RH, relwidth=0.5)


#Mise en place des Zones de texte : 


Nbr_noeuds = Label(left_frame, text = 'Nbr de Noeuds (n) :')
Nbr_noeuds.place(relx=0.3,rely= 1.2*(0.1 + RH*0.54), relwidth=0.3,relheight=0.3*RH)
entry1 = Entry(left_frame)
entry1.place(relx=0.25,rely= 1.5*(0.1 + RH*0.54), relwidth=0.4,relheight=0.3*RH)
entry1.insert(0,100)

Cluster_Head = Label(left_frame, text = "Cluster Head % (p) :")
Cluster_Head.place(relx=0.3,rely= 2*(0.1 + RH*0.54), relwidth=0.3,relheight=0.3*RH)
entry2 = Entry(left_frame)
entry2.place(relx=0.25,rely= 2.3*(0.1 + RH*0.54), relwidth=0.4,relheight=0.3*RH)
entry2.insert(0,0.1)

Energie_max = Label(left_frame, text = "En_max (joule) :")
Energie_max.place(relx=0.3,rely= 2.8*(0.1 + RH*0.54), relwidth=0.3,relheight=0.3*RH)
entry3 = Entry(left_frame)
entry3.place(relx=0.25,rely= 3.1*(0.1 + RH*0.54), relwidth=0.4,relheight=0.3*RH)
entry3.insert(0,5)

Nbr_rounds = Label(left_frame, text = "Nbr de Rounds :")
Nbr_rounds.place(relx=0.3,rely= 3.6*(0.1 + RH*0.54), relwidth=0.3,relheight=0.3*RH)
entry4 = Entry(left_frame)
entry4.place(relx=0.25,rely= 3.9*(0.1 + RH*0.54), relwidth=0.4,relheight=0.3*RH)
entry4.insert(0,20)

#Def de la fonction Main :

def main():
    Clustering(1)
    root.mainloop()

if __name__ == '__main__':
    main()
