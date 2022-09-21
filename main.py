from synchro import Synchro
import sys


if __name__ == '__main__':
    folders_synchronisation = Synchro(sys.argv[1], sys.argv[2], sys.argv[3])
    folders_synchronisation.initial_copy()
    folders_synchronisation.log_path_folder()
    periodic_sychro = folders_synchronisation.periodic_save()
    
    
