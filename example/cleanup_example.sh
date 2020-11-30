#!/bin/bash
minikube delete -p foo
minikube delete -p bar

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
rm -rf $DIR/foo $DIR/bar
