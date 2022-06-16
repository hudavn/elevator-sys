from collections import OrderedDict
from elevator.SystemManager import SystemManager
import sys
from datetime import datetime
import threading
from flask import request, Flask, jsonify
import logging

server = Flask(__name__)
server.config["JSON_SORT_KEYS"] = False


def startService():
    global elevator_system 
    elevator_system = SystemManager(numOfCabinets, numOfFloors)
    elevator_system.on()
    threading.Thread(target=elevator_system.serve).start()


@server.route('/system', methods=['GET'])
def getSystemStatus():
    return jsonify(elevator_system.getStatus())


@server.route('/cabin', methods = ['GET'])
def getCabinStatus():
    if 'id' in request.args and str(request.args['id']).isnumeric():
        id = int(request.args['id'])
        if id < elevator_system.numberOfCabinets:
            return jsonify(elevator_system.getStatus(id))
        else: 
            return resource_not_found(404)
    else:
        return jsonify(
            OrderedDict({
                'status': 400,
                'message': "The request could not be understood by the server due to incorrect syntax."
            })), 400


@server.route('/order', methods = ['POST'])
def requestSystem():
    if 'from' in request.args and str(request.args['from']).isnumeric() and \
        'direction' in request.args and str(request.args['direction']).isnumeric() and \
        int(request.args['direction']) in [0, 1]:
            floor = int(request.args['from'])
            direction = int(request.args['direction'])

            if floor <= elevator_system.numberOfFloors:
                resp = elevator_system.request(direction, floor)
                return jsonify(
                    {
                        'index': resp[0],
                        'key': resp[1],
                        'timestamp': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    })
            else: 
                return resource_not_found(404)
    else:
        return jsonify(
            OrderedDict({
                'status': 400,
                'message': "The request could not be understood by the server due to incorrect syntax."
            })), 400


@server.route('/servant', methods = ['POST'])
def servantRequest():
    if 'id' not in request.args or 'destination' not in request.args:
        return jsonify( 
            OrderedDict({
                'status': 400,
                'message': "The request could not be understood by the server due to incorrect syntax."
            })), 400

    if not str(request.args['id']).isnumeric() or int(request.args['id']) not in elevator_system.servant:
        return resource_not_found(404)

    id = int(request.args['id'])
    if 'key' not in request.args or request.args['key'] != elevator_system.servant[id][0]:
        return jsonify(
            OrderedDict({
                'status': 403,
                'message': "Unauthorized request."
            })), 403
    
    if not str(request.args['destination']).isnumeric():
        return resource_not_found(404)

    destination = int(request.args['destination'])
    servant = elevator_system.getServant(id)
    
    if servant == None:
        return jsonify(
            OrderedDict({
                'status': False, 
                'message': "Your order is still in queue."
            })), 200
    else: 
        ok = elevator_system.cabinRequest(servant, destination)
        if ok:
            return jsonify(
                OrderedDict({
                    'status': True, 
                    'message': "OK!"
                })), 200
        else:
            return jsonify(
                OrderedDict({
                    'status': 400, 
                    'message': "Request does not match the direction."
                })), 400


@server.errorhandler(404)
def resource_not_found(e):
    return jsonify(
        OrderedDict({
            'status': 404,
            'message': "The resource could not be found."
        })
    ), 404


@server.errorhandler(500)
def internal_server_error(e):
    return jsonify(
        OrderedDict({
            'status': 500,
            'message': 'The server encountered an unexpected condition that prevented it from fulfilling the request.'
        })
    ), 500


@server.errorhandler(405)
def method_not_allowed(e):
    return jsonify(
        OrderedDict({
            'status': 405,
            'message': 'The method is not allowed for this resource.'
        })
    ), 405


numOfFloors = 40
numOfCabinets = 2

startService()

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO, 
        format=('%(levelname)s:\t'
                '%(filename)s:'
                '%(funcName)s:'
                '%(lineno)d:'
                '%(thread)d:\t'
                '%(message)s'), 
        datefmt='%d-%b-%y %H:%M:%S',
        filename="./elevator/logs/runtime.log", filemode='w')
    server.run(host="0.0.0.0", port=8000)