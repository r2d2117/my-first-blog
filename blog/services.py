from googleapiclient.discovery import build
from django.core import serializers
import json
from io import StringIO


def get_books_data(query):
    """Retriving data from google books API"""

    service = build('books',
                    'v1',
                    developerKey='AIzaSyB5mHR4XBZkZNkSLVB_uaLAVUZxLUInzsQ'
                    )
    request = service.volumes().list(q=query)
    response = request.execute()
    x = json.dumps(response)
    y = json.loads(x)

    return y

# query1 = 'harry potter'

# get_books_data(query1)
