# planning_observation
The routines in this repository were made to plan an observation. 'TIC.py' is a routine that prepare your data in the format for 'observe_target_v2.py' routine. This second routine creates a plot of airmass and a skymap for your target.
The idea is to have a file with lists of IDs, run 'TIC.py', and then run 'observe_target_v2.py'. They were made for the Tess Input Catalog and CTIO obs but you can change the catalog/observatory on the code :)

'observe_target_v1.py'is an alternative version if you don't need to download RA and DEC from a catalog. You must type all the info, though... It's only useful for a few targets (and it uses ICRS as default), otherwise it's a lot of extra work :p ... If you have a lot of targets, just check the format 'observe_target_v2.py' is expecting! It is: ID, RA, DEC (in deg) separated by TAB, and run only 'observe_target_v2.py'.

You can edit the file to fit your needs. If you use it, please refere me :-) 

Let me know if you have any questions. I'll be happy to help !

-Stela


Here are examples of what should come out:

Sirius:
![alt text](https://github.com/stelais/planning_observation/blob/master/Sirius.png)


Target TIC 115015715. This one is missing the info of the observatory and timezone, because when I generated it, the command plt.text was commented.
![alt text](https://github.com/stelais/planning_observation/blob/master/115015715.png)

Target TIC 143821840. Also missing the info of the observatory and timezone for same reason. 
![alt text](https://github.com/stelais/planning_observation/blob/master/143821840.png)


++++++++++++++++++++++
I added something here. The new script: best_dates.py generates a table with the observability of each target over the time. Observable (yes - 1) or not observable (no - 0). That way we can keep track of the best nights to observe.
The table sums the # of wanted targets we can observe. And also produces a graph to visualize this.
