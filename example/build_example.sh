#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir $DIR/foo $DIR/bar

dirk init $DIR/foo
dirk init $DIR/bar
