# Manual (EN)
Move directory to your GIMP3 plug-in directory 
- Windows: .../AppData/GIMP/\<current version number\>/plug-ins/
- other: ???

Mind you: you can also change or add directories in the GIMP Preferences. 

## Localization of GIMP3 scripts in Python3

### step 0: 
Ensure ```gettext``` is imported and initialised as well as the ```babel``` package installed.

```shell
pip install Babel
```

Afterwards mark every string to be translated as ```_(<sting>)```

### step 1: extract strings
Navigate into the main directory and create a ```local``` sub-directory.
Afterwards extract all placeholders into a .pot file. For that, define the .pot-file name (the domain name) and add all files to be localised:
```shell
python -m babel.messages.frontend extract -o locale/<file_name>.pot <main_script>.py modules/<secondary_file>.py
```

Repeat when script changes. 

### step 2: init / update translation
After creating the .pot-file .po-files can be created for each language. 

When doing this **the first time**, initialise by running the following per language to be translated:
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