quotepuller
===
Get daily options quotes and save to a mongo database.

Usage
---
### Basic
1.  Install, configure and run `@optbot/pytools` to configure 
    Python and Python virtual environments on the server and to
    set `npm` configurations so that the necessary Python
    tools can be used by other `optbot` packages.

1.  Install:
    
        $ npm install
        $ sudo apt-get update
        $ sudo npm run setup

    To restrict setup to updating only the code for configuring
    and running the daemon process (without creating a new user
    or a python virtual environment):

        $ sudo npm run setup -- --daemon

1.  Configuration. See [below](#configuration).

1.  Start:

        $ sudo npm start

1.  Stop:

        $ sudo npm stop

1. Start and stop in test mode. See [below](#testing).
       
#### Configuration
##### Initialize
To configure the service to use a remote database running on host `91.198.174.192` with
the default `mongodb` port:
```
$ sudo npm config set @optbot/quotepuller:db "mongodb://91.198.174.192:27017/"
```
More info in the [Quichean wiki](https://github.com/aisthesis/quichean/wiki/Configuration).

##### Update running service
1. Stop the service
1. Delete prior configuration and replace with new:

        $ sudo rm /etc/quichean/quotepuller.cfg

1. If you also want to update the code for the service:

        $ sudo rm -rf /usr/local/lib/quichean/quotepuller/*

Testing
---
### Functionality
To start and stop the service in test mode, use the commands:

    $ sudo npm start -- --test
    $ sudo npm stop

The start command in test mode really does start the service, so
be sure to stop it when you are finished verifying that it is working.
Note that the `stop` command is the same whether testing or running live.

#### Differences
- In test mode the service immediately attempts to retrieve options quotes
regardless of time of day or day of week. When running outside of test mode,
the service will instead wait until market close and will not attempt to 
retrieve data on weekends or holidays.
- In test mode the service will write quote data to a special `optionsTst`
database.

#### Troubleshooting
If the service isn't working despite seemingly successful installation, the
required python libraries probably didn't get installed correctly. Starting with
`numpy`, verify that you really can import the modules listed in `requirements.txt`
when using the `quotepuller` virtual environment. If not, do `sudo su`, activate
the virtual environment, install everything needed by hand, then `chown` the
virtual environment directory as specified in `setup.js`.

### Code conformity
    $ jshint lib test
    $ jscs .

Connects to
---
- mongoDB
