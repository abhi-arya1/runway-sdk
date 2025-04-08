from setuptools import setup, find_packages

setup(
    name='runway-sdk',
    version='0.1.2',
    author='Opennote, Inc.',
    author_email='support@opennote.me',
    description='Runway SDK - Open Source LLM Observability and Monitoring',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/opennote-dev/runway-sdk',
    project_urls={
        'Homepage': 'https://github.com/opennote-dev/runway-sdk',
        'Issues': 'https://github.com/opennote-dev/runway-sdk/issues',
    },
    packages=find_packages(include=['runway', 'runway.*']),
    python_requires='>=3.12',
    install_requires=[
        'inquirer',
        'requests',
        'halo',
        'jupyterlab',
        'nbformat',
        'scikit-learn',
        'tabulate',
        'paramiko',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
)