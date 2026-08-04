# Manual (EN)
Move directory to your GIMP3 plug-in directory 
- Windows: ```.../AppData/GIMP/\<current version number\>/plug-ins/```
- other: ???

Mind you: you can also change or add directories in the GIMP Preferences. 

## Installation
For GIMP3, just paste the entire directory into your respective system folder.

The target directory can be found in GIMP under ```Edit``` → ```Preferences``` → ```Folders```
and in this case under ```plug-ins```.
You can edit the directories to point elsewhere or add more. 

It is important, that the plug-in's folder and main file have the same naming.
Otherwise GIMP will ignore it.

```
<main-directory>/
└── ...
└── plug-ins/
    └── ...
    └── <plugin-name>/
        └── ...
        └── <plugin-name>.py
```

> **Attention**: Before GIMP3.2 add-ons for Win11 on ARM  are not supported. Please update to a  later version.

## Localization of GIMP3 scripts in Python3

### step 0: 
Ensure ```gettext``` is imported and initialised as well as the ```babel``` package installed.

```shell
pip install Babel
```

Afterward, mark every string to be translated in the script as ```_(<string>)```.

### step 1: extract strings
Navigate into the main directory and create a ```locale``` sub-directory.
Afterwards extract all placeholders into a .pot file. For that, define the .pot-file name (the domain name) and add all files to be localised:
```shell
python -m babel.messages.frontend extract -o locale/<file_name>.pot <main_script>.py modules/<secondary_file>.py
```

Repeat when script changes. 

### step 2: init / update translation
After creating the .pot-file .po-files can be created for each language. 

.po-files are already provided with the GIT repository, so the following can be ignored. 
However, when doing this **the first time** anyway, initialise by running the following per language to be translated (e.g. for adding more language support):
```shell
python -m babel.messages.frontend init -i locale/<file_name>.pot -d locale -l <two-digit language code> -D <domain name>
```
This creates a sub-directory path like ```/<two-digit language code>/LC_MESSAGES/``` and creates a ```<domain name>.po```-file
Open it and make changes as needed. 

When running repeated translations (e.g. after extract) **only run**: 
```shell
python -m babel.messages.frontend update -i locale/<file_name>.pot -d locale -l <two-digit language code> -D <domain name>
```

### step 3: compile database
When all is said and done, compile the translations into the database. 
```shell
python -m babel.messages.frontend compile -d locale -D <domain name>
```