![RocketWsIcon](https://www.dropbox.com/s/rkhtagviyjf1bvp/rocket_icon.png?dl=1) RocketWS
====================================================================================================
[![Stories in Ready](https://badge.waffle.io/prawn-cake/RocketWS.png?label=ready&title=Ready)](https://waffle.io/prawn-cake/RocketWS)
[![Build Status](https://travis-ci.org/prawn-cake/RocketWS.svg)](https://travis-ci.org/prawn-cake/RocketWS)
[![Coverage Status](https://img.shields.io/coveralls/prawn-cake/RocketWS.svg)](https://coveralls.io/r/prawn-cake/RocketWS)

RocketWS is open-sourced WebSockets push server based on gevent-websocket library


Features
---------

* Free easy-use asynchronous standalone WebSockets server, allows to build cutting edge web-applications;
* All interactions are based on [JSON-RPC 2.0 Specification](http://www.jsonrpc.org/specification); 
* Unlimited subscribe channels;
* Can support multiple message sources, default is HTTP;
* Scalable software design;
* Supports command-line interface;


Workflow
---------
![RocketWSWorkflow](https://www.dropbox.com/s/nz4krowb760tpho/rocketws_workflow.png?dl=1)


Interactions
------------
Several main types of server interactions are supported:

* WebSockets - is used by browser-like clients;
* MessagesSources - is used by backend applications;
* Command line interface - useful for testing;

Request examples
----------------
All requests must be correspond to [JSON-RPC 2.0 Specification](http://www.jsonrpc.org/specification)

* WebSockets
  * **Subscribe** to channel `chat`:
  ```{"id": 0, "jsonrpc": "2.0", "method": "subscribe", "params": {"channel": "chat"}}```
  
  * **Unsubscribe** from channel `chat`:
  ```{"id": 0, "jsonrpc": "2.0", "method": "unsubscribe", "params": {"channel": "chat"}}```
  
  * **Send data** to channel `chat`:
  ```{"id": 0, "jsonrpc": "2.0", "method": "send_data", "params": {"channel": "chat", "data": {"message": "hola!"}}}```
    

* MessagesSources
  * **Emit** message for all subscribers for channel `chat`: ```{"id": 0, "jsonrpc": "2.0", "method": "emit", "params": {"channel": "chat", "data": {"message": "hola!"}}}```
  * **Notify all** subscribers (some system messages): ```{"id": 0, "jsonrpc": "2.0", "method": "notify_all", "params": {"data": {"message": "Broadcase system message"}}}```


Command line interface
-----------------------

* Run shell: ```make shell```
* Type ```help``` for more information


Configuration
--------------
Main settings file is `rocketws/settings.py`

There are two parameters:

* `MESSAGES_SOURCE` -- control MessagesSource parameters for backend interaction. Default port: *59999* 

* `WEBSOCKETS` -- control WebSockets server parameters for clients interaction. Default port: *58000*


Installation/Deployment
------------------------
### Dependencies
Make sure that you have ```libevent-2.0-5``` or ```libev4``` in your system.

### Develop way

* Get source code: ```git clone https://github.com/prawn-cake/RocketWS.git <dir:RocketWS>```

* Setup virtualenv: ```cd <dir:RocketWS> && make env```

* Check settings at: ```<dir:RocketWS>/rocketws/settings.py```

* Run it: ```make run```

### Supervisor way

* Get source code, setup virtualenv and check settings as described above

* Install supervisor: ```sudo aptitude install supervisor  # Debian-way```

* Add supervisor config: ```sudo vim /etc/supervisor/conf.d/rocketws.conf```

```
[program:rocketws]
command=<dir:RocketWS>/.env/bin/python <dir:RocketWS>/rocketws/server.py
autostart=false
autorestart=true
user=<str:user>
stdout_logfile=<dir:logdir>/rocketws.log
```

* Update supervisor configurations: ```sudo supervisorctl reread && sudo supervisorctl update```

* Start RocketWS with: ```sudo supervisorctl start rocketws```


### Docker way
**NOTE:** Docker works fine (without any workarounds) only under x86_64 arch (based on my tests)

* [Install docker](https://docs.docker.com/installation/ubuntulinux/)

**NOTE:** use ```sudo``` with the following commands or add your user to a docker group

* ```docker pull prawncake/rocketws```
* ```docker run -i -t -d -p 58000:58000 -p 59999:59999 prawncake/rocketws make run_bg```