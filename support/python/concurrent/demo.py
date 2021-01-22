
import concurrent.futures
import time

start = time.perf_counter()


def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    print (f'Done Sleeping...{seconds}')




with concurrent.futures.ProcessPoolExecutor() as executor:
    for secs in range(1,5):
        executor.submit(do_something, secs)