import os
import os.path

def dirlist(rootdir):
	tmp = ''
	
	filelist = os.listdir(rootdir)
	for filename in filelist:
		current_dir = os.path.join(rootdir, filename).replace('\\', '/')
		if os.path.isdir(current_dir):
			tmp += filename + dirlist(current_dir) + ','

	if tmp != '':
		tmp = '(' + tmp[:-1] + ')'
	return tmp


if __name__ == '__main__':
	print(dirlist("D:/photos"))
