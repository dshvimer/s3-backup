import os
import sys
import threading
import logging
import glob
import boto3
from botocore.exceptions import ClientError
import time
import tarfile
import datetime as dt

TIMESTAMP_FORMAT = "%Y-%m-%d-%H:%M:%S"
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
BUCKET_NAME = os.environ['BUCKET_NAME']


def make_tarfile(source_dir):
    output_path = '{}.tar.gz'.format(get_current_timestamp())
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return output_path

def get_current_timestamp():
    return time.strftime(TIMESTAMP_FORMAT)

def purge_backups():
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    for obj in bucket.objects.all():
        timestamp = obj.key.split('.')[0]
        backup_date = dt.datetime.strptime(timestamp, TIMESTAMP_FORMAT)
        week_ago = dt.datetime.now() - dt.timedelta(days=7)
        if backup_date < week_ago:
            print('Purging {}'.format(obj.key))
            obj.delete()
    
def file_exists_in_bucket(key):
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    objs = list(bucket.objects.filter(Prefix=key))
    if len(objs) > 0 and objs[0].key == key:
        return True
    else:
        return False

def upload_file(file_name):
    object_name = file_name
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
    )
    s3 = session.resource('s3')
    try:
        
        s3.meta.client.upload_file(file_name, BUCKET_NAME, object_name, Callback=ProgressPercentage(file_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()