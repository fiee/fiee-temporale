#!/bin/bash
for DIR in temporale demo
do
  cd $DIR
  echo $DIR
  django-admin makemessages -a -e html,py,tex,txt
  django-admin makemessages -a -e js -d djangojs
  open locale/*/LC_MESSAGES/*.po
  cd ..
done
cd ..
