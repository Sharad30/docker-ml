docker build -t tensorboard:latest -f docker-gpu/tensorboard.Dockerfile .
docker build -t pytorch:latest -f docker-gpu/pytorch.Dockerfile .
docker build -t tensorflow:latest -f docker-gpu/tensorflow.Dockerfile .