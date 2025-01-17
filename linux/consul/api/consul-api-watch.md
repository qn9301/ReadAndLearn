

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

* [Watches](#watches)
	* [Watches](#watches-1)
	* [Handlers](#handlers)
	* [Global Parameters](#global-parameters)
	* [Watch Types](#watch-types)
		* [Type: key](#type-key)
		* [Type: keyprefix](#type-keyprefix)
		* [Type: services](#type-services)
		* [Type: nodes](#type-nodes)
		* [Type: service](#type-service)
		* [Type: checks](#type-checks)
		* [Type: event](#type-event)

<!-- /code_chunk_output -->
---


* [Commands: Watch - Consul by HashiCorp ](https://www.consul.io/docs/commands/watch.html)


# Watches

* [Watches - Consul by HashiCorp ](https://www.consul.io/docs/agent/watches.html)


## Watches
Watches are a way of specifying a view of data (e.g. list of nodes, KV pairs, health checks) which is monitored for updates. When an update is detected, an external handler is invoked. A handler can be any executable. As an example, you could watch the status of health checks and notify an external system when a check is critical.

Watches are implemented using blocking queries in the HTTP API. Agents automatically make the proper API calls to watch for changes and inform a handler when the data view has updated.

Watches can be configured as part of the agent's configuration, causing them to run once the agent is initialized. Reloading the agent configuration allows for adding or removing watches dynamically.

Alternatively, the watch command enables a watch to be started outside of the agent. This can be used by an operator to inspect data in Consul or to easily pipe data into processes without being tied to the agent lifecycle.

In either case, the type of the watch must be specified. Each type of watch supports different parameters, some required and some optional. These options are specified in a JSON body when using agent configuration or as CLI flags for the watch command.

## Handlers

The watch configuration specifies the view of data to be monitored. Once that view is updated, the specified handler is invoked. The handler can be any executable.

A handler should read its input from stdin and expect to read JSON formatted data. The format of the data depends on the type of the watch. Each watch type documents the format type. Because they map directly to an HTTP API, handlers should expect the input to match the format of the API.

Additionally, the CONSUL_INDEX environment variable will be set. This maps to the X-Consul-Index value in responses from the HTTP API.

## Global Parameters

In addition to the parameters supported by each option type, there are a few global parameters that all watches support:

* datacenter - Can be provided to override the agent's default datacenter.
* token - Can be provided to override the agent's default ACL token.
* handler - The handler to invoke when the data view updates.

## Watch Types

The following types are supported. Detailed documentation on each is below:

* key - Watch a specific KV pair
* keyprefix - Watch a prefix in the KV store
* services - Watch the list of available services
* nodes - Watch the list of nodes
* service- Watch the instances of a service
* checks - Watch the value of health checks
* event - Watch for custom user events

### Type: key

The "key" watch type is used to watch a specific key in the KV store. It requires that the "key" parameter be specified.

This maps to the /v1/kv/ API internally.

Here is an example configuration:

```json
{
  "type": "key",
  "key": "foo/bar/baz",
  "handler": "/usr/bin/my-key-handler.sh"
}
```
Or, using the watch command:

```sh
$ consul watch -type=key -key=foo/bar/baz /usr/bin/my-key-handler.sh
```
An example of the output of this command:

```json
{
  "Key": "foo/bar/baz",
  "CreateIndex": 1793,
  "ModifyIndex": 1793,
  "LockIndex": 0,
  "Flags": 0,
  "Value": "aGV5",
  "Session": ""
}
```

### Type: keyprefix

The "keyprefix" watch type is used to watch a prefix of keys in the KV store. It requires that the "prefix" parameter be specified. This watch returns all keys matching the prefix whenever any key matching the prefix changes.

This maps to the /v1/kv/ API internally.

Here is an example configuration:

{
  "type": "keyprefix",
  "prefix": "foo/",
  "handler": "/usr/bin/my-prefix-handler.sh"
}
Or, using the watch command:

$ consul watch -type=keyprefix -prefix=foo/ /usr/bin/my-prefix-handler.sh
An example of the output of this command:

[
  {
    "Key": "foo/bar",
    "CreateIndex": 1796,
    "ModifyIndex": 1796,
    "LockIndex": 0,
    "Flags": 0,
    "Value": "TU9BUg==",
    "Session": ""
  },
  {
    "Key": "foo/baz",
    "CreateIndex": 1795,
    "ModifyIndex": 1795,
    "LockIndex": 0,
    "Flags": 0,
    "Value": "YXNkZg==",
    "Session": ""
  },
  {
    "Key": "foo/test",
    "CreateIndex": 1793,
    "ModifyIndex": 1793,
    "LockIndex": 0,
    "Flags": 0,
    "Value": "aGV5",
    "Session": ""
  }
]

### Type: services

The "services" watch type is used to watch the list of available services. It has no parameters.

This maps to the /v1/catalog/services API internally.

An example of the output of this command:

{
  "consul": [],
  "redis": [],
  "web": []
}
### Type: nodes

The "nodes" watch type is used to watch the list of available nodes. It has no parameters.

This maps to the /v1/catalog/nodes API internally.

An example of the output of this command:

[
  {
    "Node": "nyc1-consul-1",
    "Address": "192.241.159.115"
  },
  {
    "Node": "nyc1-consul-2",
    "Address": "192.241.158.205"
  },
  {
    "Node": "nyc1-consul-3",
    "Address": "198.199.77.133"
  },
  {
    "Node": "nyc1-worker-1",
    "Address": "162.243.162.228"
  },
  {
    "Node": "nyc1-worker-2",
    "Address": "162.243.162.226"
  },
  {
    "Node": "nyc1-worker-3",
    "Address": "162.243.162.229"
  }
]
### Type: service

The "service" watch type is used to monitor the providers of a single service. It requires the "service" parameter and optionally takes the parameters "tag" and "passingonly". The "tag" parameter will filter by tag, and "passingonly" is a boolean that will filter to only the instances passing all health checks.

This maps to the /v1/health/service API internally.

Here is an example configuration:

{
  "type": "service",
  "service": "redis",
  "handler": "/usr/bin/my-service-handler.sh"
}
Or, using the watch command:

```sh
$ consul watch -type=service -service=redis /usr/bin/my-service-handler.sh
```
An example of the output of this command:
```json
[
  {
    "Node": {
      "Node": "foobar",
      "Address": "10.1.10.12"
    },
    "Service": {
      "ID": "redis",
      "Service": "redis",
      "Tags": null,
      "Port": 8000
    },
    "Checks": [
      {
        "Node": "foobar",
        "CheckID": "service:redis",
        "Name": "Service 'redis' check",
        "Status": "passing",
        "Notes": "",
        "Output": "",
        "ServiceID": "redis",
        "ServiceName": "redis"
      },
      {
        "Node": "foobar",
        "CheckID": "serfHealth",
        "Name": "Serf Health Status",
        "Status": "passing",
        "Notes": "",
        "Output": "",
        "ServiceID": "",
        "ServiceName": ""
      }
    ]
  }
]
```
### Type: checks

The "checks" watch type is used to monitor the checks of a given service or those in a specific state. It optionally takes the "service" parameter to filter to a specific service or the "state" parameter to filter to a specific state. By default, it will watch all checks.

This maps to the /v1/health/state/ API if monitoring by state or /v1/health/checks/ if monitoring by service.

An example of the output of this command:

[
  {
    "Node": "foobar",
    "CheckID": "service:redis",
    "Name": "Service 'redis' check",
    "Status": "passing",
    "Notes": "",
    "Output": "",
    "ServiceID": "redis",
    "ServiceName": "redis"
  }
]
### Type: event

The "event" watch type is used to monitor for custom user events. These are fired using the consul event command. It takes only a single optional "name" parameter which restricts the watch to only events with the given name.

This maps to the v1/event/list API internally.

Here is an example configuration:

{
  "type": "event",
  "name": "web-deploy",
  "handler": "/usr/bin/my-deploy-handler.sh"
}
Or, using the watch command:

$ consul watch -type=event -name=web-deploy /usr/bin/my-deploy-handler.sh
An example of the output of this command:

[
  {
    "ID": "f07f3fcc-4b7d-3a7c-6d1e-cf414039fcee",
    "Name": "web-deploy",
    "Payload": "MTYwOTAzMA==",
    "NodeFilter": "",
    "ServiceFilter": "",
    "TagFilter": "",
    "Version": 1,
    "LTime": 18
  },
  ...
]
To fire a new web-deploy event the following could be used:

$ consul event -name=web-deploy 1609030