import pygame
import threading

neg_inf = float('-inf')
pos_inf = float('inf')
# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window caption
pygame.display.set_caption("Two Player Tic Tac Toe")

# Load and scale images
image_x = pygame.image.load('x.png')
image_x = pygame.transform.scale(image_x, (120, 120))
image_o = pygame.image.load('o.png')
image_o = pygame.transform.scale(image_o, (120, 120))

# Define button rects
button_rects = [
    pygame.Rect(200, 100, 120, 120),
    pygame.Rect(340, 100, 120, 120),
    pygame.Rect(480, 100, 120, 120),
    pygame.Rect(200, 240, 120, 120),
    pygame.Rect(340, 240, 120, 120),
    pygame.Rect(480, 240, 120, 120),
    pygame.Rect(200, 380, 120, 120),
    pygame.Rect(340, 380, 120, 120),
    pygame.Rect(480, 380, 120, 120),
]

# Track the state of each button (None for unclicked, 'X' for player 1, 'O' for player 2)
button_states = [None] * 9

# Turn counter
count = 0

def winning_condition(button_states):
    # Check rows
    for i in range(0, 9, 3):
        if button_states[i] == button_states[i + 1] == button_states[i + 2] and button_states[i] is not None:
            return button_states[i]
    # Check columns
    for i in range(3):
        if button_states[i] == button_states[i + 3] == button_states[i + 6] and button_states[i] is not None:
            return button_states[i]
    # Check diagonals
    if button_states[0] == button_states[4] == button_states[8] and button_states[0] is not None:
        return button_states[0]
    if button_states[2] == button_states[4] == button_states[6] and button_states[2] is not None:
        return button_states[2]
    return None

ai = 'O'
human = 'X'

scores = {
    'X': -1,
    'O': +1,
    'draw': 0
}

def minimax(button_states, depth, maximizingPlayer):
    result = winning_condition(button_states)
    if result is not None:
        return scores[result]
    
    if all(x is not None for x in button_states):
        return scores['draw']

    if maximizingPlayer:
        bestScore = neg_inf
        for i in range(9):
            if button_states[i] is None:
                button_states[i] = ai
                score = minimax(button_states, depth + 1, False)
                button_states[i] = None
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = pos_inf
        for i in range(9):
            if button_states[i] is None:
                button_states[i] = human
                score = minimax(button_states, depth + 1, True)
                button_states[i] = None
                bestScore = min(score, bestScore)
        return bestScore

def bestMove():
    bestScore = neg_inf
    move = None
    for i in range(9):
        if button_states[i] is None:
            button_states[i] = ai
            score = minimax(button_states, 0, False)
            button_states[i] = None
            print(f"Move: {i}, Score: {score}")  # Debugging output for each move and its score
            if score > bestScore:
                bestScore = score
                move = i
    if move is not None:
        button_states[move] = ai
        print(f"AI chooses position {move} with score {bestScore}")  # Debugging output for the chosen move


# Game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse position is within any button rect
            for i, button_rect in enumerate(button_rects):
                if button_rect.collidepoint(event.pos) and button_states[i] is None:
                    # Update the state of the button based on whose turn it is
                    if count % 2 == 0:
                        button_states[i] = 'X'
                        count += 1
                        winner = winning_condition(button_states)
                        if winner is not None:
                            break
                        if count % 2 != 0 and running:
                            bestMove()
                            count += 1
                            winner = winning_condition(button_states)
                            if winner is not None:
                                break

        # Fill the screen with a color
        screen.fill((0, 0, 0))

        # Draw the grid lines
        pygame.draw.line(screen, (255, 255, 255), (325, 100), (325, 500), 5)
        pygame.draw.line(screen, (255, 255, 255), (475, 100), (475, 500), 5)
        pygame.draw.line(screen, (255, 255, 255), (200, 225), (600, 225), 5)
        pygame.draw.line(screen, (255, 255, 255), (200, 375), (600, 375), 5)

        # Draw the buttons and images
        for i, button_rect in enumerate(button_rects):
            if button_states[i] == 'X':
                screen.blit(image_x, button_rect)
            elif button_states[i] == 'O':
                screen.blit(image_o, button_rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), button_rect)

        # Update the display
        pygame.display.flip()

        # Check for a winning condition
        winner = winning_condition(button_states)
        if winner is not None:
            print(f"Player {winner} wins!")
            running = False
        if count == 10:
            print("It's a tie!")
            running = False


# Quit Pygame
pygame.quit()
