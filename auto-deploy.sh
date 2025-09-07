#! /bin/bash

## build
doxygen doxygen.conf
rsync -av --delete --progress tmp/html/ asymptote-doc --exclude .git

## deploy
git -C asymptote-doc add .
git -C asymptote-doc commit -a -m "auto deploy"
git -C asymptote-doc push origin master


## cleanup
rm -rf tmp
git commit -a -m "auto deploy"
git push origin master


