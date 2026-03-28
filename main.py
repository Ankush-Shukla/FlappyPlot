import matplotlib.pyplot as plt


def main():
    # bars/obstacles of our game
    bars = [10, 20, 30, 40, 50, 60]
    bar_height = [40, 30, 70, 10, 20, 40]

    # birb - only change in y axis no change in x axis
    bird_height = 90
    plt.scatter(2, bird_height, color="yellow")

    plt.ylim(0, 100)
    plt.bar(bars, bar_height, color="green")
    plt.savefig("test")


if __name__ == "__main__":
    main()
