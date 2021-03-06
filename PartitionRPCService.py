#! usr/bin/env python3
#coding:utf-8
import pika
import configparser
import json
from pluginManager import DirectoryPluginManager

conf = configparser.ConfigParser()
conf.read('config.conf')

queueName = 'pythonServer'
plugin_manager = DirectoryPluginManager()
plugin_manager.loadPlugins()

credentials = pika.PlainCredentials('tabkey', '123456^')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/finance', credentials))
channel = connection.channel()
channel.exchange_declare(exchange='Language_Direct',
                         exchange_type='direct')

argsDict = {'x-max-priority':8}

channel.queue_declare(queue=queueName, passive=False,
                      durable=True, exclusive=False, auto_delete=False,arguments=argsDict)


channel.queue_bind(exchange='Language_Direct',
                   queue=queueName,
                   routing_key=queueName)

def serve(data):
    print("revice data:   ",data)
    dataStr = data.decode()
    dataJson = json.loads(dataStr)
    print(type(dataJson))

    plugins = plugin_manager.getPlugins(name=dataJson['pluginName'])

    assert isinstance(dataJson, object)
    plugins[0].getResult(jsonData=dataJson)

    return 'ok'
    # return plugins[0].getResult(jsonData=jsonData)


def on_request(ch, method, props, body):


    response = serve(body)

    if props.reply_to is None:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return response;

    ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))


channel.basic_qos(prefetch_count=1)
channel.basic_consume(consumer_callback=on_request, queue=queueName)

channel.start_consuming()

