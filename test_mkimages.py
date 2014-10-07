import os, sys
lib_path = os.path.abspath('~/githubs/aipy-damo/build/lib.linux-x86_64-2.7/aipy')
sys.path.insert(0,lib_path)
import aipy
print aipy.__file__
print lib_path
