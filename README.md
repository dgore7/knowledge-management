# knowledge-management

## Project Requirements
A knowledge management system permits a user to create a repository of data and then use various means to search the repository.
The user may enter text data directly into the system, as well as add both text and binary files.
Further, the system should permit the user to organize the data by associating pieces of data with labels that represent categories or other divisions. These labels may also be considered as keywords.
The system would permit the user to later search for relevant data and files using a variety of criteria.

## helpful commands

### virtual environment
To create a virtual environment
`$ py -m venv env c:\path\to\env`

To activate the virtual environment
```
Windows: `$ <env directory>\Scripts\activate.bat`
Mac: `$ source <env directory>/bin/activate`
```
To deactivate: `$ deactivate`

### third party packages
Upgrade pip: `$ easy_install -U pip`

Install package and add it to requirements:
```
$ pip install <some package>
$ pip freeze > requirements.txt
```
Install current project requirements: `$ pip install -r requirements.txt`


## helpful links

