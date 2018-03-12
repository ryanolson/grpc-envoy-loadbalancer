#!/usr/bin/env python3
import contextlib
import logging
import os
import sched
import shutil
import socket
import subprocess
import sys
import tempfile
import time

from pprint import pformat

import click
import yaml


def get_logger(name, level=None):
    level = level or logging.INFO
    log = logging.getLogger(name)
    log.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


log = get_logger(__name__)

@contextlib.contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

def valid_hostname(hostname):
    try:
        addr = socket.gethostbyname(hostname)
        return True
    except:
        pass
    return False


class Endpoint:

    def __init__(self, hostname=None, ip=None, port=None):
        if hostname is None and ip is None:
            raise RuntimeError("either hostname or ip is required")
        if hostname: # if provided - ip always gets overridden by dns lookup
            ip = socket.gethostbyname(hostname)
        self.hostname = hostname
        self.ip = ip
        self.port = port or 80
       
    @property
    def socket_address(self):
        return {"socket_address": {"address": self.ip or self.hostname, "port_value": self.port }} 

    @property
    def eds_endpoint(self):
        return {"endpoint": {"address": self.socket_address}}
        

class BaseDemoController:

    def __init__(self, eds_path=None):
        # all --> all endpoints over the lifetime of the controller
        # endpoints get added, but never removed - this allows us to coninue to disply
        # unhealthy endpoint that have been removed from the k8s apis
        self.all = {}
        self.healthy = {} # all entries should be keys of all
        self.active = set([]) # all entries should be keys of all
        self.active_requested = 2
        self.eds_path = eds_path or "/config/eds.yaml"
        self.version = 0

    def update(self):
        self.update_healthy()
        apply_update = False
        self.all.update(self.healthy)
        healthy = set(self.healthy.keys())
        unhealthy = self.active - healthy
        active = healthy.intersection(self.active)
        available = healthy - active
        if unhealthy:
            log.info("unheathy endpoints removed from active lb list: {}".format(unhealthy))
            apply_update = True
        while len(active) < self.active_requested and available:
            ep = available.pop()
            active.add(ep)
            log.info("adding {} to the active lb list".format(ep))
            apply_update = True
        self.active = active
        if apply_update:
            self.update_eds()

    def update_eds(self):
        self.version = self.version + 1
        eds_response = {
            "version_info": str(self.version),
            "resources": [{
                "@type": "type.googleapis.com/envoy.api.v2.ClusterLoadAssignment",
                "cluster_name": "helloworld",
                "endpoints": [{
                    "lb_endpoints": [ep.eds_endpoint for ep in self.healthy.values()]
                }],
            }],
        }
        log.info("writing new eds response:\n{}".format(pformat(eds_response, indent=2, width=120)))
        dst_eds = os.path.join(os.path.dirname(self.eds_path), "new.yaml")
        with open(dst_eds, "w") as output:
            yaml.dump(eds_response, output)
        with cd(os.path.dirname(self.eds_path)):
            shutil.move("new.yaml", os.path.basename(self.eds_path)) # envoy updates only triggered on a move

    def update_healthy(self):
        raise NotImplementedError()


class DockerComposeDemoController(BaseDemoController):

    def update_healthy(self):
        with open("/config/active", "r") as file:
            data = yaml.load(file)
        endpoints = [Endpoint(hostname=hostname) for hostname in data.get("endpoints", []) if valid_hostname(hostname)]
        self.healthy = {ep.hostname: ep for ep in endpoints}


@click.command()
@click.option("--daemon", is_flag=True)
def demo(daemon):
    controller = DockerComposeDemoController()
    if daemon:
        s = sched.scheduler(time.time, time.sleep)
        def loop():
            controller.update()
            s.enter(2, 1, loop)
        s.enter(0, 1, loop)
        s.run()
    else:
        controller.update()


if __name__ == "__main__":
   demo()
