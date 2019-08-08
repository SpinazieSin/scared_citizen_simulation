import time as time
from town import Town
from citizen import Citizen
from hunter import Hunter, PlayerHunter

def main():
    t = Town()
    t.load_empty_state(size=30)
    t.spawn_citizen(location=(29, 29))
    t.spawn_hunter()

    count = 0
    while True:
        if count > 50: break
        t.iterate()
        print(t)
        for citizen in t.citizens:
            if citizen.score["caught"]:
                print("DONE")
                print(citizen.score)
                return
        time.sleep(0.05)
        count += 1

if __name__ == '__main__':
    main()