#!/bin/bash

#Checking the parameter
if [ $# != 1 ];then
        echo -e "Parameter Error! Please check your input. \n Usage: ./stats YOUR_FILE \n Replace YOUR_FILE with your CSV file path.";
    exit
fi

#Checking the file status
if ! [ -f $1 ];then
    echo -e "File Read Error! \n File does not exist \n Please check the file path you entered"
    exit
elif ! [ -r $1 ];then
    echo "File Read Error! \n File can not be read \n Please check the file permissions."
    exit
fi

#Use awk to print the number of lines
awk 'END{print NR}' $1

#use sed to catch the first line of the file
sed -n '1p' $1

#use tail to get the last 10000 rows of the file
#use grep to count the last 10000 rows which contains "potus"
cat $1 | tail -n 10000 | grep -c -i "potus"

#use sed to get the content between 100-200 rows and use grep to count word "fake"
sed -n '100,200p' $1 | grep -c "fake"