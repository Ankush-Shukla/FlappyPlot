import matplotlib.pyplot as plt
import numpy as np
import random

bird_height = 90
Key_pressed = False


def on_key(event):
    global Key_pressed
    if event.key == "x":
        Key_pressed = True


def main():
    global bird_height, Key_pressed

    # X positions
    bars = np.array([10, 20, 30, 40, 50, 60], dtype=float)

    width = 3
    speed = 0.3

    # Heights
    bar_height = np.array([40, 30, 70, 10, 20, 40], dtype=float)
    gap = 20  # constant gap

    fig, ax = plt.subplots(figsize=(8, 6))
    point = ax.scatter(2, bird_height, color="yellow")

    ax.set_xlim(0, 70)
    ax.set_ylim(0, 100)

    # Initial bars
    bottom_rects = ax.bar(bars, bar_height, width=width, color="green")
    gap_rects = ax.bar(bars, [gap]*len(bars), bottom=bar_height, width=width, color="white")
    top_rects = ax.bar(
        bars,
        100 - (bar_height + gap),
        bottom=bar_height + gap,
        width=width,
        color="green",
    )

    fig.canvas.mpl_connect("key_press_event", on_key)

    try:
        while True:
            # ---------------- Bird physics ----------------
            bird_height -= 0.4
            bird_height = max(0, bird_height)

            if Key_pressed:
                bird_height += 10
                Key_pressed = False

            point.set_offsets([[2, bird_height]])

            # ---------------- Bar movement ----------------
            bars -= speed

            for i in range(len(bars)):
                if bars[i] < 0:
                    bars[i] = 70  # reset to right
                    bar_height[i] = random.randint(10, 70)

            # ---------------- Update bars ----------------
            for i, rect in enumerate(bottom_rects):
                rect.set_x(bars[i])
                rect.set_height(bar_height[i])

            for i, rect in enumerate(gap_rects):
                rect.set_x(bars[i])
                rect.set_y(bar_height[i])

            for i, rect in enumerate(top_rects):
                rect.set_x(bars[i])
                rect.set_y(bar_height[i] + gap)
                rect.set_height(100 - (bar_height[i] + gap))

            plt.pause(0.01)

    except KeyboardInterrupt:
        print("Game stopped")


if __name__ == "__main__":
    main()