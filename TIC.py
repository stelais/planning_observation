from astroquery.mast import Catalogs
import numpy as np

def get_star_info(IDnumber):
	tic = Catalogs.query_object("TIC {0}".format(IDnumber), radius=0.0001, catalog="TIC")
	star = tic[np.argmin(tic["dstArcSec"])]
	tic_ID = int(star["ID"])
	tic_ra = float(star["ra"])
	tic_dec = float(star["dec"])
	return tic_ID, tic_ra ,tic_dec

def main():
	############# WRITE THE NAME OF YOUT TXT FILE CONTAINING YOUR ID
	ID_INPUT = 'list_TIC'

	#Reading the ID.txt file
	file_read = np.loadtxt(ID_INPUT+'.txt')
	lista = file_read.astype(int)
	lista = lista.astype(str)
	lista = lista.tolist()
	#print('lista: ',lista,'\n',type(lista))

	#WRITING IN TXT FILE
	table_path = open(ID_INPUT + '_output.txt',"w")
	table_path.write("      ID \t             RA \t                 DEC \n")

	for IDnumber in lista:
		tic_ID, tic_ra, tic_dec =  get_star_info(IDnumber)
		table_path.write(" %10d  \t" % (tic_ID) \
			+ " %4.15f \t" % (tic_ra) \
			+ " %4.15f \t" % (tic_dec) + "\n") \
	
	table_path.close()   

main()
 