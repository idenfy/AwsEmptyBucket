from typing import Optional, List
from aws_cdk.aws_cloudformation import CustomResource, CustomResourceProvider, ICustomResourceProvider
from aws_cdk.aws_iam import Role, CompositePrincipal, ServicePrincipal, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_kms import IKey
from aws_cdk.aws_lambda import IFunction, Runtime, Code, Function
from aws_cdk.aws_s3 import *
from aws_cdk.core import Stack, RemovalPolicy, Duration
from aws_empty_bucket.package import package_root


class EmptyS3Bucket(Bucket):
    def __init__(
            self, 
            scope: Stack,
            id: str,
            access_control: Optional[BucketAccessControl] = None,
            block_public_access: Optional[BlockPublicAccess] = None,
            bucket_name: Optional[str] = None,
            cors: Optional[List[CorsRule]] = None,
            encryption: Optional[BucketEncryption] = None,
            encryption_key: Optional[IKey] = None,
            lifecycle_rules: Optional[List[LifecycleRule]] = None,
            metrics: Optional[List[BucketMetrics]] = None,
            public_read_access: Optional[bool] = None,
            removal_policy: Optional[RemovalPolicy] = None,
            server_access_logs_bucket: Optional[IBucket] = None,
            server_access_logs_prefix: Optional[str] = None,
            versioned: Optional[bool] = None,
            website_error_document: Optional[str] = None,
            website_index_document: Optional[str] = None,
            website_redirect: Optional[RedirectTarget] = None,
            website_routing_rules: Optional[List[RoutingRule]] = None,
            **kwargs
    ) -> None:
        assert bucket_name, 'Bucket name must be provided!'
        removal_policy = removal_policy or RemovalPolicy.DESTROY

        known_args = dict(
            scope=scope,
            id=id,
            access_control=access_control,
            block_public_access=block_public_access,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        unknown_args = kwargs

        super().__init__(
            **{
                **known_args,
                **unknown_args
            }
        )

        self.__role = Role(
            scope=scope,
            id=bucket_name + 'Role',
            role_name=bucket_name + 'Role',
            assumed_by=CompositePrincipal(
                ServicePrincipal("lambda.amazonaws.com"),
                ServicePrincipal("cloudformation.amazonaws.com")
            ),
            inline_policies={
                bucket_name + 'Policy': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                's3:ListBucket',
                                's3:HeadBucket',
                            ],
                            effect=Effect.ALLOW,
                            resources=[f'arn:aws:s3:::{bucket_name}']
                        ),
                        PolicyStatement(
                            actions=[
                                's3:GetObject',
                                's3:DeleteObject'
                            ],
                            effect=Effect.ALLOW,
                            resources=[f'arn:aws:s3:::{bucket_name}/*']
                        ),
                        PolicyStatement(
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            effect=Effect.ALLOW,
                            resources=['*']
                        ),
                    ]
                )
            },
            managed_policies=[]
        )

        self.__custom_backend = Function(
            scope=scope,
            id=bucket_name + 'Backend',
            code=Code.from_asset(
                path=package_root
            ),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_6,
            description=f'A custom resource backend to empty {bucket_name} bucket.',
            function_name=bucket_name + 'Backend',
            memory_size=128,
            role=self.__role,
            timeout=Duration.seconds(900),
        )

        provider: ICustomResourceProvider = CustomResourceProvider.from_lambda(self.__custom_backend)

        self.__custom_resource = CustomResource(
            scope=scope,
            id=bucket_name + 'CustomResource',
            provider=provider,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'bucketName': bucket_name
            },
            resource_type='Custom::EmptyS3Bucket'
        )

        # Make sure that custom resource is deleted before lambda function backend.
        self.__custom_resource.node.add_dependency(self.__custom_backend)
        # Make sure that custom resource is deleted before the bucket.
        self.__custom_resource.node.add_dependency(self)

    @property
    def backend(self) -> IFunction:
        return self.__custom_backend

    @property
    def custom_resource(self) -> CustomResource:
        return self.__custom_resource
