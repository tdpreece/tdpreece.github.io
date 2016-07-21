---
layout: post
title: "How to ssh to a Vagrant VM"
date: 2016-02-22
---

I had created a Vagrant VM (`config.vm.box = "precise32"`) and wanted to
ssh to it using my own user and without using the `vagrant ssh` command.

I changed to the dir that contained the `Vagrantfile` and connected to the
VM via ssh using vagrant's command.
```
tdpreece@laptop$:~/vagrant/example_deployment$ vagrant ssh
```

I then changed to my user and created the necessary ssh files.
```
vagrant@precise32:~$ sudo su tdpreece
tdpreece@precise32:/home/vagrant$ cd
tdpreece@precise32:~$ mkdir .ssh
tdpreece@precise32:~$ chmod 700 .ssh
tdpreece@precise32:~$ touch .ssh/authorized_keys
tdpreece@precise32:~$ chmod 600 .ssh/authorized_keys
```

I then copied the contents of `~/.ssh/id_rsa.pub` from my laptop to 
`~/.ssh/authorized_keys` on the VM.

Back on my laptop I obtained the inforamtion I needed to ssh to the VM
using my own user. 
```
tdpreece@:~laptop/vagrant/example_deployment$ vagrant ssh-config
Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /home/tdpreece/.vagrant.d/insecure_private_key
  IdentitiesOnly yes
  LogLevel FATAL
```

Then I connected to the VM via ssh using my own user,
```
tdpreece@tdpreece-Inspiron-3542:~/vagrant/example_deployment$ ssh -p 2222 tdpreece@127.0.0.1

Welcome to your Vagrant-built virtual machine.
Last login: Thu Jul 21 20:26:11 2016 from 10.0.2.2
tdpreece@precise32:~$ 
```
