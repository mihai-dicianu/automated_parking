import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
from matplotlib.pylab import *
import matplotlib.patches as mpatches

import pandas as pd

import numpy as np

fig,a =  plt.subplots(2,2,figsize=(15.9, 16.7), dpi=80, facecolor='w', edgecolor='k')
thismanager = get_current_fig_manager()
thismanager.window.wm_geometry("+0+0")
fig.suptitle("Lateral parking sensor measurement", fontsize=20)


a[0][0] = subplot2grid((2, 2), (0, 0))
a[0][1] = subplot2grid((2, 2), (0, 1))
a[1][0] = subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)

ax_front   = a[0][0]
ax_back    = a[0][1]
ax_lateral = a[1][0]
ax_lateral_derivative = ax_lateral.twinx()

ax_front.set_title('Front sensor measurement')
ax_back.set_title('Back sensor measurement')
ax_lateral.set_title('Lateral sensor measurement')

# set label names
ax_front.set_xlabel("x [cm]")
ax_front.set_ylabel("Front distance [cm]")
ax_back.set_xlabel("x [cm]")
ax_back.set_ylabel("Back distance [cm]")
ax_lateral.set_xlabel("x [cm]")
ax_lateral.set_ylabel("Lateral distance [cm]")
ax_lateral_derivative.set_ylabel("Derivative [cm/cm]")


ax_front.grid(True)
ax_back.grid(True)
ax_lateral.grid(True)
ax_lateral_derivative.grid(None)

ax_front.set_facecolor('w')
ax_back.set_facecolor('w')
ax_lateral.set_facecolor('w')
fig.patch.set_facecolor('w')


label_lateral_distance = 'Lateral distance'
label_lateral_distance_derivative = 'Lateral distance derivative'
label_front_distance = 'Front distance'
label_back_distance = 'Back distance'

red_patch = mpatches.Patch(color='blue', label=label_lateral_distance)
blue_patch = mpatches.Patch(color='red', label=label_lateral_distance_derivative)

green_patch = mpatches.Patch(color='green', label=label_front_distance)
yellow_patch = mpatches.Patch(color='yellow', label=label_back_distance)


ax_lateral.legend(handles=[red_patch,blue_patch], loc = 'upper right')
ax_front.legend(handles=[green_patch], loc = 'upper right')
ax_back.legend(handles=[yellow_patch], loc = 'upper right')


# Data Placeholders

lateral_distance = zeros(0)
front_distance = zeros(0)
back_distance = zeros(0)


lateral_x = zeros(0)



'''

# set y-limits
#ax01.set_ylim(0,2)
#ax02.set_ylim(-6,6)
#ax03.set_ylim(-0,5)
#ax04.set_ylim(-10,10)

# sex x-limits
ax01.set_xlim(0,5.0)
ax02.set_xlim(0,5.0)
ax03.set_xlim(0,5.0)
ax04.set_xlim(0,5.0)

'''
ann_max = None
ann_min = None
#carSpeed = 46.15
carSpeed = 26.66
def animate(self, file_path_front, file_path_right, file_path_back):
    
    global lateral_x, lateral_distance, front_distance, back_distance, ann_max, ann_min
    
    data_lateral    = pd.read_csv(file_path_right)
    data_front      = pd.read_csv(file_path_front)
    data_back       = pd.read_csv(file_path_back)
    
    lateral_time = data_lateral['x_value'] 
    lateral_distance = data_lateral['distance']

    lateral_x = []
    for i in lateral_time:
        lateral_x.append(i * carSpeed)
    
    
    #lateral_x = data_lateral['x_value']
    front_distance = data_front['distance']

    #lateral_x = data_lateral['x_value']
    back_distance = data_back['distance']

    derivative = np.diff(lateral_distance)/np.diff(lateral_x)
        
    #derivative_moving_avg = numpy.diff(lateral_distance)/numpy.diff(lateral_x)
    if len(derivative):
        ind_MAX = np.argmax(derivative)
        ind_MIN = np.argmin(derivative)

    

  
    
    #distance = (lateral_x[ind_MIN] - lateral_x[ind_MAX])*carSpeed

    #print("distance is", distance)

   #ax_front   = a[0][0]
    #ax_back    = a[0][1]
   #ax_lateral = a[1][0]
  
    #a[1][0] = subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
    #a[1][0].plot(x,np.exp(x))
    ax_lateral.plot(lateral_x,lateral_distance,'b-', label=label_lateral_distance)
    ax_lateral_derivative.plot(lateral_x[:-1],derivative,'r-', label=label_lateral_distance_derivative)
    
    if len(lateral_x) == len(front_distance):
        ax_front.plot(lateral_x, front_distance, 'g-')
    if len(lateral_x) == len(back_distance):
        ax_back.plot(lateral_x, back_distance, 'y-')
    
    if len(derivative):
        if ann_max != None:
            ann_max.remove()
        if ann_min != None:
            ann_min.remove()
        #Annotate max derivative
        ann_max = plt.annotate("x_max={:.2f}".format(lateral_x[ind_MAX]), xy = (lateral_x[ind_MAX], derivative[ind_MAX]), color = "green", fontsize = 16)
        #Annotate max derivative
        ann_min = plt.annotate("x_min={:.2f}".format(lateral_x[ind_MIN]), xy = (lateral_x[ind_MIN], derivative[ind_MIN]), color = "green", fontsize = 16)



def plotMain(file_path_front, file_path_right, file_path_back):
    print ("Plotter started, opening figure")
    ani = FuncAnimation(fig, animate, blit = False, repeat = False, interval=1, fargs=(file_path_front, file_path_right, file_path_back,))
    #plt.tight_layout()
    plt.show()


#full_path_right = path_csv + right_sensor_file

#plotMain(full_path_right) 
