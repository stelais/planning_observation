# planning_observation
The routines in this repository were made to plan an observation. 'TIC.py' is a routine that prepare your data in the format for 'observe_target_v2.py' routine. This second routine creates a plot of airmass and a skymap for your target.
The idea is to have a file with lists of IDs, run 'TIC.py', and then run 'observe_target_v2.py'. They were made for the Tess Input Catalog and CTIO obs but you can change the catalog/observatory on the code :)

'observe_target_v1.py'is an alternative version if you don't need to download RA and DEC from a catalog. You must type all the info, though... It's only useful for a few targets, otherwise it's a lot of extra work :p ... If you have a lot of targets, just check the format 'observe_target_v2.py' is expecting! It is: ID, RA, DEC (in deg) separated by TAB, and run only 'observe_target_v2.py'.

You can edit the file to fit your needs. If you use it, please refere me :-) 

Let me know if you have any questions. I'll be happy to help !

-Stela
