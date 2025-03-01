#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Check status of docker service
# Service is CRIT if its status is not up
#
# Author: lars.getwan@metrosystems.net
#
# 
# Plugin output:
#
# <<<docker_info:sep(58)>>>
# service:up
# images:3
# go_routines:34
# file_descriptors:29
# events_listeners:0

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    register,
    Result,
    Service,
    State,
)

def discover_docker_info(section):
    for line in section:
        if line[0] == 'service':
            yield Service()
            return


def check_docker_info(section):
    for line in section:
        if  line[0] == 'service':
            service = line[1]

            if service == 'up':
                yield Result(state=State.OK, summary="service = up")
            else:
                yield Result(state=State.CRIT, summary="service = %s" % service)

        for var in ('images','go_routines','file_descriptors','events_listeners'):
            if line[0] == var:
                yield Result(state=State.OK, summary="%s = %s" % (line[0],line[1]))
                yield Metric(line[0], int(line[1]))


register.check_plugin(
    name="docker_info",
    service_name="Docker Info",
    discovery_function=discover_docker_info,
    check_function=check_docker_info,
)
