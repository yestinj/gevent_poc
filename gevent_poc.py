import math

import gevent
import gevent.monkey
import urllib.request
import hashlib

from gevent.queue import Queue

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

DOWNLOAD_URL = 'http://slowwly.robertomurray.co.uk/delay/3000/url/https://www.python.org/'

download_results = Queue()


def download(id):
    response = urllib.request.urlopen(DOWNLOAD_URL)
    result = response.read().decode('utf-8')

    m = hashlib.md5()
    m.update(result.encode('utf-8'))
    md5_hash = m.hexdigest()

    results = {'id': id, 'length': len(result), 'hash': md5_hash}
    download_results.put_nowait(results)
    return True


def chudnovsky_pi():
    """
    I wasn't going to reinvent the wheel here, all credit goes to:
    https://towardsdatascience.com/how-to-make-pi-part-1-d0b41a03111f
    I made very minor modifications

    :return: The calculated value of pi, as best as Python can manage it using this formula.
    """
    pi = 0
    # 18 was the highest I could go with Python 3, higher results in a math error.
    for k in range(0, 18):
        numerator = math.pow(-1, k % 2) * math.factorial(6 * k) * (13591409 + 545140134 * k)
        denominator = math.factorial(3 * k) * math.pow(math.factorial(k), 3) * math.pow(640320, 3 * k + 3 / 2)
        pi += numerator / denominator
        # Part of a better solution, if pi calculation is going to take longer than the downloads.
        if len(download_results) == 10:
            print('Breaking out, all downloads complete before we finished...')
            break
    pi = 12 * pi
    pi = 1 / pi

    # Better solution - assuming we finish faster here than the downloads, block/sleep/await for the downloads
    # to be complete, e.g. queue size 10 or some better signaling method, e.g. greenlets all completed.
    return pi


def calculate_pi():
    """
    Calculate the value of pi while doing 10x downloads of the given URL.
    """
    threads = []
    for i in range(1, 11):
        threads.append(gevent.spawn(download, i))

    # NOTE: This is a bit of a cop out. I couldn't figure out how to do what I wanted in the time allocated, it would
    # have been something like checking a semaphore at the end of the chudnovsky_pi for loop, having each download
    # job decrement the semaphore when it was complete, thus triggering the loop to break once all downloads were
    # complete, or, adding to a queue, and only consuming from the queue when the downloads are all complete,
    # e.g. len(queue) == 10.
    # Since this pi calculation method is much faster than the downloads, and its the best approximation in Python,
    # I decided to rather stick with this method of doing it.

    # For a better solution, we'd need to now start up chudnovsky_pi in its own greenlet,
    pi = chudnovsky_pi()
    gevent.joinall(threads)

    print('The final pi is {}'.format(pi))
    results = list()
    while not download_results.empty():
        results.append(download_results.get())
    sorted_results = sorted(results, key=lambda k: k['id'])

    print('Downloads for: {}'.format(DOWNLOAD_URL))
    for r in sorted_results:
        print('Download {}: Bytes Downloaded: {}, Contents MD5 Hash: {}'.format(r['id'], r['length'], r['hash']))


def main():
    gevent.spawn(calculate_pi()).join()


if __name__ == '__main__':
    main()
