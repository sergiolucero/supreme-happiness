import glob
from awslib import *

client = boto3.client('textract')

resps = {}

for fn in glob.glob('IICORTOS/*.pdf'):
    print(fn)
    response = client.start_document_text_detection(
                   DocumentLocation={'S3Object': {'Bucket': 'discosferreiro', 
                                                  'Name': fn} },
                   #ClientRequestToken=random.randint(1,1e10),
                   )

    resps[fn] = response #client.get_document_text_detection(JobId=jobid)
