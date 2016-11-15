cd ./attachments

chmod 700 curls.sh

./curls.sh

TS=`date +'%Y%m%d.%H%M%S'`
zip json_result.$TS.zip *.json

rm *.json
rm *.txt
rm curls.sh