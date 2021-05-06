#! usr/bin/env python3
import pika
import uuid

class PartitionRPCRequestor():
    def __init__(self,  queueName):
        self.queueName = queueName

        self.credentials = pika.PlainCredentials('hadoop', '123xxxx$%^')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672,
                                                                            '/finance', self.credentials))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='Language_Direct',
                                 exchange_type='direct')
        argsDict = {'x-max-priority':8}

        self.channel.queue_declare(queue=self.queueName, passive=False,
                              durable=True, exclusive=False, auto_delete=False,arguments=argsDict)

        replyTo = self.channel.queue_declare(exclusive=True)
        self.callback_queue = replyTo.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def request(self,data):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        issuccess = self.channel.basic_publish(exchange='Language_Direct',
                                   routing_key=self.queueName,  #'pythonServer',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(data))
        if issuccess:
            while self.response is None:
                self.connection.process_data_events()
            return self.response
        else:
            return 'Error'

if __name__ == '__main__':
    requestor = PartitionRPCRequestor('pythonServer')

    result = requestor.request('{"pluginName":"sencondPlugin"}')

    print("respone is : ",result)