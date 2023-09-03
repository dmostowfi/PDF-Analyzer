#
# Python program to open and process a PDF file, extracting
# all numeric values from the document. The goal is to tally
# the first significant (non-zero) digit of each numeric
# value, and save the results to a text file. This will
# allow checking to see if the results follow Benford's Law,
# a common method for detecting fraud in numeric data.
#
# https://en.wikipedia.org/wiki/Benford%27s_law
# https://chance.amstat.org/2021/04/benfords-law/
#

from configparser import ConfigParser
from pypdf import PdfReader

import string
import os
import pathlib
import boto3

#
# execution starts here:
#
try:
  print("**STARTED**")

  #
  # setup AWS S3 access that we'll need eventually:
  #
  config_file = 'credentials.txt'
  s3_profile = 's3-read-write'

  os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
  boto3.setup_default_session(profile_name=s3_profile)

  configur = ConfigParser()
  configur.read(config_file)
  bucketname = configur.get('s3', 'bucket_name')

  s3 = boto3.resource('s3')
  bucket = s3.Bucket(bucketname)

  #
  # file to operate on, and file to output results:
  #
  
  #download file to operate on
  bucketkey = "update09.pdf" #previously
  bucket.download_file(bucketkey, bucketkey)
  #filename for results
  bucketkey_results = pathlib.Path(bucketkey).stem + ".txt"

  #
  # open pdf file:
  #
  print("**PROCESSING '", bucketkey, "'**")

  reader = PdfReader(bucketkey)
  number_of_pages = len(reader.pages)
  counter = [0,0,0,0,0,0,0,0,0,0]

  #
  # for each page, extract text, split into words,
  # and see which words are numeric values:
  #
  pages = reader.pages
  for page in pages:
    text = page.extract_text()
    words = text.split()
    for word in words:
      # remove punctuation from word:
      word = word.translate(str.maketrans('', '', string.punctuation))
      if word.isnumeric():
        #print(word)
        digits = list(word) #split the # into an array (still strings) #[1,2,3]
        #print(digits)
        for digit in digits: 
          digit = int(digit) #convert to an int
          if digit == 0:
            continue
          else:   
            i = digit #i = 2
            counter[i] = counter[i] + 1
            break #don't iterate through the digits unless you need to
      else:
        continue #continue to next word


  #print("** Page", 0, ", text length", len(text), ", num words", len(words))

  #
  # we've analyzed the PDF, so print the results to
  # the console but also to the results .txt file:
  #

  def printresults():
    results = f"**RESULTS**\n{number_of_pages} pages"
    for i in range(len(counter)):
      results += f"\n{i} {counter[i]}"
    return results

  #print to the console
  results = printresults()
  print(results)
  
  
  #print to the .txt file
  outfile = open(bucketkey_results, "w")
  outfile.write(results)
  outfile.close()

  #upload .txt file to bucket
  bucket.upload_file(bucketkey_results,
                     bucketkey_results,
                     ExtraArgs = {
                       'ACL': 'public-read',
                       'ContentType': 'text/plain'
                     })

  print("**DONE**")


except Exception as err:
  #print to console
  print("**ERROR**")
  print(str(err))
  
  #print to txt file
  outfile = open(bucketkey_results, "w")
  outfile.write("**ERROR**\n")
  outfile.write(str(err))
  outfile.write("\n")
  outfile.close()
  bucket.upload_file(bucketkey_results,
                    bucketkey_results,
                    ExtraArgs = {
                      'ACL': 'public-read',
                      'ContentType': 'text/plain'
                    })
  
  print("**DONE**")