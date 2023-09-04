#!/usr/bin/env python3
# coding: utf-8
#
# Forked from S-shangli/exo2sbv.py
# Original gist pandanote-info/exo2srt.py
#

import io
import sys
import os
import re
import codecs
from struct import *

class AviUtlElement:
	"""AviUtlの中でテキストに関連する要素を格納するクラス"""
	def __init__(self):
		self.start = 0
		self.end = 0
		self.text = "";

	def setTextAsUtf8(self,s):
		ss = len(s)
		self.text = ""
		for x in range(0,ss-1,4):
			# print str(x)+","+s[x:x+4]
			c = int(s[x:x+2],16)+int(s[x+2:x+4],16)*256
			if c == 0: break
			self.text += chr(c)
		self.text = re.sub(r"\r?\n","",self.text);
		#print b

def formatForSrt(s):
	if fps_calc!=0:
		fps=fps_calc
	else:
		fps = 60
	sec = float(s%(60*fps))/fps
	hm = s/(60*fps)
	h = int(hm/60)
	m = int(hm%60)
	return ("{0:02d}:{1:02d}:{2:06.3f}".format(h,m,sec));



# check args
if not( len(sys.argv) == 2 ):
    print("Error: invalid args.", file=sys.stderr)
    print("\n使い方: exoファイルをドラッグ＆ドロップしてみてください.\n")
    input("[Enter]キーで終了\n")
    sys.exit(1)


filepath = sys.argv[1]
# check input file
if not os.path.isfile(filepath):
    print(f"Error: \"{filepath}\" is not exist.", file=sys.stderr)
    sys.exit(1)
#print(f"{filepath}")


f_in = open(filepath, 'r' , encoding="CP932")
try:
    lines = f_in.read()
except Exception as e:
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
    print("\n使い方: exoファイルをドラッグ＆ドロップしてみてください.\n")
    input("[Enter]キーで終了\n")
    sys.exit(1)
f_in.close()

sid = 0
element = {}
start_ = 0
end_ = 0
text = ""
fps_calc=0
fps_calc_rate=0
fps_calc_scale=0
exedit_element_flg=0 # 0:not_started 1:probing 2:finished

for line in lines.split("\n"):

	# calculate fps from exofile
	if fps_calc == 0:
		if exedit_element_flg==0:
			m = re.match(r"\[exedit\]",line)
			if m:
				exedit_element_flg += 1
		elif exedit_element_flg==1:
			m = re.match(r"(rate|scale)=(\d+)",line)
			if m:
				if m.group(1) == "rate":
					fps_calc_rate = m.group(2)
				elif m.group(1) == "scale":
					fps_calc_scale = m.group(2)
			else:
				m = re.match(r"^\[",line)
				if m:
					exedit_element_flg += 1
		elif exedit_element_flg==2:
			if ( not(fps_calc_rate == 0) and not(fps_calc_scale == 0) ):
				fps_calc = int(fps_calc_rate) / int(fps_calc_scale)

	m = re.match(r"\[([0-9]+)\]",line)
	if m:
		sid = int(m.group(1))
	else:
		mm = re.search(u'_name=テキスト',line)
		if mm:
			#print("element[" +sid+"]")
			element[sid] = AviUtlElement()
			element[sid].start = start_
			element[sid].end = end_
		else:
			m3 = re.match(r"text=(.+)",line)
			if m3:
				#print("text:" +sid)
				element[sid].setTextAsUtf8(m3.group(1))
			else:
				m4 = re.match(r"(start|end)=(\d+)",line)
				if m4:
					if m4.group(1) == "start":
						start_ = m4.group(2)
					elif m4.group(1) == "end":
						end_ = m4.group(2)


filepath_out = filepath + ".sbv"
f_out = open(filepath_out, 'w' , encoding="UTF-8")

for k,v in sorted(element.items()):
	f_out.write(formatForSrt(int(v.start)-1)+","+formatForSrt(int(v.end))+"\n"+v.text+"\n\n")

f_out.close()

