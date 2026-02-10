import pygame
import numpy as np
import random

class GridGame:
    def __init__(self):
        self.GRID_SIZE = 5
        self.CELL_SIZE = 100
        self.WINDOW_SIZE = self.GRID_SIZE * self.CELL_SIZE
        
        # 0 = прохід, 1 = стіна
        self.LEVEL_MAP = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        self.agent_pos = [0, 0]
        self.coin_pos = [4, 4]
        self.reset()

    def reset(self):
        self.agent_pos = [0, 0]
        while True:
            self.coin_pos = [random.randint(0, 4), random.randint(0, 4)]
            if self.LEVEL_MAP[self.coin_pos[0]][self.coin_pos[1]] == 0 and self.coin_pos != self.agent_pos:
                break
        return self._get_state()

    def _get_state(self):
        state = np.array(self.LEVEL_MAP)
        state[self.agent_pos[0], self.agent_pos[1]] = 2 # Агент
        return state

    def step(self, action):
        new_pos = list(self.agent_pos)
        if action == 0: new_pos[0] -= 1 # Up
        elif action == 1: new_pos[0] += 1 # Down
        elif action == 2: new_pos[1] -= 1 # Left
        elif action == 3: new_pos[1] += 1 # Right

        reward = -1 # Штраф за час
        
        # Перевірка меж та стін
        if (0 <= new_pos[0] < self.GRID_SIZE and 
            0 <= new_pos[1] < self.GRID_SIZE and 
            self.LEVEL_MAP[new_pos[0]][new_pos[1]] == 0):
            self.agent_pos = new_pos
        else:
            reward = -5 # Штраф за удар об стіну або межу

        done = False
        if self.agent_pos == self.coin_pos:
            reward = 50 # Велика нагорода за монету
            done = True

        return self._get_state(), reward, done

    def render(self):
        self.screen.fill((255, 255, 255))
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                rect = pygame.Rect(c*self.CELL_SIZE, r*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                if self.LEVEL_MAP[r][c] == 1:
                    pygame.draw.rect(self.screen, (100, 100, 100), rect) # Стіна
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        
        # Малюємо монету та агента
        pygame.draw.circle(self.screen, (255, 215, 0), (self.coin_pos[1]*100+50, self.coin_pos[0]*100+50), 30)
        pygame.draw.rect(self.screen, (0, 0, 255), (self.agent_pos[1]*100+10, self.agent_pos[0]*100+10, 80, 80))
        pygame.display.flip()