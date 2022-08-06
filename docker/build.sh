docker build -t mlcpu:latest -f docker-cpu/mlcpu.Dockerfile .

docker build -t trainingqueue:latest -f servers/trainingqueue.Dockerfile .
docker build -t trainingclient:latest -f servers/trainingclient.Dockerfile .
docker build -t codeserver:latest -f servers/codeserver.Dockerfile .
docker build -t dataserver:latest -f servers/dataserver.Dockerfile .


# docker build -t tensorboard:latest -f docker-gpu/tensorboard.Dockerfile .
# docker build -t pytorch:latest -f docker-gpu/pytorch.Dockerfile .
# docker build -t tensorflow:latest -f docker-gpu/tensorflow.Dockerfile .