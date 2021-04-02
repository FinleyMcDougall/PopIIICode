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
    creation_times = star_ds.data['pop3', 'creation_time'].to('Myr')
    # unique ID for each particle
    star_ids = star_ds.data['pop3', 'particle_index'].d.astype(int)
    n_stars = star_ids.size

    a = ytree.load("p2p_nd/p2p_nd.h5")
    halo_positions = a['position'].to('unitary').d
    virial_radii = a['virial_radius'].to('unitary').d

    ### Step 1: find trees for all the star particles
    star_trees = []
    star_id_list = []
    f = open('my_file.yaml', mode='r')
    tree_data = yaml.load(f, Loader=yaml.FullLoader)
    for my_star_id, my_star in tree_data.items():
        my_tree = a[my_star["tree_id"]]
        star_trees.append(my_tree)
        star_id_list.append(my_star_id)

    ### Step 2: for each tree/star pair, find the earliest halo containing the star
    # a list of all halos
    f = open('simulation.yaml', mode='r')
    data = yaml.load(f, Loader=yaml.FullLoader)
    for mystartree, mystarid in zip(star_trees, star_id_list):
        pbar = yt.get_pbar('Seaching', mystartree.tree_size)
        creation_time = creation_times[np.where(mystarid==star_ids)[0]][0]
        my_halos = []
        for ihalo, halo in enumerate(mystartree['forest']):
            pbar.update(ihalo)

            # skip the final halo that has no descendent
            if halo.descendent is None:
                continue

            if halo['time'] < creation_time and halo.descendent['time'] > creation_time:
                # keep the descendent since that's the halo we actually want
                print (f"Adding candidate halo {halo.descendent}.")
                my_halos.append(halo.descendent)
        pbar.finish()

        ### Step 2.5: my_halos has all halos at the right time. Now find which one of those
        # contains the star. Use the 'Snap_idx' field to find the right snapshot to load to get the star's position at the right time. If there are multiple halos in the correct distance from the star then choose the largest halo
        new_dict = dict((item['Snap_idx'], item['filename']) for item in data)
        filename = new_dict[my_halos[0]["Snap_idx"]]
        filenameentry = filename.split("/")[0]
        ds_filename = f"pop3/{filenameentry}.h5"
        star_halo_ds = yt.load(ds_filename)
        star_halo_ids = star_halo_ds.data['pop3', 'particle_index'].d.astype(int)
        star_halo_positions = star_halo_ds.data['pop3', 'particle_position'].to('unitary').d
        halo_id = np.where(mystarid==star_halo_ids)[0]
        star_halo_pos = star_halo_positions[halo_id]
        star_halos_wanted = []
        for my_halo in my_halos:
            my_halo_position = my_halo['position'].to('unitary').d
            my_halo_virial = my_halo['virial_radius'].to('unitary').d
            my_halo_distance = distance(star_halo_pos, my_halo_position)
            if my_halo_distance < my_halo_virial:
                star_halos_wanted.append(my_halo)
                #tree_data[mystarid]["halo_id"] = my_halo.tree_id
        if star_halos_wanted:
            my_star_halo_masses = [star_halo['mass'] for star_halo in star_halos_wanted]
            my_halo = star_halos_wanted[np.argmax(my_star_halo_masses)]
            tree_data[mystarid]["halo_id"] = my_halo.tree_id
    f = open('halodata.yaml', mode='w')
    yaml.dump(tree_data, stream=f)
    f.close()
