import threading
import time

def main() -> None:
    thread = threading.Thread(target=count_text, args=("elephant", 10))
    thread.start()
    print("Thread executing..")
    thread.join()
    print("Thread end.")

def count_text(text: str, number: int) -> None:
    for n in range(1, number + 1):
        print(f"{n} {text}")
        time.sleep(1)

if __name__ == "__main__":
    main()