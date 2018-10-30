import os
import srt
import io
import re
from nltk.corpus import stopwords

s = set(stopwords.words('english'))

# -*- coding: utf-8 -*-


#### utils

def is_time_stamp(l):
  if l[:2].isnumeric() and l[2] == ':':
    return True
  return False

def has_letters(line):
  if re.search('[a-zA-Z]', line):
    return True
  return False

def has_no_text(line):
  l = line.strip()
  if not len(l):
    return True
  if l.isnumeric():
    return True
  if is_time_stamp(l):
    return True
  if l[0] == '(' and l[-1] == ')':
    return True
  if l[0] == '{' and l[1] == '\\':
    return True
  if not has_letters(line):
    return True
  return False

def is_lowercase_letter_or_comma(letter):
  if letter.isalpha() and letter.lower() == letter:
    return True
  if letter == ',':
    return True
  return False

def clean_up(lines):
  """
  Get rid of all non-text lines and
  try to combine text broken into multiple lines
  """
  new_lines = []
  for line in lines[1:]:
    if has_no_text(line):
      continue
    elif len(new_lines) and is_lowercase_letter_or_comma(line[0]):
      #combine with previous line
      new_lines[-1] = new_lines[-1].strip() + ' ' + line
    else:
      #append line
      new_lines.append(line)
  return new_lines

####

def main():
  file_list = os.listdir('/Users/jbh/Desktop/daredevil_srt')
  file_encoding = 'utf-8' 

  for file_name in file_list:
    print(file_name)
    f = io.open(os.path.join('/Users/jbh/Desktop/daredevil_srt',file_name),mode="r", encoding="utf-8")
    lines = f.readlines()
    # clean up all non-text elements from srt file
    new_lines = clean_up(lines)

    if not os.path.exists('srt_txt'):
      os.makedirs('srt_txt')
    # save the cleaned lines to .txt file
    new_file_name = 'srt_txt/' + file_name[:-4] + '.txt'
    with open(new_file_name, 'w') as f:
      for line in new_lines:
        # remove punctuation
        line = re.sub(r'[^\w\s]','',line)
        # remove short words
        shortword = re.compile(r'\W*\b\w{1,3}\b')
        line = shortword.sub('',line)
        f.write(line.encode('utf-8'))

  file_list = os.listdir('srt_txt')

  for file_name in file_list:
    word_list = []
    print(file_name)
    with open(os.path.join('/Users/jbh/Desktop/srt_txt',file_name), 'r') as f:
      for line in f:
        # lowercase the string
        word_list.extend((line.lower()).split())
    # exclude duplicated words
    word_list = set(word_list)
    word_list = sorted(list(word_list))

    if not os.path.exists('word_list'):
      os.makedirs('word_list')
    # save word list
    with open('word_list/'+file_name[:-4]+'_words.txt', 'w') as f:
      for word in word_list:
        if not word in s:
          f.write(word + '\n')



if __name__ == '__main__':
  main()