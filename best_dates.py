import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_moon 
from pytz import timezone
from astroplan import Observer
from astroplan import FixedTarget
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file, save


def observer_function(name_of_the_observatory, name_timezone):
    return Observer.at_site(name_of_the_observatory, timezone=name_timezone)

def target_wanted(RA, DEC, name_target='Target'):
    coordinates = SkyCoord(RA, DEC, unit="deg")
    return FixedTarget(name=name_target, coord=coordinates)

def target_coord(RA, DEC):
    return SkyCoord(RA, DEC, unit="deg")  

def targeting_moon(observe_time):
    coordinates_moon = get_moon(observe_time)
    coordinates_moon = coordinates_moon.icrs      
    return FixedTarget(name='Moon', coord=coordinates_moon)  

def getting_good_airmass(target_coords, time, obs_location):
    #Getting airmass
    target_altaz = target_coords.transform_to(AltAz(obstime=time,location=obs_location)) 
    target_airmass = target_altaz.secz
    good_airmass = []
    for index in range(0,len(target_airmass)):
        if target_airmass[index] <= 1.5:
            eh_obs = 1
            #print(target_airmass[index])
        else:
            eh_obs = 0
        good_airmass.append(eh_obs)
    return good_airmass    

def night_is_good(observer,time):
    nights = []
    for index in range(0,len(time)):
        if observer.is_night(time[index]):
                night = 1
                print(index)
        else:
                night = 0
        nights.append(night)
    return nights     

def save_night(observer,time):
    nights = night_is_good(observer,time)

    path = open('it_is_night.txt','w')
    print("aqui")
    night_time = []
    for index in range(0,len(nights)):
        if nights[index] == 1: 
            print(index)
            path.write(str(time[index])+"\n")
    path.close()        
    return None 

def read_night(file_path='it_is_night.txt'):
    file = open(file_path,'r')
    tempo =[]
    for line in file:
        line = line.replace("\n","")
        tempo.append(Time(line))
    file.close()        
    return tempo

def gerando_noites():
        #================ADD HERE THE DETAILS OF YOUR OBSERVATION
    name_of_the_observatory = 'ctio'
    name_timezone = 'America/Santiago'
    utcoffset = -3*u.hour
    time_str = '2020-02-01 17:00:00'
    #/\ The code uses in UTC, so here is still your timezone if you fix in the utcoffset


    observe_time = Time(time_str) - utcoffset
    print(observe_time)
    #time window
    delta_time = np.linspace(0, 181.6, 5200)*u.day
    time = observe_time + delta_time
    print(time)
    #to_be_plot = time.plot_date
    
    observer = observer_function(name_of_the_observatory,name_timezone) 

    save_night(observer,time)    

def main():
    #=================ADD HERE YOUR .TXT FILE WITH THE ID OF YOUR TARGETS
    file_read = np.loadtxt('TIC_output.txt', skiprows = 1)
    ID_array = file_read[:,0]    
    RA_array = file_read[:,1]
    DEC_array = file_read[:,2] 

    #================ADD HERE THE DETAILS OF YOUR OBSERVATION
    name_of_the_observatory = 'ctio'
    name_timezone = 'America/Santiago'
    utcoffset = -3*u.hour
    time_str = '2020-02-01 17:00:00'
    #/\ The code uses in UTC, so here is still your timezone if you fix in the utcoffset

    how_many_targets = len(ID_array)

    observe_time = Time(time_str) - utcoffset
    print(observe_time)
    #time window
    delta_time = np.linspace(0, 181.6, 36200)*u.day
   
    #============ACTIVATE IF YOU DONT HAVE THE TABLE:
    #time = observe_time + delta_time
    #print(time)

    
    observer = observer_function(name_of_the_observatory,name_timezone)        
    obs_location = observer.location

    #nights = night_is_good(observer,time)

    #night_time = []
    #for index in range(0,len(nights)):
    #    if nights[index] == 1: night_time.append(time[index])

    #===================================== TILL HERE
    
    night_time = read_night('it_is_night.txt')
    time = Time(night_time)

    #TARGET DATA
    good_airmass={}
    for i in range(0,len(RA_array)):
        RA = str(RA_array[i])
        DEC = str(DEC_array[i])
        NAME = str(int(ID_array[i]))
        #frame = 'icrs'

        target = target_wanted(RA, DEC, NAME)
        target_coords = target_coord(RA,DEC)
   
        good_airmass[NAME] = getting_good_airmass(target_coords, time, obs_location)
        #good_airmass = getting_good_airmass(target_coords, time, obs_location)
    #print(good_airmass)

    #TOTAL
    total_of_targets = []
    for index in range(0, len(night_time)):
        result = 0
        for i in range(0,len(RA_array)):
            NAME = str(int(ID_array[i]))
            result = result + good_airmass[NAME][index]
        total_of_targets.append(result)    


    good_time = open('observation.txt','w')
    good_time.write('Time in UTC/TIC_ID')
    for i in range(0,len(RA_array)):
        good_time.write(f'\t{int(ID_array[i])}' )
    good_time.write('\tTOTAL OF TARGETS\n')         
    for index in range(0, len(night_time)):
        good_time.write(str(time[index]))
        for i in range(0,len(RA_array)):
            NAME = str(int(ID_array[i]))
            good_time.write(f'\t{good_airmass[NAME][index]}' )
        good_time.write(f'\t{total_of_targets[index]}\n')    
    
    time_string = [str(x) for x in night_time]
    

    #PLOTTING
    output_file("observable_time.html") 

    p = figure(title = "When can we maximize the targets?",x_range=time_string)
    p.xaxis.major_label_orientation = np.pi/4
    p.xaxis.axis_label = 'Days and Hours in UTC'
    p.yaxis.axis_label = 'Number of targets that are observable'

    p.circle(time_string, total_of_targets, fill_alpha=0.2, size=5)
    save(p)

    plt.figure(figsize=(7,7))
    plt.plot(time_string, total_of_targets,'o', markersize=2)
    plt.xlabel('Hours in UTC')
    plt.ylabel('How many targets are observable?')
    plt.show()    

main()


