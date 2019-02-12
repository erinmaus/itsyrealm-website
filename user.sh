#!/bin/sh
export FLASK_APP="itsyrealm"
export FLASK_ENV="development"
flask add-user --username ${ITSYREALM_USER} --password ${ITSYREALM_DEFAULT_PASSWORD}