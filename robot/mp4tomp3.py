import os


for i in range(3,23):
	print(i)
	os.system("ffmpeg -i %s.mp4 -f mp3 -vn %s.mp3"%(i,i))