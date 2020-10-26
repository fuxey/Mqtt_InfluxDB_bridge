from flask import jsonify, render_template, redirect, request, url_for
from app.base import blueprint
from flask import current_app
import logging

logger = logging.getLogger("mqttInfluxDBPusher")


@blueprint.route('/', methods=['GET'])
def route_default():
    return redirect(url_for('base_blueprint.state'))


@blueprint.route('/state', methods=['GET'])
def state():
    mqttInfluxDbBridge = current_app.config['MQTTINFLUXDBBRIDGE_ALLTOPICS']()
    return str(mqttInfluxDbBridge)


@blueprint.route('/addSubscription', methods=['POST'])
def add_subscription():
    topic_to_subscribe = str(request.args.get('topic'))
    logger.debug("receive topic: " + str(topic_to_subscribe))
    current_app.config['MQTTINFLUXDBBRIDGE_ADDTOPIC'](topic_to_subscribe)
    return redirect(url_for('base_blueprint.state'))


@blueprint.route('/removeTopic', methods=['DELETE'])
def remove_topic():
    topic_to_unsubscribe = str(request.args.get('topic'))
    logger.debug("remove topic: " + str(topic_to_unsubscribe))
    current_app.config['MQTTINFLUXDBBRIDGE_REMOVETOPIC'](topic_to_unsubscribe)
    return redirect(url_for('base_blueprint.state'))
