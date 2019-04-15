#!/bin/sh

# size of swapfile in megabytes
#may needs to execute as sudo user 
# Only Root User can do this Swap

swapsize=512
# does the swap file already exist?
grep -q "swapfile" /etc/fstab

# if not then create it
if [ $? -ne 0 ]; then
    echo 'swapfile not found. Adding swapfile.'
    #fallocate -l 1G /swapfile
    dd if=/dev/zero of=/swapfile count=4096 bs=1MiB
    chmod 600 /swapfile
    mkswap /swapfile
    #swapon /swapfile
    swapon -a 
    swapon -s 
    echo '/swapfile none swap defaults 0 0' >> /etc/fstab
else
    echo 'swapfile found. No changes made.'
fi

# output results to terminal
cat /proc/swaps
cat /proc/meminfo | grep Swap
swapon -a
free -h

###### END OF Swap Script ###################