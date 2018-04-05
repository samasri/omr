import subprocess
import sys

print sys.argv[1]


if sys.argv[1] == 'amd64':
	fileName = 'x86/amd64'
if sys.argv[1] == 'i386':
	fileName = 'x86/i386'
if sys.argv[1] == 'power':
	fileName = 'power'
if sys.argv[1] == 'z':
	fileName = 'z'

fileName = 'sources/getFileList/' + fileName
subprocess.Popen("make", stderr=subprocess.STDOUT, cwd=fileName)