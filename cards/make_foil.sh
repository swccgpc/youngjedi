#!/bin/bash

exit 1

find light/ dark/ -type f | awk '{
  OUT=$0; 
  gsub("dark/",  "dark-shiny/", OUT); 
  gsub("light/", "light-shiny/", OUT); 
  gsub(".jpg", ".png", OUT); 
  print "composite -dissolve 30 holo.jpg "$0" "OUT;
}'



