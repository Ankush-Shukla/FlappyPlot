import matplotlib.pyplot as plt
import numpy as np
import random
# ---------------- CONFIG ----------------
WIDTH = 100
HEIGHT = 100

BIRD_X = 10
GRAVITY = 0.5
FLAP_STRENGTH = 8

PIPE_SPEED = 0.6
PIPE_WIDTH = 6
INITIAL_GAP = 30
MIN_GAP = 12

NUM_PIPES = 5
PIPE_SPACING = 25

# ---------------- STATE ----------------
bird_y = 50
velocity = 0
key_pressed = False
game_over = False
score = 0


def on_key(event):
    global key_pressed, game_over, bird_y, velocity, score

    if event.key == "x":
        key_pressed = True

    if event.key == "r" and game_over:
        reset_game()

def reset_game():
    global bird_y, velocity, game_over, score, pipes

    bird_y = 50
    velocity = 0
    game_over = False
    score = 0

    pipes.clear()
    init_pipes()

# ---------------- PIPE SYSTEM ----------------
pipes = []


def init_pipes():
    for i in range(NUM_PIPES):
        x = WIDTH + i * PIPE_SPACING
        gap_y = random.randint(30, 70)
        pipes.append({"x": x, "gap_y": gap_y})

def update_pipes(frame):
    global score

    # difficulty scaling
    gap_size = max(MIN_GAP, INITIAL_GAP - frame * 0.02)

    for pipe in pipes:
        pipe["x"] -= PIPE_SPEED

        # scoring
        if pipe["x"] < BIRD_X and not pipe.get("passed"):
            pipe["passed"] = True
            score += 1

        # reset pipe (controlled loop)
        if pipe["x"] < 10:
            pipe["x"] = WIDTH
            pipe["gap_y"] = random.randint(30, 70)
            pipe["passed"] = False

    return gap_size


def check_collision(gap_size):
    global bird_y

    for pipe in pipes:
        if abs(pipe["x"] - BIRD_X) < PIPE_WIDTH:
            gap_top = pipe["gap_y"] + gap_size / 2
            gap_bottom = pipe["gap_y"] - gap_size / 2

            if bird_y > gap_top or bird_y < gap_bottom:
                return True

    if bird_y <= 0 or bird_y >= HEIGHT:
        return True

    return False


# ---------------- MAIN ----------------
def main():
    global bird_y, velocity, key_pressed, game_over

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)

    fig.canvas.mpl_connect("key_press_event", on_key)

    # visuals
    bird = ax.scatter(BIRD_X, bird_y, s=200, color="yellow")
    text = ax.text(2, 95, "", fontsize=12)

    init_pipes()

    frame = 0

    try:
        while True:
            frame += 1

            if not game_over:
                # ---------- Bird Physics ----------
                velocity -= GRAVITY

                if key_pressed:
                    velocity = FLAP_STRENGTH
                    key_pressed = False

                bird_y += velocity
                bird_y = max(0, min(HEIGHT, bird_y))

                # ---------- Pipes ----------
                gap_size = update_pipes(frame)

                # ---------- Collision ----------
                if check_collision(gap_size):
                    game_over = True

            # ---------- Render ----------
            ax.clear()
            ax.set_xlim(0, WIDTH)
            ax.set_ylim(0, HEIGHT)

            # draw bird
            ax.scatter(BIRD_X, bird_y, s=200, color="yellow")

            # draw pipes
            for pipe in pipes:
                x = pipe["x"]
                gap_y = pipe["gap_y"]

                gap_top = gap_y + gap_size / 2
                gap_bottom = gap_y - gap_size / 2

                # bottom pipe
                ax.bar(x, gap_bottom, width=PIPE_WIDTH)

                # top pipe
                ax.bar(
                    x,
                    HEIGHT - gap_top,
                    bottom=gap_top,
                    width=PIPE_WIDTH,
                )

            # UI
            ax.text(2, 95, f"Score: {score}")

            if game_over:
                ax.text(30, 50, "GAME OVER\nPress R to Restart")

            plt.pause(0.01)

    except KeyboardInterrupt:
        print("Exited")


if __name__ == "__main__":
    main()