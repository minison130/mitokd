#!/bin/bash

THIS_DIR=$(cd $(dirname $0);pwd)

coverage run -m unittest discover ./
coverage report -m
