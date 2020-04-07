import os


def main(audio="music.m4a"):
    print("\nprogram is finished")
    if audio:
        os.system(f"afplay {audio}")
    else:
        os.system('say "your program is finished"')


if __name__ == "__main__":
    main()
