## Setup
On an ubuntu machine with python3 and pip installed, clone this repository and navigate into it

Install boto3 dependency by running ```pip install -r requirements.txt```

Create a file named ```backup.bash``` with the contents:

```
#!/bin/bash

export BUCKET_NAME=<Name of bucket>
export ACCESS_KEY_ID=<Access key id for user>
export SECRET_ACCESS_KEY=<Secret key for user>
export BACKUP_DIR=<Path to directory to backup (for testing use 'data')>
export BACKUP_HOME=<Path to this repo>

python $BACKUP_HOME/upload.py
```

Then ```sudo chmod +x backup.bash```

Add cron job by running ```crontab -e``` then add the following to the bottom of the file
```
MAILTO=email@address.com
0 0 * * * /home/ubuntu/daily-s3-backup/backup.bash
```
If the repo was cloned into another location the path to ```backup.bash``` should be changed to reflect that

Files will be backed up to S3 at midnight every night
