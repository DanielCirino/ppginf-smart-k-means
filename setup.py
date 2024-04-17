from setuptools import setup, find_packages


def obterRequerimentos(filename):
    return [req.strip()
            for req
            in open(filename).readlines()
            ]


setup(
    name="smart-k-means",
    version="0.1.0",
    description="Smart K-means",
    packages=find_packages(),
    include_package_data=True,
    install_requires=obterRequerimentos("requirements.txt"))
