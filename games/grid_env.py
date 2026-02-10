import pygame
import numpy as np
import random

class GridGame:
    def __init__(self):
        # Game constants
        self.GRID_SIZE = 5
        self.CELL_SIZE = 100
        self.WINDOW_SIZE = self.GRID_SIZE * self.CELL_SIZE
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Grid Coin Collector")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.agent_pos = [0, 0]  # [row, col]
        self.coin_pos = [0, 0]
        self.done = False
        
        # Reset to initialize positions
        self.reset()
    
    def reset(self):
        """Reset the game and return initial state"""
        # Place agent at random position
        self.agent_pos = [random.randint(0, self.GRID_SIZE-1), random.randint(0, self.GRID_SIZE-1)]
        
        # Place coin at random position (different from agent)
        while True:
            self.coin_pos = [random.randint(0, self.GRID_SIZE-1), random.randint(0, self.GRID_SIZE-1)]
            if self.coin_pos != self.agent_pos:
                break
        
        self.done = False
        return self._get_state()
    
    def _get_state(self):
        """Return current state as 2D grid array"""
        state = np.zeros((self.GRID_SIZE, self.GRID_SIZE))
        state[self.agent_pos[0], self.agent_pos[1]] = 1  # Agent
        state[self.coin_pos[0], self.coin_pos[1]] = 2    # Coin
        return state
    
    def step(self, action):
        """
        Execute action and return (next_state, reward, done)
        Actions: 0=Up, 1=Down, 2=Left, 3=Right
        """
        if self.done:
            # If episode ended, reset and start new episode
            self.reset()
            
        # Move agent based on action
        if action == 0:  # Up
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == 1:  # Down
            self.agent_pos[0] = min(self.GRID_SIZE - 1, self.agent_pos[0] + 1)
        elif action == 2:  # Left
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == 3:  # Right
            self.agent_pos[1] = min(self.GRID_SIZE - 1, self.agent_pos[1] + 1)
        
        # Check if agent collected coin
        reward = -1  # Step penalty
        if self.agent_pos == self.coin_pos:
            reward += 10  # Coin collection reward
            self.done = True  # Episode ends when coin is collected
            
        next_state = self._get_state()
        return next_state, reward, self.done
    
    def render(self):
        """Update the pygame display"""
        # Fill screen with white background
        self.screen.fill(self.WHITE)
        
        # Draw grid lines
        for i in range(self.GRID_SIZE + 1):
            # Vertical lines
            pygame.draw.line(self.screen, self.BLACK, 
                            (i * self.CELL_SIZE, 0), 
                            (i * self.CELL_SIZE, self.WINDOW_SIZE), 2)
            # Horizontal lines
            pygame.draw.line(self.screen, self.BLACK, 
                            (0, i * self.CELL_SIZE), 
                            (self.WINDOW_SIZE, i * self.CELL_SIZE), 2)
        
        # Draw agent (blue square)
        agent_rect = pygame.Rect(
            self.agent_pos[1] * self.CELL_SIZE + 10,
            self.agent_pos[0] * self.CELL_SIZE + 10,
            self.CELL_SIZE - 20,
            self.CELL_SIZE - 20
        )
        pygame.draw.rect(self.screen, self.BLUE, agent_rect)
        
        # Draw coin (yellow circle)
        coin_center = (
            self.coin_pos[1] * self.CELL_SIZE + self.CELL_SIZE // 2,
            self.coin_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        )
        pygame.draw.circle(self.screen, self.YELLOW, coin_center, self.CELL_SIZE // 3)
        
        # Update display
        pygame.display.flip()
        self.clock.tick(60)  # Cap at 60 FPS
    
    def run_manual_game(self):
        """Run the game manually with keyboard controls for testing"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        _, _, done = self.step(0)
                    elif event.key == pygame.K_DOWN:
                        _, _, done = self.step(1)
                    elif event.key == pygame.K_LEFT:
                        _, _, done = self.step(2)
                    elif event.key == pygame.K_RIGHT:
                        _, _, done = self.step(3)
                    
                    if done:
                        print("Coin collected! Resetting...")
                        self.reset()
            
            self.render()
        
        pygame.quit()

# Example usage for testing
if __name__ == "__main__":
    # Create game instance
    game = GridGame()
    
    # Test RL interface
    print("Testing RL interface:")
    state = game.reset()
    print("Initial state:")
    print(state)
    
    # Take a few random steps
    for i in range(5):
        action = random.randint(0, 3)
        next_state, reward, done = game.step(action)
        print(f"Action: {action}, Reward: {reward}, Done: {done}")
        if done:
            print("Episode finished!")
            break
    
    # Run manual game (uncomment to play with keyboard)
    # game.run_manual_game()
