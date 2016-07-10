A Python based CNC Router.

Currently supported GCode commands: G1

###Available commands:

cli.py - used for executing GCode files. For use instructions run python cli.py

queue.py - used for consuming (rabbitmq-)queued GCode files. For use instructions run python queue.py

###Install

Ensure pip is installed: http://www.liquidweb.com/kb/how-to-install-pip-on-ubuntu-14-04-lts/

Ensure 'pika' is installed: https://pika.readthedocs.io/en/0.10.0/