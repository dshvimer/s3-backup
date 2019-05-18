On an ubuntu machine, clone this repository and navigate into it

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

Run ```sudo chmod +x install.bash```
Then ```sudo chmod +x backup.bash```

Install the Cron job by running ```./install.bash```

Run ```crontab -d``` then the following to the file
```
MAILTO=dshvimer@protonmail.com
0 0 * * * /home/ubuntu/daily-s3-backup/backup.bash
```

Enjoy the backed up files
