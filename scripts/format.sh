#!/bin/bash
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

yapf -i -r pytable/
yapf -i -r tests/
