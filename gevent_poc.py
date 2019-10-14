import gevent
import gevent.monkey
import urllib.request

gevent.monkey.patch_socket()

"""
Brief summary of the purpose of this script:

1. Use gevent to download data from the given URL 10 times, as fast as possible
2. While the downloads are being performed - calculate the value of PI as accurately as possible.

Results:

When all URLS are downloaded:
  In the code block that calculated pi, display the final value of pi, each download task displaying the 
    number of bytes downloaded, and some mechanism to show a human that the data is the same for each download.

"""

"""
Solution ideas and planning:

1. Downloading the URL ten times.
    Spawn 10 async tasks and download the file in each. They can run concurrently.
    Need to be able to return their results to another gevent task, being filesize and content or md5 hash of content 
2. Calculating pi.
    Another 'job' spawned which sits calculating pi.
    It needs a way of knowing when each download is complete, so that it can print out the final stuffs.
    Ways to do this?
    1. Semaphore set at 10, decrement on each complete download?
    2. Signal handler of some kind in the calculation process?
        e.g. Calculate -> 0.1s check state of 'x' -> repeat
        
    
     

"""

DOWNLOAD_URL = 'http://slowwly.robertomurray.co.uk/delay/3000/url/https://www.python.org/'


def download(id):
    response = urllib.request.urlopen(DOWNLOAD_URL)
    result = response.read().decode('utf-8')
    print('Process {} done, length {}'.format(id, len(result)))
    return True


# Reference to https://stackoverflow.com/questions/28699577/python-pi-approximation for the basic implementation
def calculate_pi():
    pass
    # value = 0
    # for k in xrange(1, 2 * rank + 1, 2):
    #     sign = -(k % 4 - 2)
    #     value += float(sign) / k
    # return 4 * value


def main():
    print('Starting greenlets...')
    threads = []
    for i in range(1, 10):
        threads.append(gevent.spawn(download, i))
    print('All started!')
    gevent.joinall(threads)
    print('All finished!')


if __name__ == '__main__':
    main()
