import gevent

"""
Brief summary of the purpose of this script:

1. Use gevent to download data from the given URL 10 times, as fast as possible
2. While the downloads are being performed - calculate the value of PI as accurately as possible.

Results:

When all URLS are downloaded:
  In the code block that calculated pi, display the final value of pi, each download task displaying the 
    number of bytes downloaded, and some mechanism to show a human that the data is the same for each download.

"""

DOWNLOAD_URL = 'http://slowwly.robertomurray.co.uk/delay/3000/url/https://www.python.org/'


def main():
    pass


if __name__ == '__main__':
    main()