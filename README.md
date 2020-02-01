## AWS Empty Bucket

A custom S3 bucket with an ability to completely delete itself 
(even if it contains files within).

#### Remarks

The project is written by [Laimonas Sutkus](https://github.com/laimonassutkus) 
and is owned by [iDenfy](https://github.com/idenfy). This is an open source
library intended to be used by anyone. [iDenfy](https://github.com/idenfy) aims
to share its knowledge and educate market for better and more secure IT infrastructure.

#### Related technology

This project utilizes the following technology:

- *AWS* (Amazon Web Services).
- *AWS CDK* (Amazon Web Services Cloud Development Kit).
- *AWS CloudFormation*.
- *AWS S3* (Amazon Web Services Simple Storage Service).

#### Assumptions

This library project assumes the following:

- You have knowledge in AWS (Amazon Web Services).
- You have knowledge in AWS CloudFormation and AWS S3.
- You are managing your infrastructure with AWS CDK.
- You are writing AWS CDK templates with a python language.

#### Install

The project is built and uploaded to PyPi. Install it by using pip.

```bash
pip install aws-empty-bucket
```

Or directly install it through source.

```bash
./build.sh -ic
```

#### Description

Natively S3 buckets can not be deleted if they contain files. If you were to 
delete a bucket through CloudFormation, you would get a similar error message:

> **The bucket you tried to delete is not empty** 
> (Service: Amazon S3; Status Code: 409; Error Code: BucketNotEmpty; 
> Request ID: *<some-id>*; S3 Extended Request ID: 
> *<some-other-id>*)

This gets especially annoying if a developer is spinning up and tearing down
the infrastructure many times a day. Wouldn't it be awesome if S3 buckets could 
just be simply deleted in any case?

With this project you can create S3 buckets that can be deleted even if they
contain filed inside. A project exposes a class `EmptyS3Bucket` which can 
be used exactly the same as a class `Bucket` provided by AWS CDK. Next time
you delete your stack, you will not see that error message again.

#### Examples


To create an S3 Bucket that can be easily deleted create an `EmptyS3Bucket`
instance in your stack. An example is given below:

```python
from aws_cdk import core, aws_s3
from aws_empty_bucket.empty_s3_bucket import EmptyS3Bucket

class MainStack(core.Stack):
    def __init__(self, scope: core.App) -> None:
        super().__init__(
            scope=scope,
            id='MyCoolStack'
        )

        self.empty_bucket = EmptyS3Bucket(
            self,
            'MyCoolBucketThatCanBeDeleted',
            access_control=aws_s3.BucketAccessControl.PRIVATE,
            bucket_name='mybucket',
        )
```

To delete inner S3 Bucket files, a custom resource with a lambda function as
as a backend is created too. `EmptyS3Bucket` exposes two properties:
`backend` and `custom_resource`. If you need to access them use the following:

```python
from aws_empty_bucket.empty_s3_bucket import EmptyS3Bucket

empty_bucket = EmptyS3Bucket(...)

function = empty_bucket.backend
resource = empty_bucket.custom_resource
```
