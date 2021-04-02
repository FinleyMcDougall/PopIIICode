import numpy as np
import yt
import ytree
import matplotlib.pyplot as plt
import yaml

#distance formula to find the find the distance between two points in 3D space by finding sqrt(dx^2 + dy^2 +dz^2)
def distance(x1, x2):
    return np.sqrt(((x1-x2)**2).sum()) 

#Step 3 - Opening the list of halos containing the star at its earliest time after creation as well as an additional file for a star for which a halo could not be found. Get the treenode for these halos.
if __name__ == "__main__":
    star_ds = yt.load("pop3/DD0560.h5")
    star_positions = star_ds.data['pop3', 'particle_position'].to('unitary').d
    creation_times = star_ds.data['pop3', 'creation_time'].to('Myr').d
    # unique ID for each particle
    star_ids = star_ds.data['pop3', 'particle_index'].d.astype(int)
    n_stars = star_ids.size
    
    b = ytree.load('/home/brs/finley/first_star/first_star.h5')
    tree = b[0]

    a = ytree.load("p2p_nd/p2p_nd.h5")
    halo_positions = a['position'].to('unitary').d
    virial_radii = a['virial_radius'].to('unitary').d
    halowanted = []
    star_id_list = []

    f = open('halodata.yaml', mode='r')
    tree_data = yaml.load(f, Loader=yaml.FullLoader)
    for star_id, myhalo in tree_data.items():
        my_tree = a[myhalo["tree_id"]]
        my_halo = my_tree.get_node('forest', myhalo['halo_id'])
        my_star = star_id
        halowanted.append(my_halo)
        star_id_list.append(my_star)

halowanted.append(tree)

#halo1 = halowanted[0]
#halo2 = halowanted[1]

#Making empty lists to append the masses of the ancestors and corresponding time of the halo's main progenitor containing the stars. Also a list of 12 distinct colours such that when graphed the stars can be distinguished.
star_halo_mass = []
star_halo_time = []
colour = ['b', 'r', 'g', 'c', 'm', 'y', 'orange', 'lime', 'violet', 'purple', 'k', 'coral']


#graphing the evolution of mass of the halos for each star
"""
for iwanted, i in zip(halowanted, colour):
    star_halo_mass = iwanted['prog', 'mass'].to('Msun')
    star_halo_time = iwanted['prog', 'time'].to('Myr')
    plt.plot(star_halo_time, star_halo_mass, i, label = iwanted)

plt.ylabel('Halo Mass (log(Msun))')
plt.xlabel('Time (Myr)')
#plt.legend()
plt.yscale('log')
plt.savefig("StarHaloEvo")
"""
#Graphing Final Mass of the Star with respect to time
"""
for iwanted, i in zip(halowanted, colour):
    star_mass = iwanted['mass'].to('Msun')
    star_time = iwanted['time'].to('Myr')
    #plt.plot(star_time, star_mass, i, label = iwanted)
    plt.plot(star_time, star_mass, 'ro')
plt.ylabel('Halo Mass (Msun)')
plt.xlabel('Time (Myr)')
plt.yscale('log')
#plt.legend()
plt.savefig("FinalMass")
"""
"""
#Graphing the rate of growth for each star
for i, (iwanted, icolour) in enumerate(zip(halowantd, colour)):
star_halo_mass = iwanted['prog', 'mass'].to('Msun')
star_halo_time = iwanted['prog', 'time'].to('Myr')
dtime = star_halo_time[1:] - star_halo_time[:-1]
dmass = star_halo_mass[1:] - star_halo_mass[:-1]
gradient = dmass/dtime
time = star_halo_time[:-1]    
plt.plot(time, gradient)
plt.ylabel('Growth Rate (MSun/Myr)')
plt.xlabel('Time (Myr)')
plt.savefig("GradientNew1")
"""
#Making a list of the times of the star's creation and the final mass of their corresponding halo
"""
file = open("StarCreations1.txt", "a")
for iwanted, istar in zip(halowanted, star_id_list):
    name = str(iwanted)
    time = str(iwanted['time'])
    mass = str(iwanted['mass'])
    star = str(istar)
    file.write(name + " " + time + " " + mass + " " + star)
    file.write('\n')
file.close()
"""
