#!/bin/bash
sudo gpgconf --kill dirmngr
sudo chown -R $USER:$USER ~/.gnupg
