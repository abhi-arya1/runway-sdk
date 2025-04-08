python3 setup.py sdist bdist_wheel

set -e # Exit on error

python3 -m twine upload --repository pypi dist/*