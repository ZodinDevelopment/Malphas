import time


def example(seconds):
    print("Starting")
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print("Completed.")
    