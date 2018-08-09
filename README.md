[![DOI](https://zenodo.org/badge/144040707.svg)](https://zenodo.org/badge/latestdoi/144040707)

# delay-proxy

An HTTP proxy in Python 2.7 that introduces network delays to the response from a server.

The network delays (in milliseconds) follow a random [Gamma distribution](https://en.wikipedia.org/wiki/Gamma_distribution) with parameters `alpha` and `beta`. 

## Download and Install
Download or clone this repository. Execute the following command in the `delay-proxy` folder. 

```
[sudo] python setup.py install
```

## Execution and Parameters
To start a proxy, execute the following command: 
```
run-delay-proxy port server alpha beta randomseed [buffsize]
```

- `port`: Listening port for the proxy (int).
- `server`: IP address and port of the server (ip:port).
- `alpha`: Alpha parameter for gamma distribution (int).
- `beta`: Beta parameter for gamma distribution (float).
- `randomseed`: Seed for the delays in the proxy (int). Using the same seed allows to reproduce the sequence of delays. 
- `buffsize`:  Buffersize that specifies the size of the data chunks sent to the client (int).

## Example of Usage

In the following example, the proxy listens in the port `8005` and contacts the server `http://127.0.0.1:5000/db`. 
The response from the server is sent to the client with network delays (in milliseconds) that follow a Gamma distribution with parameters `alpha = 10` and `beta = 3.0`. The seed used for generating the delays is `1`. 

```
# Delaying the answer from a server. 
run-delay-proxy 8005 http://127.0.0.1:5000/db 10 3.0 1
```

In the following example, the answer from the server is partitioned in chunks of size `1024` characters. 
Each chunk from the server is sent to the client with the network delays as specified in the previous example. 
```
# Delaying chunks of the answer from a server. 
run-delay-proxy 8005 http://127.0.0.1:5000/db 10 3.0 1 1024 
```

## How to Cite
Use the DOI provided in this README.
