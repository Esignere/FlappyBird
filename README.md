# Flappy Bird - Python & Pygame

A recreation of the classic Flappy Bird game, developed in Python using the Pygame library. The project implements bird animation, gravity, jumping mechanics, pipe generation, collision detection, and score tracking.

## Features

- **Bird Movement:** Jumping mechanics and gravity simulation.
- **Animations:** Animated bird sprites with rotation based on movement.
- **Obstacle Generation:** Pipes with randomized heights.
- **Collision Detection:** Mask-based collision detection between the bird and pipes.
- **Score System:** Tracks the player's score as they pass obstacles.
- **Scrolling Ground:** Continuously moving ground for a seamless gameplay experience.
- **Game Loop:** Event handling and frame rate control.

## Technologies

- Python
- Pygame
- Random
- OS

## Project Structure

```text
FlappyBird/
├── img/
│   ├── bg.png
│   ├── base.png
│   ├── pipe.png
│   ├── bird1.png
│   ├── bird2.png
│   └── bird3.png
├── FlappyBird.py
└── README.md
```

## Requirements

- Python 3.10 or later recommended
- Pygame

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/FlappyBird.git
cd FlappyBird
```

**2. Install the dependencies**

```bash
python -m pip install pygame
```

**3. Run the game**

```bash
python FlappyBird.py
```

Make sure the `img` directory and its image assets are in the same directory as `FlappyBird.py`.

## How to Play

- Press **SPACE** to make the bird jump.
- Avoid colliding with pipes.
- Avoid hitting the ground or the top of the screen.
- Pass through the obstacles to increase your score.

## What I Learned

Through this project, I practiced:

- Object-oriented programming with Python classes.
- Game loops and event handling.
- Sprite animation and image transformations.
- Basic physics simulation using velocity and displacement.
- Collision detection using Pygame masks.
- Randomized obstacle generation.
- Managing game objects and updating the display.

## Future Improvements

- Add a start screen and a game-over screen.
- Implement a restart button.
- Save the highest score.
- Add sound effects and background music.
- Improve the user interface.

## License

This project was created for educational purposes. Image assets may have separate licenses or attribution requirements.
