#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import pickle


def dump_or_load(file, var=None, dump=False):
    if dump:
        # save variable to a file
        with open(file, "wb") as file:
            pickle.dump(var, file)
        print(f"Saved  {file}")
        return
    else:
        # from file to variable
        with open(file, "rb") as file:
            var_loaded = pickle.load(file)
        print(f"Opened {file}")
        return var_loaded
