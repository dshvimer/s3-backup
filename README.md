## Setup

On a fresh AWS EC2 Ubuntu 18 instance, install the following packages:

```
sudo apt update
sudo apt install python3.7
sudo apt install python3-pip
sudo apt install mailutils
> Select 'Internet Site'
> Select default domain
```

Clone this repo then enter into the new directory (```s3-backup```) by default

Install boto3 dependency by running ```pip3 install -r requirements.txt```

Create a file named ```backup.bash``` with the contents:

```
#!/bin/bash

export BUCKET_NAME=<Name of bucket>
export ACCESS_KEY_ID=<Access key id for user>
export SECRET_ACCESS_KEY=<Secret key for user>
export BACKUP_DIR=<Path to directory to backup (for testing use 'data')>
export BACKUP_HOME=<Path to this repo>
export EMAIL=<Email address>

python $BACKUP_HOME/upload.py; cat $BACKUP_HOME/backup.log | mail $EMAIL
```

Then ```sudo chmod +x backup.bash```

Add cron job by running ```crontab -e``` then add the following to the bottom of the file
```
0 0 * * * /home/ubuntu/s3-backup/backup.bash
```
If the repo was cloned into another location the path to ```backup.bash``` should be changed to reflect that

Files will be backed up to S3 at midnight every night. An email is sent with the log file contents
