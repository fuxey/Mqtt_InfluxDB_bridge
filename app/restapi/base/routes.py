from flask import redirect, request, url_for
from restapi.base import blueprint
from flask import current_app, render_template, jsonify
import logging
import json
from constants import *

logger = logging.getLogger("mqttInfluxDBPusher")
logger.info("register routes!")


@blueprint.route('/health', methods=['GET'])
def health_route():
    return str('health')


@blueprint.route('/', methods=['GET'])
def route_default():
    return render_template('index.html')


@blueprint.route('/help', methods=['GET'])
def help_route():
    return render_template('help.html')


@blueprint.route('/state', methods=['GET'])
def state():
    mqttInfluxDbBridge = current_app.config[MQTTINFLUXDBBRIDGE_ALLTOPICS]()
    received_messages_counter = current_app.config[MQTTINFLUXDBBRIDGE_GET_RECEIVED_MESSAGE_COUNTER]()
    logger.debug(mqttInfluxDbBridge)
    default = {"topics": [],
               "receivedMessages": received_messages_counter}
    for key in mqttInfluxDbBridge:
        default["topics"].append(key)

    return json.dumps(default)


@blueprint.route('/addSubscription', methods=['POST'])
def add_subscription():
    data = json.loads(request.stream.read())
    logger.debug(data["topic"])
    topic_to_subscribe = data["topic"]
    measurement_name = data["measurementName"]
    host_name = data["hostName"]
    database_name = data["dbName"]

    logger.debug("receive topic: " + topic_to_subscribe)
    current_app.config[MQTTINFLUXDBBRIDGE_ADDTOPIC](topic_to_subscribe,
                                                    measurement_name,
                                                    host_name)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@blueprint.route('/removeTopic', methods=['DELETE'])
def remove_topic():
    data = json.loads(request.stream.read())
    logger.debug(data["topic"])
    topic_to_unsubscribe = data["topic"]
    logger.debug("remove topic: " + topic_to_unsubscribe)
    current_app.config[MQTTINFLUXDBBRIDGE_REMOVETOPIC](topic_to_unsubscribe)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@blueprint.route('/create_database', methods=['POST'])
def create_database():
    database_to_create_name = str(request.args.get('name'))
    logger.debug("create database with name: " + database_to_create_name)
    current_app.config[MQTTINFLUXDBBRIDGE_CREATE_DATABASE](database_to_create_name)
    return redirect(url_for('base_blueprint.state'))


@blueprint.route('/list_database', methods=['GET'])
def list_databases():
    allDatabase = current_app.config[MQTTINFLUXDBBRIDGE_LIST_DATABASE]()
    return str(allDatabase)
