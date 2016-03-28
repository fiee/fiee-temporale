#!/bin/bash
for DIR in temporale demo demo/biography
do
  cd $DIR
  echo $DIR
  ../manage.py makemessages -a -e html,py,tex,txt
  ../manage.py makemessages -a -d djangojs
  open locale/*/LC_MESSAGES/*.po
  cd ..
done
cd ..
