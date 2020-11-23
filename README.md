# README

Docker network build:
    docker network create my_socket_ipc_network

In master folder server build commands:
    docker build -t tutti_master .
    docker run --rm -it --network=my_socket_ipc_network --name ipc_server_dns_name tutti_master

In slave folder crawler build commands:
    docker build -t tutti_slave .
    docker run --rm -it --network=my_socket_ipc_network tutti_slave

To stop all containers:
    docker stop $(docker ps -aq)