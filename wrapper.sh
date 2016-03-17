#!/bin/bash

QUERY="${query}"
DATABASE="${database}"

lib/./makeblastdb -dbtype nucl -in $DATABASE -out db
lib/./blastn -query $QUERY -db db

return $!;
