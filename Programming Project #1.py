
#!/usr/bin/env/python3
if __name__ == '__main__':
    data = []
    with open('2FA9noend.pdb', 'r') as f:
        for i, l in enumerate(f):
            d = l.strip().split()
            types = [str, int, str, str, str, int, float, float, float, float, float, str]
            d = [t_i(d_i) for d_i, t_i in zip(d, types)]
            # Append
            data.append(d)

    # Average AMU of atoms
    amu = {'C': 12.0107, 'O': 15.999, 'N': 14.0067, 'S': 32.065}

    
    # Ask user what to do
    do_what = input("Geometric Center [GC] or Center of mass [CM]: ")

    # Coordinates for GC or CM
    x,y,z = 0,0,0
    # Total Mass
    total_mass = 0

    # For each atom
    for d in data:
        # Get the coords
        x_a, y_a, z_a = d[6:9]

        if do_what.lower() == 'gc':
            # Keep a running sum
            x += x_a
            y += y_a
            z += z_a
            total_mass += 1

        elif do_what.lower() == 'cm':
            # Get atom name and mass
            atom_name = d[-1]
            m = amu[atom_name]

            # Running sum of mass * coords
            x += m * x_a
            y += m * y_a
            z += m * z_a
            total_mass += m
        else:
            print("Did not select good inputs. Please choose GC or CM.")
            assert False

    # Normalize running sum
    x /= total_mass
    y /= total_mass
    z /= total_mass


    pdb_format = "{:6s}{:5d} {:^4s}{:1s} {:3s} {:1d} {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:>2s}\n"

    with open('output.pdb', 'w') as f:
        for d in data:
            # Shift each coordinate by the center 
            x_a, y_a, z_a = d[6:9]
            x_a -= x
            y_a -= y
            z_a -= z
            d[6:9] = x_a, y_a, z_a

            # Write the pdb file
            f.write(pdb_format.format(*d))

    print(f"Wrote to file and shifted using {do_what}")