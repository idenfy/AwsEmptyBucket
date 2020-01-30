## AWS Empty Bucket

A package to empty an S3 bucket before deleting it.

#### Description

A project exposes a custom resource class `EmptyS3` which provides 3 resources:

- A CloudFormation custom resource object
- A custom resource backend (lambda function)
- Backend's role
