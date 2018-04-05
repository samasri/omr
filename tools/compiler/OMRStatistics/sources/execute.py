import subprocess
import sys
import os

if sys.argv[1] == 'amd64':
	fileName = 'x86/amd64'
elif sys.argv[1] == 'i386':
	fileName = 'x86/i386'
elif sys.argv[1] == 'p':
	fileName = 'p'
elif sys.argv[1] == 'z':
	fileName = 'z'
else:
	raise Exception('Argument passed does not represent a supported architecture')

os.environ["ARCH"] = sys.argv[1]

fileName = 'sources/getFileList/' + fileName
p = subprocess.Popen("make", stderr=subprocess.STDOUT, cwd=fileName)
p.wait()