from utils import make_tarfile, upload_file, file_exists_in_bucket, purge_backups
import os
import sys
import datetime as dt

log = open("backup.log", "a")
sys.stdout = log

DIRECTORY = os.environ['BACKUP_DIR']


output_path = make_tarfile(DIRECTORY)
print('Starting job @ {}'.format(dt.datetime.now()))
print('Successfully compressed {} into {}'.format(DIRECTORY, output_path))
print('Beginning upload...')

upload_file(output_path)

if not file_exists_in_bucket(output_path):
    print('\nVerification of file upload to s3 failed...exiting')
    exit()

print('\nVerified file upload to s3...Cleaning up')
print('Removing backup archive {}'.format(output_path))
os.remove(output_path)

purge_backups()