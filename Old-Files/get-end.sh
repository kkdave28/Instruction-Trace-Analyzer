#! /bin/bash
readelf -s "$1" | grep -w "main" | awk '{print $3}'