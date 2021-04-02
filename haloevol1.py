import numpy as np
import yt
import ytree
import matplotlib.pyplot as plt
import yaml

def distance(x1, x2):
    return np.sqrt(((x1-x2)**2).sum()) 

if __name__ == "__main__":
    star_ds = yt.load("pop3/DD0560.h5")
    star_positions = star_ds.data['pop3', 'particle_position'].to('unitary').d
    creation_times = star_ds.data['pop3', 'creation_time'].to('Myr').d
    # unique ID for each particle
    star_ids = star_ds.data['pop3', 'particle_index'].d.astype(int)
    n_stars = star_ids.size

    a = ytree.load("p2p_nd/p2p_nd.h5")
    halo_positions = a['position'].to('unitary').d
    virial_radii = a['virial_radius'].to('unitary').d

    ### Step 1: find trees for all the star particles
    star_trees = []

    data = {}
    
    # loop over all stars
    for istar in range(n_stars):
        star_position = star_positions[istar]
        creation_time = creation_times[istar]
        star_id =int(star_ids[istar])
        data[star_id] = {}
        print (f"Finding halo for star {star_id}.")

        # did we find the star or not
        found = False
        for itree in range(a.size):
            halo_position = halo_positions[itree]
            virial_radius = virial_radii[itree]
            star_distance = np.sqrt(((star_position - halo_position)**2).sum())
            if star_distance < virial_radius:
                print (f"Star {star_id} found in tree {a[itree]}.")
                star_trees.append(a[itree])
                found = True
                data[star_id]["tree_id"] = itree
                break
        # if we reach the end of the loop and didn't find it, append a None so we know.
        if not found:
            print (f"No halo found for star {star_id}!")
            star_halos.append(None)

    #open yaml file and write the halos trees corresponding to each star using the star_id and tree_id
    f = open('my_file.yaml', mode='w')
    yaml.dump(data, stream=f)
    f.close()
    
"""
file = open("StarLocations.txt", "a")
for istar in range(n_stars):
    star_position = str(star_positions[istar])
    star_id = str(star_ids[istar])
    file.write(star_id + " " + star_position)
    file.write('\n')

"""
"""
for istar in range(n_stars):
    pos_diff_1 = star_positions[istar] - star_positions[5]
    pos_diff_2 = star_positions[istar] - star_positions[7]
    pos_diff_3 = star_positions[istar] - star_positions[10]
    star_id = str(star_ids[istar])
    file.write(star_id)
    file.write('\n')
    file.write(pos_diff_1)
    file.write('\n')
    file.write(pos_diff_2)
    file.write('\n')
    file.write(pos_diff_3)
    file.write('\n')
"""
file.close()
