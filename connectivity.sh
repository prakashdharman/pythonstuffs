#!/bin/bash

check_connectivity() {
    host=$1
    port=$2
    
    nc -z -w 2 $host $port
    
    if [ $? -eq 0 ]; then
        echo "Connected to $host on port $port"
    else
        echo "Connection to $host on port $port failed"
    fi
}

main() {
    hosts=("example.com" "google.com" "facebook.com")
    ports=(80 443 22)  # Example list of ports to check
    
    for host in "${hosts[@]}"; do
        for port in "${ports[@]}"; do
            check_connectivity $host $port
        done
    done
}

main
#######

#!/bin/bash

check_connectivity() {
    host=$1
    port=$2
    
    nc -z -w 2 $host $port
    
    if [ $? -eq 0 ]; then
        echo "Connected to $host on port $port"
    else
        echo "Connection to $host on port $port failed"
        # Check if the port is open but the service is not responding
        nc -z -w 2 $host $port </dev/null &>/dev/null
        if [ $? -eq 0 ]; then
            echo "Port $port is open but service is not responding"
        fi
    fi
}

main() {
    hosts=("example.com" "google.com" "facebook.com")
    ports=(80 443 22)  # Example list of ports to check
    
    for host in "${hosts[@]}"; do
        for port in "${ports[@]}"; do
            check_connectivity $host $port
        done
    done
}

main
