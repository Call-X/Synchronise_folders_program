
# VeeamsoftwareProjet - "Synchronise_folders_program"


## Custommer asking:

Veeam Software, a socity which the global leader in data protection asked me to develop a small program 
that synchronizes two folders: source and replica. 
The program should maintain a full, identical copy of source folder at replica folder


## Installation guide :
1. Clone the repository 
```
$ git clone https://github.com/Call-X/Synchronise_folders_program.git
```
2. Navigate to the root folder of the repository

3. Create a virtual environnement with :
``` 
python -m venv projectenv
```
3. Activate the virtual environment with
``` 
projectenv/Srcipts/activate
``` 
4. install the project with its dependencies with :
``` 
pip install -r requirements.txt
``` 

## How to use ?

1. Finally, run the synchroniser program with :
``` 
Your <synchronisation_content> has to be express in seconds
``` 
``` 
python main.py <source_folder_path> <destination_folder_path> <log_file.txt> <synchronisation_content>
``` 
## Contributeur :

-Emile MIATH -

# Licence & Copyright :

Aucun copyrights