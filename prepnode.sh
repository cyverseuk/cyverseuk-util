# install puppet and sets up hosts on new nodes

#!/bin/bash

hostname=`hostname`
sed -i "s/\([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\)\tlocalhost/\1\t$hostname localhost/" /etc/hosts

echo 10.0.72.94	puppet >> /etc/hosts

apt update && apt install -y puppet

puppet agent --enable
puppet agent --test --noop
