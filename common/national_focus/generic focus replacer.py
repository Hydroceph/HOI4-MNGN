import pathlib

# Get the path to the current directory
folder_path = pathlib.Path(__file__).parent
print(folder_path)

# Loop through each .txt file in the folder, only processing .txt files
for file_path in folder_path.glob('*.txt'):
    if file_path.is_file():
        with open(file_path, 'r') as file:
            filedata = file.read() 
            print(f"Processing {file_path.name}")
        filedata = filedata.replace('shared_focus = army_effort', 'shared_focus = mod_army_effort')
        filedata = filedata.replace('shared_focus = aviation_effort', 'shared_focus = mod_aviation_effort')
        filedata = filedata.replace('shared_focus = naval_effort', 'shared_focus = mod_new_naval_estimates')
        filedata = filedata.replace('shared_focus = industrial_effort', 'shared_focus = mod_scrap_naval_estimates')
        filedata = filedata.replace('shared_focus = political_effort', 'shared_focus = mod_industrial_effort')
        with open(file_path, 'w') as file:
            file.write(filedata)