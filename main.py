import matplotlib.pyplot as plt
import numpy as np
import random

# ---------------- CONFIG ----------------
BIRD_X = 10

GRAVITY = 0.35
FLAP_FORCE = 5.5
MAX_FALL = -6
MAX_RISE = 6
DAMPING = 0.92

PIPE_SPEED = 0.5
PIPE_WIDTH = 6

INITIAL_GAP = 28
MIN_GAP = 14

NUM_PIPES = 5
SPACING_RATIO = 0.35   # responsive spacing


# ---------------- STATE ----------------
class GameState:
    def __init__(self):
        self.bird_y = 50
        self.velocity = 0
        self.key_pressed = False
        self.game_over = False
        self.score = 0
        self.frame = 0
        self.pipes = []


state = GameState()


# ---------------- INPUT ----------------
def on_key(event):
    if event.key == "x":
        state.key_pressed = True

    if event.key == "r" and state.game_over:
        reset_game()


# ---------------- GAME CONTROL ----------------
def reset_game():
    global state
    state = GameState()
    init_pipes(100, 100)


# ---------------- PIPE SYSTEM ----------------
def generate_gap(prev_gap, gap_size, height):
    margin = 5
    min_y = gap_size / 2 + margin
    max_y = height - gap_size / 2 - margin

    if prev_gap is None:
        return random.uniform(min_y, max_y)

    # smooth transition (no sudden jumps)
    new_gap = prev_gap + random.uniform(-10, 10)
    return max(min_y, min(max_y, new_gap))


def init_pipes(width, height):
    state.pipes.clear()
    spacing = width * SPACING_RATIO
    gap_size = INITIAL_GAP

    prev_gap = None

    for i in range(NUM_PIPES):
        gap_y = generate_gap(prev_gap, gap_size, height)
        prev_gap = gap_y

        x = width + i * spacing

        state.pipes.append({
            "x": x,
            "gap_y": gap_y,
            "passed": False
        })


def update_pipes(width, height):
    spacing = width * SPACING_RATIO
    gap_size = max(MIN_GAP, INITIAL_GAP - state.frame * 0.01)

    for pipe in state.pipes:
        pipe["x"] -= PIPE_SPEED

        # scoring
        if pipe["x"] < BIRD_X and not pipe["passed"]:
            pipe["passed"] = True
            state.score += 1

        # reset pipe (maintain spacing)
        if pipe["x"] < BIRD_X - 10:
            max_x = max(p["x"] for p in state.pipes)

            pipe["x"] = max_x + spacing

            pipe["gap_y"] = generate_gap(
                prev_gap=pipe["gap_y"],
                gap_size=gap_size,
                height=height
            )

            pipe["passed"] = False

    return gap_size


# ---------------- COLLISION ----------------
def check_collision(gap_size, height):
    y = state.bird_y

    for pipe in state.pipes:
        if abs(pipe["x"] - BIRD_X) < PIPE_WIDTH:
            gap_top = pipe["gap_y"] + gap_size / 2
            gap_bottom = pipe["gap_y"] - gap_size / 2

            if y > gap_top or y < gap_bottom:
                return True

    if y <= 0 or y >= height:
        return True

    return False


# ---------------- MAIN ----------------
def main():
    fig, ax = plt.subplots(figsize=(6, 8))

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    fig.canvas.mpl_connect("key_press_event", on_key)

    init_pipes(100, 100)

    try:
        while True:
            state.frame += 1

            # dynamic dimensions (resize-safe)
            width = ax.get_xlim()[1]
            height = ax.get_ylim()[1]

            if not state.game_over:
                # ---------- Bird Physics ----------
                state.velocity -= GRAVITY

                if state.key_pressed:
                    state.velocity += FLAP_FORCE
                    state.key_pressed = False

                # clamp velocity
                state.velocity = max(MAX_FALL, min(MAX_RISE, state.velocity))

                # damping (smooth control)
                state.velocity *= DAMPING

                state.bird_y += state.velocity
                state.bird_y = max(0, min(height, state.bird_y))

                # ---------- Pipes ----------
                gap_size = update_pipes(width, height)

                # ---------- Collision ----------
                if check_collision(gap_size, height):
                    state.game_over = True

            else:
                gap_size = max(MIN_GAP, INITIAL_GAP - state.frame * 0.01)

            # ---------- Render ----------
            ax.clear()
            ax.set_xlim(0, width)
            ax.set_ylim(0, height)

            # bird
            ax.scatter(BIRD_X, state.bird_y, s=200)

            # pipes
            for pipe in state.pipes:
                x = pipe["x"]
                gap_y = pipe["gap_y"]

                gap_top = gap_y + gap_size / 2
                gap_bottom = gap_y - gap_size / 2

                ax.bar(x, gap_bottom, width=PIPE_WIDTH)
                ax.bar(
                    x,
                    height - gap_top,
                    bottom=gap_top,
                    width=PIPE_WIDTH
                )

            # UI
            ax.text(2, height - 5, f"Score: {state.score}")

            if state.game_over:
                ax.text(width / 3, height / 2, "GAME OVER\nPress R")

            plt.pause(0.01)

    except KeyboardInterrupt:
        print("Exited")


if __name__ == "__main__":
    main()