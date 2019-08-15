import time as time
from town import Town
from citizen import Citizen
from hunter import Hunter, PlayerHunter


def run_simulation():
    t = Town()
    t.load_empty_state(size=30)
    t.spawn_citizen(location=(15, 15))
    t.spawn_hunter()

    count = 0
    while True:
        if count > 50:
            break
        t.iterate()
        print(t)
        for citizen in t.citizens:
            if citizen.score["caught"]:
                print("DONE")
                print(citizen.score)
                return
        time.sleep(0.05)
        count += 1


def run_player_game():
    t = Town()
    t.load_empty_state(size=20)
    t.spawn_player()
    t.spawn_citizen(location=(15, 15), ai_type="smart")

    count = 0
    while True:
        if count > 50:
            break
        print(t)
        t.iterate()
        for citizen in t.citizens:
            if citizen.score["caught"]:
                print("DONE")
                print(citizen.score)
                return
        count += 1


def main():
    # run_simulation()
    run_player_game()
    print("FINISHED")


if __name__ == '__main__':
    main()
