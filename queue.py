# Load libraries.
import pika
import pprint
import sys
import RPi.GPIO as GPIO
from Nema17 import Nema17
from GCodeStringToCommandArray import GCodeStringToCommandArray
from CNCRouter import CNCRouter

# Check command line parameters.
if len(sys.argv) != 7:
    print "Usage: python queue.py hostname port vhost username password queue"
    sys.exit(-1)

# Load parameters.
HOSTNAME = sys.argv[1]
PORT = int(sys.argv[2])
VHOST = sys.argv[3]
USERNAME = sys.argv[4]
PASSWORD = sys.argv[5]
QUEUE = sys.argv[6]

# TODO: Remove redundant code: see cli.py

# Set PIN mapping to BCM: https://cdn.shopify.com/s/files/1/0176/3274/files/Pins_Only_grande.png?2408547127755526599
GPIO.setmode(GPIO.BCM)

# Create OX and OY axis motor controllers.
OX = Nema17(GPIO, 6, 18)
OY = Nema17(GPIO, 13, 17)
OZ = Nema17(GPIO, 12, 27)

# Based on: https://www.rabbitmq.com/tutorials/tutorial-one-python.html and https://pika.readthedocs.io/en/0.10.0/intro.html
# Prepare authentication.
credentials = pika.PlainCredentials(USERNAME, PASSWORD)
parameters =  pika.ConnectionParameters(HOSTNAME, PORT, VHOST, credentials)

# Connect.
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Create queue - this request is idempotent - the queue will not be overwritten.
channel.queue_declare(queue='gcode', durable=True, exclusive=False, auto_delete=False)

# Based on: http://pika.readthedocs.io/en/0.10.0/examples/blocking_consume.html
def on_message(channel, method_frame, header_frame, body):
    # Parse GCode instructions.
    GCodeCommandsArray = GCodeStringToCommandArray().convert(body);
    # Execute G Code Instructions
    CNCRouter(OX, OY, OZ).execGCode(GCodeCommandsArray)
    # Set message as consumed.
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

channel.basic_consume(on_message, 'gcode')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()

# Free GPIO Pins.
GPIO.cleanup()
