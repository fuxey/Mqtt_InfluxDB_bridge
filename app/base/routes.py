from flask import jsonify, render_template, redirect, request, url_for
from app.base import blueprint
from flask import current_app

@blueprint.route('/', methods=['GET'])
def route_default():
    return redirect(url_for('base_blueprint.state'))


@blueprint.route('/state', methods=['GET'])
def state():
    allTopics = current_app['MQTTINFLUXDBBRIDGE'].getAllSubscribedTopics()
    return "all Topics" + allTopics


@blueprint.route('/addSubscription', methods=['POST'])
def add_subscription():
    return redirect(url_for('base_blueprint.state'))


@blueprint.route('/removeTopic', methods=['DEL'])
def remove_topic():
    return redirect(url_for('base_blueprint.state'))
