import boto3
import logging

from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Action:
    S3_RESOURCE = boto3.resource('s3')

    @staticmethod
    def create(**kwargs) -> Dict[str, Any]:
        logger.info('Not doing anything since this backend only deletes files upon delete event.')
        return {'status': 'skipped'}

    @staticmethod
    def update(**kwargs: Dict[str, Any]) -> Dict[str, Any]:
        logger.info('Not doing anything since this backend only deletes files upon delete event.')
        return {'status': 'skipped'}

    @staticmethod
    def delete(**kwargs: Dict[str, Any]) -> Dict[str, Any]:
        bucket = kwargs.get('bucketName', kwargs.get('BucketName', kwargs.get('bucket_name')))
        logger.info(f'Deleting all inner files for bucket {bucket}...')

        bucket = Action.S3_RESOURCE.Bucket(bucket)
        for obj in bucket.objects.filter():
            logger.info(f'Deleting {obj.key}...')
            Action.S3_RESOURCE.Object(bucket.name, obj.key).delete()

        return {'status': 'deleted'}
