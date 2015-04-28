quotepuller
===
Get daily options quotes and save to a mongo database.

Usage
---
### Basic
1.  Install:
    
        $ npm install
        $ sudo npm run setup

1.  Configuration. 

1.  Start:

        $ sudo npm start

1.  Stop:

        $ sudo npm stop
       
#### Configuration
An example of how to use configurations is provided in `lib/show.js`.
Call this script with:

    $ npm run show

Detailed documentation in the [Quichean wiki](http://quichean.wikidot.com/wiki:configuring-services).

Testing
---
### Functionality
    $ npm test

### Code conformity
    $ jshint lib test
    $ jscs .

Connects to
---
- mongoDB
