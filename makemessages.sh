#!/bin/bash
for DIR in temporale demo
do
  cd $DIR
  echo $DIR
  ../manage.py makemessages -a -e html,py,tex,txt
  ../manage.py makemessages -a -e js -d djangojs
  open locale/*/LC_MESSAGES/*.po
  cd ..
done
cd ..
