---
layout: post
title: "Developing on a remote server using PyCharm"
date: 2016-02-22
---

The following explains how I set up PyCharm (2016.1.2) so that I could deploy code
to a remote VM and run the tests.  The remote VM I was deploying to was set up using
Vagrant (`config.vm.box = "precise32"`).

## Clone source code from github
File > Settings > Version Control Github, then added my details and

checked the 'Clone git repositories using ssh'.
VCS > Checkout from version control > GitHub

## Configure remote deployment
Tools > Deployment > Configuration
I clicked the green plus sign in the top left of the dialog to add a deployment.
I gave the deployment a name ('a_python_project_deployment') and selected 'SFTP'
from the 'Type' dropdown.
I clicked 'OK'.

### Connection Tab
I used a private-public key pair to connect to the remote VM

![alt text](/assets/img/pycharm-deployment-config.png)

I then clicked the 'Test SFTP connection button' to check everything was working.

### Mappings Tab
I added a deployment path for the remote server

### Excluded Paths tab
I did not add any excluded paths for this project, however, if I would exlude the
directory that contains the virtual environment if it is contained within the project
folder.

I then clicked 'OK' to save this configuration.

### Upload code to remote server

#### Initial upload
Tools > Deployment > Upload to a_python_project_deployment, where 'a_python_project_deployment', where
was the name of the deployment I configured in the previous step.
I have noticed that it does seem to matter which file/folder you have seleted in Project window.  Select
the root of the project to make sure that everything gets uploaded.
Your project will now be uploaded to the remote server.
I then made an ssh connection with the remote server to check that it had worked.

```
tdpreece@precise32:~$ tree a_python_project 
a_python_project
`-- test
    |-- __init__.py
    `-- test1.py
```

#### Uploading changes during development
I enabled 'Automatic Upload' (Tools > Deployment) so that I didn't have to manually upload
changes that I made.
After adding a new file (test2.py) I checked on the remote sever and the new file had appeared

```
tdpreece@precise32:~$ tree a_python_project/
a_python_project/
|-- README.md
`-- test
    |-- __init__.py
    |-- test1.py
    `-- test2.py
```

#### Pulling in change from the origin
I pulled in changes from origin/master (VCS > Git > Pull), which resulted in a new file, test3.py,
being added to the 'test' dir on PyCharm, however, when I checked the remote server test3.py was not
present.
This was fixed by,
Tools > Deployment > Upload to a_python_project_deployment, where 'a_python_project_deployment'.

## Configure the interpreter
File > Settings > Project > Project interpreter
I cliked on the cog button at the end of the 'Project Interpreter' select box then clicked on 'Add remote'
and configured the interpreter as shown below (I was using a virtualenv).
![alt text](/assets/img/pycharm-configure-remote-python-interpreter.png)
When developing in Python 2.7 on CentOS 6 servers I had to add the following line to my ~/.bashrc

```
source scl_source enable python27
```

## Running the tests
Run > Edit Configurations
Clicked the green plus button in the top left to add a test configuration
Entered the following details,

![alt text](/assets/img/pycharm-remote-test-config.png)

Run the tests with, Run > Run 'my tests', where 'my tests' is the name I gave to my configuration.
