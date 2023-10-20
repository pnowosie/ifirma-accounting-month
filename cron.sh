#!/usr/local/bin/bash

## Some of cron.sh good practices
# - make it executable
# - prefer full paths, don't use `~` or ${HOME}
# - override PATH, otherwise you need to provide path to every command
# - to setup `crontab -e` check: https://cron.help 
PATH=/usr/bin:/bin:/usr/local/bin
WORKING_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
LOG_FILE="execution.log"

cd ${WORKING_DIR}
echo "Cron job started: $(date +'%Y-%m-%d %H:%M:%S')" | tee -a  ${LOG_FILE}

make adjust 2>&1 | tee -a ${LOG_FILE}

echo "Cron job stoped:  $(date +'%Y-%m-%d %H:%M:%S')" | tee -a  ${LOG_FILE}
