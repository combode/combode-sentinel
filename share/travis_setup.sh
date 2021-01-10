#!/bin/bash
set -evx

mkdir ~/.combodecore

# safety check
if [ ! -f ~/.combodecore/.combode.conf ]; then
  cp share/combode.conf.example ~/.combodecore/combode.conf
fi
