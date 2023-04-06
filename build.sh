 #!/bin/bash
 
 # Build the project

 python setup.py sdist bdist_wheel
 twine upload dist/*
