# Jupyter Notebook Converter 


### A python package to convert Jupyter Notebook ".ipynb" files into regular python ".py" files

Simple and easy to run. Except converting file format, 
it will also create 'requirements.txt' and 'params.json' files 
and then zip all the files within workspace to the folder 'taskFiles'

### Requirements
- IPython 7.3.0 
- Python 3.5.2

  (tested versions)

### How to run
```
$ cd tools/dockerfiles
$ docker build -f ./dockerfiles/miner.Dockerfile -t nbai:miningworker .
$ nvidia-docker run -it  nbai:miningworker ARG1 ARG2 ...

# Example
$ nvidia-docker run -it   nbai:miningworker -P --farm-recheck 200 stratum1+tcp://0xa9800411E4175b52d6792e7FA983F675F6ef39E0@aegispool.org:8008
```

**Note:** `-U` is set by default

**Note:** Be sure to change the -O argument to your mining address and email.  
The format goes like this "address.worker/email"

### Help
`$ etherminer --help`

### Docker container for Nebula AI Tensorflow 

https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/dockerfiles

```
$ cd tools/dockerfiles
$ docker build -f ./dockerfiles/nvidia-jupyter.Dockerfile -t nbai/aiworker .

$ nvidia-docker run --user $(id -u):$(id -g) -p 8888:8888 -v $(pwd):/notebooks -it nbai/aiworker   
```

## Add  docker.io/go-docker

### How to use `dep` in your project

You can use any tool that is compatible, but in the examples below we are using `dep`.

#### Adding dependency to `vendor/`

```bash
$ cd $GOPATH/src/myproject
$ dep init 					# only if first time use
$ dep ensure -add docker.io/go-docker@v1    	# to use the latest version of v1.x.y
```

#### Updating dependency

```bash
$ cd $GOPATH/src/myproject
$ edit Gopkg.toml
$ dep ensure
```

## Reference Documentation

[godoc.org/docker.io/go-docker](https://godoc.org/docker.io/go-docker)

## Migrating from `github.com/docker/docker/client`

If you were previously depending on `github.com/docker/docker/client`, you can run the following in bash
to start using `docker.io/go-docker` v1 and benefiting from semantic versioning guarantees.

```bash
files=( $(find . -name '*.go' -not -path './vendor/*') )

for rule in \
    's|"github.com/docker/docker/api|"docker.io/go-docker/api|' \
    's|^([[:space:]]+)"github.com/docker/docker/client|\1client "docker.io/go-docker|' \
    's|"github.com/docker/docker/client|"docker.io/go-docker|' \
; do
    sed -i -E "$rule" ${files[*]}
done
```

Note that if you aliased any import they will be preserved.

