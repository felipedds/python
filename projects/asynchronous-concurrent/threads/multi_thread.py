import threading
import time

def main() -> None:
    threads = [
        threading.Thread(target=count_text, args=("elephant", 10)),
        threading.Thread(target=count_text, args=("camel", 8)),
        threading.Thread(target=count_text, args=("monkey", 20))
    ]

    [thread.start() for thread in threads]
    print("Thread executing..")
    [thread.join() for thread in threads]
    print("Thread end.")

def count_text(text: str, number: int) -> None:
    for n in range(1, number + 1):
        print(f"{n} {text}")
        time.sleep(1)

if __name__ == "__main__":
    main()