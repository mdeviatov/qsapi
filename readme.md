# qsapi
## Goal
The goal of this project is to integrate Qlik Sense Apps into version control.

qlik_explore.py discovers all applications on a Qlik Sense instance. 
For every application it will collect the load script, variables, master
dimensions and measurements and the sheets. For every sheet child objects
are collected.
Collected information is stored in directory structure for the application.

git_processing then checks for changes, commits and push the changes 
to the repository.

The process can run unattended daily to ensure all changes
are collected on a regular base.