from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='aws_empty_bucket',
    version='2.2.0',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=(
        'AWS CDK package that empties an S3 bucket upon resource deletion.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'aws_cdk.core>=1.44.0,<1.50.0',
        'aws_cdk.aws_iam>=1.44.0,<1.50.0',
        'aws_cdk.custom_resources>=1.44.0,<1.50.0',
        'aws_cdk.aws_s3>=1.44.0,<1.50.0',
        'aws_cdk.aws_s3_deployment>=1.44.0,<1.50.0',
    ],
    author='Laimonas Sutkus',
    author_email='laimonas@idenfy.com, laimonas.sutkus@gmail.com',
    keywords='AWS CDK S3 CustomResource',
    url='https://github.com/idenfy/AwsEmptyBucket.git',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
)
