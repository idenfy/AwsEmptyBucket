import boto3

from typing import Any, Dict


class Action:
    S3_CLIENT = boto3.client('s3')

    @staticmethod
    def create(**kwargs) -> Dict[str, Any]:
        pass

    @staticmethod
    def update(**kwargs: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @staticmethod
    def delete(**kwargs: Dict[str, Any]) -> Dict[str, Any]:
        bucket = kwargs['bucketName']

        bucket = Action.S3_CLIENT.Bucket(bucket)
        for obj in bucket.objects.filter():
            Action.S3_CLIENT.Object(bucket.name, obj.key).delete()

        return {}
