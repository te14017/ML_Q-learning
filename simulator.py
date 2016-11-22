from runner import main as runner


def main():
    i = 0
    n = 100
    while i <= n:
        runner(simulation=True)
        i += 1


if __name__ == '__main__':
    main()
