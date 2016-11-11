#!/bin/bash

find . -path "./virt_env" -prune -o -path "./*/migrations" -prune -o -name "*\.py" -exec pep8 --show-source {} \;
