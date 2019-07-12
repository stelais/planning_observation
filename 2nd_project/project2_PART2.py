from astropy import units as u
from astropy.constants import sigma_sb, L_sun
import numpy as np
import matplotlib.pyplot as plt
 
def get_flux(temperature): 
    boltzmann_constant =  sigma_sb
    flux = boltzmann_constant * temperature**4
    return flux
def get_diameter_star(luminosity, temperature):
    flux = get_flux(temperature)
    diameter_of_star = (((luminosity)/(4*np.pi*flux))**(1/2))*2
    return diameter_of_star
def get_distance(diameter_of_aperature, wavelength, luminosity, temperature):
    diameter_star = get_diameter_star(luminosity,temperature)
    distance = ((diameter_star * diameter_of_aperature)/ (1.22*wavelength))
    return distance
def get_distance_in_pc(diameter_of_aperature,wavelength, luminosity,temperature):   
    return (get_distance(diameter_of_aperature,wavelength, luminosity,temperature)).to(u.parsec)
# L_sun
def mean_luminosity_mainsequence(type):
  if type == 'M':
    return 10000*L_sun
  if type == 'K':
    return 3895*L_sun
  if type == 'G':
    return 1950*L_sun
  
def mean_temperature(type):  
  if type == 'M':
    return 3500.0 *u.K
  if type == 'K':
    return 4379.0 *u.K
  if type == 'G':
    return 5000.0 *u.K


wavelength_infrared = 1*u.mm
diameter_of_aperature = np.linspace(0.05,2.4,30)* u.m
list = ['M', 'K', 'G']


###################################################### PLOT ################################################
fig = plt.figure(figsize=(10,6))
for star_type in list:
  distance_inpc = get_distance_in_pc(diameter_of_aperature,wavelength_infrared,mean_luminosity_mainsequence(star_type), mean_temperature(star_type))
  plt.plot(diameter_of_aperature,distance_inpc,label=star_type)

plt.xlabel('Diameter of aperature (m)')
plt.ylabel('Distance (pc)')
plt.title('Nearest distance a telescope can resolve a star class Ib')
plt.legend(shadow=True)  
plt.show()  
