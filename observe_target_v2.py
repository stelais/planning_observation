import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord, get_moon, solar_system_ephemeris, get_sun 
from pytz import timezone
from astropy.time import Time
from astroplan import Observer
from astroplan import FixedTarget
from astroplan.plots import plot_airmass, plot_sky

def observer_function(name_of_the_observatory, name_timezone):
    return Observer.at_site(name_of_the_observatory, timezone=name_timezone)

def target_wanted(RA, DEC, name_target='Target'):
    coordinates = SkyCoord(RA, DEC, unit="deg")
    return FixedTarget(name=name_target, coord=coordinates)

def targeting_moon(observe_time):
    coordinates_moon = get_moon(observe_time)
    coordinates_moon = coordinates_moon.icrs      
    return FixedTarget(name='Moon', coord=coordinates_moon)      

def targeting_sun(observe_time):
    coordinates_sun = get_sun(observe_time)
    coordinates_sun = coordinates_sun.icrs      
    return FixedTarget(name='Sun', coord=coordinates_sun)  


def main():
    #=================ADD HERE YOUR .TXT FILE WITH THE ID OF YOUR TARGETS
    file_read = np.loadtxt('list_TIC_output.txt', skiprows = 1)
    ID_array = file_read[:,0]    
    RA_array = file_read[:,1]
    DEC_array = file_read[:,2] 

    #================ADD HERE THE DETAILS OF YOUR OBSERVATION
    name_of_the_observatory = 'ctio'
    name_timezone = 'America/Santiago'
    time_str = '2019-07-25 04:00:00'
    #/\ Here is in UTC

    #IF YOU WANT TO PLOT THE MOON/SUN AIRMASS + MOON/SUN IN SKY   
    see_moon = 'yes'
    see_sun = 'no'

    how_many_targets = len(ID_array)
    observe_time = Time(time_str)
    
    #time window
    time = observe_time + np.linspace(-12, 12, 100)*u.hour
    to_be_plot = time.plot_date
    observer = observer_function(name_of_the_observatory,name_timezone)
    
    i = 0       
    while how_many_targets > 0 :    
        fig = plt.figure(figsize=(11,7))
        fig.subplots_adjust(hspace=0.5)


        if see_sun == 'yes'
            sun = targeting_sun(observe_time)

            ax = plt.subplot(1, 2, 1)
            plot_airmass(sun, observer, observe_time,brightness_shading=True,style_kwargs={'color': 'r'}, min_airmass=0.5, max_airmass=3.5)
            ax.set_title('Airmass')
            plt.legend(shadow=True, loc=2)
            
            ax = plt.subplot(1, 2, 2, projection='polar')
            plot_sky(sun, observer, observe_time,style_kwargs={'color': 'r'}) 
            ax.set_title('Position at time: '+time_str+'[UTC]\n \n') 
        else:
            pass

        if see_moon == 'yes': 
            moon = targeting_moon(observe_time)

            ax = plt.subplot(1, 2, 1)
            plot_airmass(moon, observer, observe_time,brightness_shading=True, min_airmass=0.5,max_airmass=3.5)
            ax.set_title('Airmass')
            plt.legend(shadow=True, loc=2)

            ax = plt.subplot(1, 2, 2, projection='polar')
            plot_sky(moon, observer, observe_time) 
            ax.set_title('Position at time: '+time_str+'[UTC]\n \n')   
        else:
            pass 
            

        #TARGET DATA

        RA = str(RA_array[i])
        DEC = str(DEC_array[i])
        NAME = str(int(ID_array[i]))
        #frame = 'icrs'

        target = target_wanted(RA, DEC, NAME)
        
        ax = plt.subplot(1, 2, 1)
        plot_airmass(target, observer, observe_time,brightness_shading=True, min_airmass=0.5,max_airmass=3.5)
        plt.text(0.5, 0.9, 'Observatory: '+name_of_the_observatory+'\n Timezone: '+name_timezone, horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes)
        ax.set_title('Airmass')
        plt.legend(shadow=True, loc=2)

        ax = plt.subplot(1, 2, 2, projection='polar')        
        plot_sky(target, observer, observe_time) 
        ax.set_title('Position at time: '+time_str+'[UTC]\n \n') 

        how_many_targets -= 1 
        i += 1
    
        plt.legend(shadow=True, loc=2)
        plt.tight_layout()
        #CHANGE HERE THE PATH AND NAME YOUR DIRECTORY SHOULD BE SAVED IN/AS
        plt.savefig('graph_representation/'+NAME+'.png')
main()   