
t: file3
	echo t


# file3: file2
# 	echo file3 > file3

file2: file1
	echo file2 > file2

file1: 
	echo file1 > file1
