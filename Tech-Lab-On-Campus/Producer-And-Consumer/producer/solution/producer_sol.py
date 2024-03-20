# importing required libraries
import pika
import os
from producer_interface import mqProducerInterface

class mqProducer(mqProducerInterface): 

    # constructor
    def __init__(self, routing_key: str, exchange_name: str): 
        # save parameters to class variables
        self.myrouting_key = routing_key
        self.myexchange_name = exchange_name

        # Call setupRMQConnection
        self.setupRMQConnection()

    # connecting to the RabbitMQ
    def setupRMQConnection(self): 
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.myconnection = pika.BlockingConnection(parameters=con_params)

        # Establish Channel
        self.mychannel = self.myconnection.channel()

        # Create the exchange if not already present
        self.myexchange = self.mychannel.exchange_declare(exchange = self.myexchange_name)

    def publishOrder(self, message: str):
        # Basic Publish to Exchange
        self.mychannel.basic_publish(
            exchange = self.myexchange_name,
            routing_key = self.myrouting_key,
            body="Start Order",
        )

        # Close Channel
        self.mychannel.close()
        # Close Connection
        self.myconnection.close()

