# coding:utf-8

import pika
import configparser
import IService
import RemoteProcedure


conf = configparser.ConfigParser()
conf.read('config.conf')
print(conf.get('RabbitMQ','user'))
print(conf.get('RabbitMQ','password'))


class RPCService(IService):
    queueName = ''
    procedure = None

    def __init__(self, queueName, procedure):
        self.queueName = queueName
        self.procedure = procedure

        credentials = pika.PlainCredentials('hadoop', '123xxxx$%^')
        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/finance', credentials))

        channel = connection.channel()


        channel.exchange_declare(exchange='Language_Direct',
                                 exchange_type='direct')
        channel.queue_declare(queue=self.queueName,passive=False,
                              durable=True,exclusive=False,auto_delete=False)

        channel.queue_bind(exchange='Language_Direct',
                       queue=self.queueName,
                       routing_key=self.queueName)


        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(consumer_callback=self.on_request,queue=queueName)
        channel.start_consuming()

    def serve(self,procedure,data):
        return procedure.process(data)

    def on_request(self, ch, method, props, body):
        inputStr = str(body)


        response = self.serve(self.procedure,inputStr)





        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=str(response))

        ch.basic_ack(delivery_tag = method.delivery_tag)

