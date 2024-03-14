#!/usr/bin/env bash
source container/.dockerenv
# Parse command line arguments for the GPU option
while getopts "g:" opt; do
  case $opt in
    g) gpu=$OPTARG ;;
    \?) echo "Invalid option -$OPTARG" >&2
        exit 1 ;;
  esac
done

# Check if GPU argument was provided
if [ -z "$gpu" ]; then
  echo "GPU argument (-g) is mandatory"
  exit 1
fi

# Now you can use the $gpu variable to decide which GPU to use
# For demonstration, we're just echoing the selected GPU


# docker build --no-cache --rm -t ${IMAGE_NAME} .
# DOCKER_BUILDKIT=0 docker build --rm -t ${IMAGE_NAME} . -f container/Dockerfile --build-arg MODEL=${MODEL}
docker build --rm -t ${IMAGE_NAME} . -f container/Dockerfile --build-arg MODEL=${MODEL}

echo "Using GPU: $gpu for training"

cd container && ./docker_run.sh -i -g $gpu -c "bash /run_spacy_commands.sh"
