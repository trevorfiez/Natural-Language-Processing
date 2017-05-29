def get_raw_pairs():
    raw = sys.stdin.read().split("\n")
    del raw[2::3]
    return "\n".join(raw)[0:-1]

def main():
    ek_raw = get_raw_pairs()

if __name__ == "__main__":
    main()
