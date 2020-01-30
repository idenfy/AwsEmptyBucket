from setuptools import setup

setup(
    name='empty_s3_bucket',
    version='1.0.0',
    install_requires=[
        'boto3==1.9.215',
        'botocore==1.12.215',
        'cfnresponse==1.0.1'
    ],
)
