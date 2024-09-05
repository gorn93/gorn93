import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class simulation_of_crowd :
    def __init__(self, room_size =(50,50),exit =(0,0),crowd=100,person_radius=0.5):
        self.room_size = room_size
        self.exit = exit
        self.crowd = crowd
        self.people =[]
        self.initial_people()
        self.person_radius = person_radius
        self.exited = 0

    def initial_people(self):
        generated_position = set()
        for i in range(self.crowd) :
            while True :
                x = np.random.uniform(0,self.room_size[0])
                y = np.random.uniform(0,self.room_size[1])
                point = (x,y)

                if point not in generated_position :
                    generated_position.add(point)
                    break
            speed = np.random.uniform(1.2,1.45)
            self.people.append({'position':np.array([x,y]),'speed':speed})

    def deplacement(self):
        for person in self.people :
            direction = self.exit - person['position']
            if np.linalg.norm(direction)> 0.5 :
                direction /= np.linalg.norm(direction)
                new_pos = person['position'] + direction*person['speed']
                new_pos[0] = np.clip(new_pos[0],0,self.room_size[0])
                new_pos[1] = np.clip(new_pos[1],0,self.room_size[1])
                person['position'] = new_pos

        self.people = [p for p in self.people if np.linalg.norm(p['position']-self.exit)>0]
        self.nb_restants = self.crowd - len(self.people)

    def run_simulation(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        scatter = ax.scatter([],[],c=[],cmap='viridis',s=50,vmin =1.2,vmax=1.45)
        exit_marker = ax.plot(*self.exit[:], 'rs', markersize=20)[0]
        ax.set_xlim(0, self.room_size[0])
        ax.set_ylim(0, self.room_size[1])
        text = ax.text(0.02, 0.98, '', transform=ax.transAxes, verticalalignment='top')

        def update(frame) :
            if self.people :
                self.deplacement()
                positions = np.array([p['position'] for p in self.people])
                speeds= [p['speed'] for p in self.people]
                scatter.set_offsets(positions[:])
                scatter.set_array(np.array(speeds))
                text.set_text(f'People exited: {self.nb_restants}')
                return scatter, exit_marker, text
            else :
                plt.close(fig)
                return scatter, exit_marker, text
        
        anim = FuncAnimation(fig,update,frames=None,interval = 20,repeat=False,blit=True)
        plt.show()

sim1 = simulation_of_crowd(room_size = (200,200),exit=(200,0),crowd=500)
sim1.run_simulation()
