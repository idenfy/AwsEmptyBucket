from aws_cdk import core
from aws_cdk.aws_cloudformation import CustomResourceProvider, CustomResource
from aws_cdk.aws_iam import Role, PolicyStatement, PolicyDocument, Effect, CompositePrincipal, ServicePrincipal, IRole
from aws_cdk.aws_lambda import Code, Runtime, IFunction, Function
from aws_cdk.aws_s3 import IBucket
from aws_cdk.core import Duration, RemovalPolicy
from aws_empty_bucket.package import package_root


class EmptyS3:
    """
    Custom CloudFormation resource which empties an S3 bucket on delete event.
    """
    def __init__(
            self,
            stack: core.Stack,
            prefix: str,
            bucket: IBucket,
    ) -> None:
        """
        Constructor.

        :param stack: A stack in which the resource should be placed.
        :param prefix: Prefix for resource names.
        :param bucket: A bucket to depend on and delete its contents upon stack deletion.
        """
        self.__role = Role(
            scope=stack,
            id=prefix + 'EmptyS3Role',
            role_name=prefix + 'EmptyS3Role',
            assumed_by=CompositePrincipal(
                ServicePrincipal("lambda.amazonaws.com"),
                ServicePrincipal("cloudformation.amazonaws.com")
            ),
            inline_policies={
                prefix + 'EmptyS3Policy': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                's3:ListBucket',
                                's3:HeadBucket',
                            ],
                            effect=Effect.ALLOW,
                            resources=[bucket.bucket_arn]
                        ),
                        PolicyStatement(
                            actions=[
                                's3:GetObject',
                                's3:DeleteObject'
                            ],
                            effect=Effect.ALLOW,
                            resources=[bucket.arn_for_objects('*')]
                        )
                    ]
                )
            },
            managed_policies=[]
        )

        self.__custom_backend = Function(
            scope=stack,
            id=prefix + 'CustomEmptyS3Backend',
            code=Code.from_asset(
                path=package_root
            ),
            handler='handler',
            runtime=Runtime.PYTHON_3_6,
            description=f'A custom resource backend to empty {prefix} S3 buckets.',
            function_name=prefix + 'CustomEmptyS3Backend',
            memory_size=128,
            role=self.__role,
            timeout=Duration.seconds(900),
        )

        # noinspection PyTypeChecker
        self.__custom_resource = CustomResource(
            scope=stack,
            id=prefix + "CustomEmptyS3Resource",
            provider=CustomResourceProvider.from_lambda(self.__custom_backend),
            removal_policy=RemovalPolicy.DESTROY,
            resource_type='EmptyS3'
        )

        # Make sure bucket is created when applying this custom resource.
        # In case of deletion this custom resource will be executed before s3 deletion
        # effectively deleting all inner objects.
        self.__custom_resource.node.add_dependency(bucket)

    @property
    def backend(self) -> IFunction:
        return self.__custom_backend

    @property
    def backend_role(self) -> IRole:
        return self.__role

    @property
    def custom_resource(self) -> CustomResource:
        return self.__custom_resource
