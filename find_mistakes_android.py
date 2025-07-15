#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timedelta
import re
import xml.etree.ElementTree as ET

if len(sys.argv) < 3:
	exit()

print(datetime.now(),'start')
timestamp=int(datetime.now().timestamp())

en_tmp_file='%s.%d.txt' % (os.path.splitext(sys.argv[1])[0], timestamp)
others_tmp_file='%s.%d.txt' % (os.path.splitext(sys.argv[2])[0], timestamp)
if len(sys.argv) == 4:
	output_file=sys.argv[3]
print('%s,%s' % (sys.argv[1],sys.argv[2]))
# os.system('cp %s %s' % (sys.argv[1].replace('(','\\(').replace(')','\\)'), en_tmp_file.replace('(','\\(').replace(')','\\)')))
# os.system('cp %s %s' % (sys.argv[2].replace('(','\\(').replace(')','\\)'), others_tmp_file.replace('(','\\(').replace(')','\\)')))
os.system('cp "%s" "%s"' % (sys.argv[1], en_tmp_file))
os.system('cp "%s" "%s"' % (sys.argv[2], others_tmp_file))

en_dict={}
others_dict={}
translatable_false_count=0

try:
	with open (en_tmp_file, 'r') as en:
	# for row in en.readlines():
	# 	key=re.split(r'<it|em>|="|">|</', row)[2]
	# 	string=re.split(r'<it|em>|="|">|</', row)[3]
	# 	print(key,string)
	# 	if key == '' or row == '':
	# 		pass
	# 	else:
	# 		en_dict[key]=string
		tree=ET.parse(en)
		resources=tree.getroot()
		for string in resources.findall('string'):
			translatable=string.get('translatable')
			if translatable == None or translatable != 'false':
				name=string.get('name')
				string=string.text
				# print(name,string)
				en_dict[name]=string
			else:
				translatable_false_count+=1
except Exception as e:
	print(e)
	exit()
	
try:
	with open (others_tmp_file, 'r') as others:
	# for row in others.readlines():
	# 	key=re.split(r'<it|em>|="|">|</', row)[2]
	# 	string=re.split(r'<it|em>|="|">|</', row)[3]
	# 	if key == '' or row == '':
	# 		pass
	# 	else:
	# 		en_dict[key]=string
		tree=ET.parse(others)
		for string in tree.findall('string'):
			name=string.get('name')
			string=string.text
			# print(name,string)
			others_dict[name]=string
except:
	os.remove(en_tmp_file)
	exit()

count=0
size=len(en_dict)
error_count=0
for en_key, en_string in en_dict.items():
	# for others_key, others_string in others_dict.items():
		# print(en_key,en_string)
		# print(others_key,others_string)
		# formatted_text='{0:80}'
	count+=1
	text='(%d/%d)%s,%s' % (count, size, en_key, en_string)
	# print('\r%s' % text[:80], end='')
	others_string=others_dict.get(en_key)
	if others_string != None:
		en_placeholder_count=len(re.findall(r'%[.\ddsf]',str(en_string)))
		others_placeholder_count=len(re.findall(r'%[.\ddsf]',str(others_string)))
		if en_placeholder_count != others_placeholder_count:
			en_digit_count=len(re.findall(r'%(\d\$){0,1}d',str(en_string)))
			others_digit_count=len(re.findall(r'%(\d\$){0,1}d',str(others_string)))
			en_string_count=len(re.findall(r'%(\d\$){0,1}s',str(en_string)))
			others_string_count=len(re.findall(r'%(\d\$){0,1}s',str(others_string)))
			en_float_count=len(re.findall(r'%.{0,1}(\d\$){0,1}f',str(en_string)))
			others_float_count=len(re.findall(r'%.{0,1}(\d\$){0,1}f',str(others_string)))
			print('\n..................................')
			print('%s\n%s' % (en_string, others_string))
			print('%d:%d' % (en_placeholder_count, others_placeholder_count))
			print('%d:{}:{},%s:{}:{},%f:{}:{}'.format(en_digit_count,others_digit_count,en_string_count,others_string_count,en_float_count,others_float_count))
			print('..................................')
		continue
	else:
		# print('\n..................................\n{} not found\n..................................'.format(en_key))
		error_count+=1
print('\nproccessed {} strings\n{} strings is translatable false'.format(count, translatable_false_count))
print('{} strings not found in {}'.format(error_count, others_tmp_file))

os.remove(en_tmp_file)
os.remove(others_tmp_file)
print(datetime.now(),'finish')
