#!/bin/bash

QUERY="${query}"
DATABASE="${database}"

chmod u+x /iplant/home/rosysnake/workaround/lib/makeblastdb
chmod u+x /iplant/home/rosysnake/workaround/lib/blastn

/iplant/home/rosysnake/workaround/lib/./makeblastdb -dbtype nucl -in $DATABASE -out db
/iplant/home/rosysnake/workaround/lib/./blastn -query $QUERY -db db

return $!;
