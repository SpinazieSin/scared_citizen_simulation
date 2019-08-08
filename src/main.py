import time as time
from town import Town
from citizen import Citizen
from hunter import Hunter, PlayerHunter

def main():
    t = Town()
    t.load_empty_state()
    t.spawn_citizen()

    count = 0
    while True:
        if count > 50: break
        t.iterate()
        print(t)
        time.sleep(1)
        count += 1

if __name__ == '__main__':
    main()