
from PIL import Image

import PySimpleGUI as GUI
import os.path
import imageio
import h5py as h5
import numpy as np


print("hdf5 converter started")
# variables definition
exportTypes = ["Sequences", "Single frames"]
export = exportTypes[0]  # default value
path = path0 = "/no folder"
sequence = []


# functions
def checkpath(directory, default):
    if os.path.exists(directory):
        print("Folder defined:", directory)
        return 1
    elif directory == default:
        print("Please select a folder.")
        return 0
    else:
        print("Path does not exist")
        return 0

# window management
layout = [
    [GUI.Text("Select folder with .hdf5 to convert")],
    [GUI.FolderBrowse("Folder", enable_events=True)],
    [GUI.Text("Export mode:")],
    [GUI.Combo(exportTypes, size=(100, 50), default_value=exportTypes[0], enable_events=True, key='ExportTypes')],
    [GUI.Button("OK")], [GUI.Button("Cancel")]
]
window = GUI.Window(".hdf5 converter", layout, size=(290, 150))
while True:
    event, values = window.read()
    if event == GUI.WIN_CLOSED or event == 'Cancel':
        print("Program closed")
        exit()

    if event == 'Folder':
        path = values['Folder']
        checkpath(path, path0)

    if event == 'ExportTypes':
        export = values['ExportTypes']
        print("Export mode defined as \"" + export + "\"")

    if event == 'OK':
        print("Parameters defined")
        print("\tPath: ", path, "\n\tExport mode: ", export)
        if checkpath(path, path0):
            window.close()
            break

print('\n_______________\nConversion Started\n')
##########################################

# fileName = "\\25-1-YeaZ_seg_0-3.h5"
fileNames = os.listdir(path)
print(len(fileNames), "files and folder in path: ", fileNames)

for file in fileNames:
    print("______________\nNext File: ")
    if not file.endswith(".h5") | file.endswith(".hdf5"):
        print(file, "is not a .hdf5")
        continue
    else:
        print("\nTreating hdf5 File: " + file)

        # h5-file definition (dictionary-like) and keys extraction
        f = h5.File(path + "\\" + file, 'r')  # groups
        keys = f.keys()  # array with the keys found in the hdf5 file
        print('List of keys in ' + file, str(list(keys)) + " (Number=" + str(len(keys)) + "):")
        fileName = os.path.splitext(file)[0]  # get name without extension

        if not os.path.exists(path + "\\" + "Masks"):
            os.makedirs(path + "\\" + "Masks")  # Create a folder if it does not exist

        # Iterates across file's groups/keys
        for i in keys:
            # quality check of groups/keys reading
            print("\nTreating key:" + str(f[i]))

            # getting datasets within the group
            T_datasets = f[i]
            print("\n'T_datasets' in '" + str(i) + "': " + str(T_datasets))
            print("T_datasets type and list : ", type(T_datasets), list(T_datasets))
            if len(T_datasets) > 0 and export == exportTypes[1]:
                if not os.path.exists(path + "\\" + "Masks" + "\\" + fileName + "_" + i):
                    os.makedirs(
                        path + "\\" + "Masks" + "\\" + fileName + "_" + i)  # Create a FOV folder if it does not exist
            # Sort datasets (the sorting in hdf5 files is not in the chronological order: 0-1-10-100-101-102-103-.....-12-120, etc)
            # Remove the "T" at the beginning of string of T_datasets and sort
            T_datasets = [j[1:] for j in T_datasets]
            T_datasets.sort(key=int)
            print("T_datasets list after sorting : ", list(T_datasets))

            # iterated across image datasets

            for j in T_datasets:  # for each dataset (timepoints) in a field of view
                data = np.array(f[i]["T" + j])
                print("data in image ", i, "T" + j, str(type(data))[8:-2], "max=" + str(np.amax(data)),
                      "min=" + str(np.amin(data)))

                # format adjustment
                dataPIL = (data * 255).astype(np.uint8)

                # make a new image from dataset and save or append to sequence
                if export == exportTypes[1]:
                    imageio.imwrite(path + "\\" + "Masks" + "\\" + fileName + "_" + i + "\\"
                                    + fileName + "_" + i + "_T" + j + ".tif", dataPIL)
                if export == exportTypes[0]:
                    im = Image.fromarray(dataPIL)
                    sequence.append(im)

            if export == exportTypes[0]:
                print("image count in sequence ", i, ": ", len(sequence))
                imageio.mimwrite(path + "\\" + "Masks" + "\\" + fileName + "_" + i + "_SEQ.tif", sequence,
                                 format="tif")
                sequence.clear()  # resetting image sequence
