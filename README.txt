Installation
============

mkdir epfl_test
cd epfl_test
git clone https://github.com/JustusW/EPFL.git
git clone https://github.com/solute/pyramid_epfl.git
cd pyramid_epfl
python setup.py develop
cd ../EPFL
python setup.py develop
pserve development.ini