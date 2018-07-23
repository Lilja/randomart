# Random.org art

Creates an image, from the random values from random.org which is considered "true random" as opposed to the random that exists within the ordinary computer, "psuedo" random.

## Requirements
* `virtualenv`
* `python 3`

Optionally:

`make`

## Installation
* Download the repository

### Makefile
* Run `make build`.

### Manual steps
* Run `./setup.sh` to create the configuration file, `.env.yaml`.
* Install the dependencies with `virtualenv`, `pip install -r requirements.txt`.


## Api Keys
Since the api of Random.org is limited to a 1000 requests/day, this script uses multiple clients with multiple api keys that rotates every api-call. Just use one key if you're unsure about it.

Request keys [here](https://api.random.org/api-keys/beta).

## Example of `.env.yaml`
```
    keys:
      - example-key-1
      - example-key-2
```
