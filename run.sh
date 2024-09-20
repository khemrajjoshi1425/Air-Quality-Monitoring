#!/bin/bash

# Function to stop and remove all Docker containers
cleanup_docker_containers() {
    echo "Stopping all running Docker containers..."
    docker stop $(docker ps -q)
    echo "Removing all Docker containers..."
    docker rm $(docker ps -a -q)
    echo "Docker containers cleaned up!"
}

# Function to start Docker Compose
run_docker_compose() {
    echo "Starting Docker Compose services..."
    docker-compose up -d
    if [ $? -eq 0 ]; then
        echo "Docker Compose started successfully!"
    else
        echo "Failed to start Docker Compose."
        exit 1
    fi
}

# Function to run Telegraf
run_telegraf() {
    sleep 5
    echo "Running Telegraf..."
    telegraf --config telegraf.conf &
    if [ $? -eq 0 ]; then
        echo "Telegraf started successfully!"
    else
        echo "Failed to start Telegraf."
        exit 1
    fi
}

# Function to run Python script
run_python_script() {
    echo "Running Python Producer..."
    python3 producer.py
    if [ $? -eq 0 ]; then
        echo "Python Producer executed successfully!"
    else
        echo "Python Producer execution failed."
        exit 1
    fi
}


# Run the steps
run_python_script
run_docker_compose
run_telegraf

echo "All tasks completed successfully!"
