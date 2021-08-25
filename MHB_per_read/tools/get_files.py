import os 
import shutil
import sys

args = sys.argv

folder = args[1]
ext = args[2]

def get_subfolders(fol):
    subfolders = [ f.path for f in os.scandir(fol) if f.is_dir() ]
    return subfolders

def add_files_to_directory(fol, ext, directory):
    files = os.listdir(fol)
    for file in files:
        if file[-len(ext):] == ext:
            new_file = shutil.copy(fol + '/' + file, directory)

def get_all_folders(fol, ext, directory):
    subfols = get_subfolders(fol)
    files = os.listdir(fol)
    if (len(files) == 0 or ((len(files) == 1) and ('.ipynb_checkpoints' not in files[0] or '.DS_store' not in files[0]))):
        return 
    else:
        for subfol in subfols: 
            add_files_to_directory(fol, ext, directory)
            get_all_folders(subfol, ext, directory)

def make_directories(fol, ext):
    subfols = get_subfolders(fol)
    dirs = []
    for subfol in subfols:
        if '.ipynb_checkpoints' not in subfol:
            new_dir_name = subfol.split('/')[-1] + '_' + ext + '_folder'
            os.mkdir(new_dir_name)
            dirs.append(new_dir_name)
            get_all_folders(subfol, ext, new_dir_name)
    return dirs

dirs = make_directories(folder, ext)

get_all_folders(folder, 'final.txt', 'empty')