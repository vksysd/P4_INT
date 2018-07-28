P4APPRUNNER=../utils/p4apprunner.py
mkdir -p build
tar -czf build/p4app.tgz * --exclude='build'
#cd build
sudo python $P4APPRUNNER p4app.tgz --build-dir ./build
