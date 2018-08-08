from setuptools import setup, find_packages

setup(
    name='delay-proxy',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/maribelacosta/delay-proxy',
    license='Apache 2',
    author='Maribel Acosta',
    author_email='maribel.acosta@kit.edu',
    description='An A HTTP proxy that introduces network delays to the response from the server',
    classifiers=("License :: OSI Approved :: Apache Software License", "Topic :: System :: Networking"),
    scripts=['bin/run-delay-proxy']
)
