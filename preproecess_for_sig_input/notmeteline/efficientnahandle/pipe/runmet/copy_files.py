import os
import sys
import shutil

args = sys.argv

old_dir = args[1]
files = os.listdir(old_dir)
if len(files) == 1:
    folder = old_dir + '/' + files[0]

new_dir = old_dir[:-4]

for fol in os.listdir(folder):
    name = fol.split('\\')[1][1:]
    og = folder + '/' + fol + '/stdout'
    shutil.copyfile(og, new_dir + '/' + name + '.txt')