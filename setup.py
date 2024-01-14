from setuptools import setup
from os import environ, path, walk

BASE_PATH = path.abspath(path.dirname(__file__))


def get_version():
    """Find the version of the package"""
    version = None
    version_file = path.join(BASE_PATH, "ovos_mark1/version.py")
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if "VERSION_MAJOR" in line:
                major = line.split("=")[1].strip()
            elif "VERSION_MINOR" in line:
                minor = line.split("=")[1].strip()
            elif "VERSION_BUILD" in line:
                build = line.split("=")[1].strip()
            elif "VERSION_ALPHA" in line:
                alpha = line.split("=")[1].strip()

            if (major and minor and build and alpha) or "# END_VERSION_BLOCK" in line:
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(path.join(BASE_PATH, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


def package_files(directory):
    paths = []
    for (p, directories, filenames) in walk(directory):
        for filename in filenames:
            paths.append(path.join('..', p, filename))
    return paths


with open(path.join(BASE_PATH, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="ovos-mark1-utils",
    version=get_version(),
    url="https://github.com/OpenVoiceOS/ovos-mark1-utils",
    license="Apache-2.0",
    install_requires=required("requirements.txt"),
    author="Jarbas",
    author_email="jarbas@openvoiceos.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["ovos_mark1", "ovos_mark1.eyes", "ovos_mark1.faceplate"],
    package_data={"": package_files("ovos_mark1")},
    include_package_data=True,
)
