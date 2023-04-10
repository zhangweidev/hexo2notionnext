 #!/bin/bash
 
 # Build the project
 rm -rf dist/*
 python setup.py sdist bdist_wheel
 twine upload dist/*
