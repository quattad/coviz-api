#!/bin/bash

# ^ shebang to specify this is a bash file

app="docker.test"
docker build -t ${app}

# start docker on daemon mode(as a bg process) and bind port onto server
# mount entire project dir on Docker container
docker run -d -p 56733:80 \
    --name=${app} \
    -v $PWD:/app ${app}