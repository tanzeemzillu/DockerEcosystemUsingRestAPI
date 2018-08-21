import docker
from flask import Flask, request
import json

import requests
app = Flask(__name__)

"""successful server creation"""


@app.route("/", methods=['GET'])
def test():
    return 'server has been created'


"""Show docker info in json format"""


@app.route("/info", methods=['GET'])
def info():
    try:
        client = docker.from_env()
        docker_info = client.info()
        """load ouput in json format"""
        docker_info_string = (json.dumps(docker_info, indent=4))
        return (docker_info_string)
    except requests.exceptions.HTTPError:
        pass


"""Show image list"""


@app.route("/Ilist", methods=['GET'])
def show_image_list():
    try:
        client = docker.from_env()
        li = client.images.list()
        """iterate through the imagelist and print it in server side"""
        iterator = li.__iter__()
        for i in iterator:
            return str(i)
        return str(li)
    except requests.exceptions.HTTPError:
        pass


"""Show container list"""


@app.route("/Clist", methods=['GET'])
def show_container_list():
    try:
        client = docker.from_env()
        container_list = client.containers.list()
        return ('\n'+'online containers \n'+str(container_list))
    except requests.exceptions.HTTPError:
        pass


"""Pull the image"""


@app.route("/pull", methods=['POST'])
def pull_image_from_hub():
    try:
        client = docker.from_env()
        data = request.get_json()
        imagename = data['imagename']
        pulledimage = client.images.pull(imagename)
        return ("pulled image:" +str(pulledimage))
    except requests.exceptions.HTTPError:
        pass


"""Create Container"""


@app.route("/create", methods=['POST'])
def create_container_from_image():
    try:
        client = docker.from_env()
        data = request.get_json()
        imagename = data['imagename']
        containername = data['containername']
        container = client.containers.create(imagename, detach=True, name=containername)
        return (str(container))
        return ('Created Container Name:'+container.name)
    except requests.exceptions.HTTPError:
        pass


"""Start the container"""


@app.route("/start", methods=['POST'])
def start_container_from_image():
    try:
        client = docker.from_env()
        data = request.get_json()

        """Container is possible to run either with imagename or the containername. But it is not 
         possible to use both value to run a container """

        imagename = data['imagename']
        containername = str(data['containername'])
        client.containers.run(imagename, detach=True, name=containername)
        containerstate = client.containers.get(containername)
        return ('started container'+ str(containerstate))
    except requests.exceptions.HTTPError:
        pass


"""Inspect running container"""


@app.route("/inspectCon", methods=['POST'])
def inspect_running_container():
    try:
        client = docker.from_env()
        data = request.get_json()
        containerID = data['containerID']
        inspect = client.api.inspect_container(containerID)
        """Return in json format"""
        inspect_info = (json.dumps(inspect, indent=4))
        return (inspect_info)
    except requests.exceptions.HTTPError:
        pass


"""Stop all container"""


@app.route("/stop", methods=['GET'])
def stop():
    try:
        client = docker.from_env()
        container_list = client.containers.list()
        for container in container_list:
            container.stop()
        return "All container stoped"
    except requests.exceptions.HTTPError:
        pass


"""Remove all container"""


@app.route("/remove", methods=['DELETE'])
def remove_existing_container():
    try:
        client = docker.from_env()
        delete = client.containers.prune()
        return str(delete)
    except requests.exceptions.HTTPError:
        pass


"""Create Bridge Network"""


@app.route("/networkcreate", methods=['POST'])
def network_create():
    try:
        data = request.get_json()
        networkname = data['networkname']
        subnet = data['subnet']
        iprange = data['iprange']
        gateway = data['gateway']
        ipam_pool = docker.types.IPAMPool(subnet, iprange, gateway)
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        client = docker.from_env()
        networkcreate = client.networks.create(networkname, driver = "bridge", ipam = ipam_config)
        return str(networkcreate) + 'created successfully'
    except requests.exceptions.HTTPError:
        pass


@app.route("/containerexec", methods=['POST'])
def container_exec():
    try:
        client = docker.from_env()
        data = request.get_json()
        imagename = data['imagename']
        containername = str(data['containername'])
        command = str(data['command'])
        container=client.containers.run(imagename, detach=True, name=containername, command=command)
        log = str(container.logs())
        runningcontainer = client.containers.get(containername)
        client.containers.run(containername)
        return "Running container is: " + str(runningcontainer) + "and log is " + str(log)
    except requests.exceptions.HTTPError:
        pass


if __name__ == "__main__":
    app.run()

