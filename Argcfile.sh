#!/usr/bin/env bash

set -e




# @cmd test and source env
testProj ()
{
  source ".venv/bin/activate"
  pytest
  
}




# See more details at https://github.com/sigoden/argc
eval "$(argc --argc-eval "$0" "$@")"







