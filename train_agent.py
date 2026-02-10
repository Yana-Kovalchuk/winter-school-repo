import numpy as np
import random
import time
import pygame
import os
import matplotlib.pyplot as plt
from games.grid_env2 import GridGame 

def train():
    env = GridGame()
    MODEL_FILE = "q_table_walls.npy"
    
    # Гіперпараметри
    alpha = 0.1          
    gamma = 0.95         
    epsilon = 1.0        # Починаємо з 100% випадкових ходів
    epsilon_min = 0.05   # Мінімальний шанс випадкового ходу
    epsilon_decay = 0.998 # Коефіцієнт згасання епсилону
    episodes = 1000      
    max_steps = 100      # Обмеження кроків на гру
    
    q_table = np.zeros([25, 4])
    rewards_history = [] # Для графіка

    print("Починаємо оптимізоване навчання в лабіринті...")

    for i in range(episodes):
        env.reset() 
        state = int(env.agent_pos[0] * 5 + env.agent_pos[1])
        done = False
        total_reward = 0
        steps = 0
        
        while not done and steps < max_steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Exploration vs Exploitation (Епсилон-жадібна стратегія)
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3) 
            else:
                action = np.argmax(q_table[state]) 

            _, reward, done = env.step(action)
            next_state = int(env.agent_pos[0] * 5 + env.agent_pos[1])
            total_reward += reward
            steps += 1

            # Оновлення Q-таблиці (Рівняння Белмана)
            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])
            q_table[state, action] = old_value + alpha * (reward + gamma * next_max - old_value)
            
            state = next_state
            
            # Рендеримо лише кожен 2-й епізод, щоб навчання йшло швидше
            if i % 2 == 0:
                env.render()
                pygame.display.set_caption(f"Ep: {i+1} | Rew: {total_reward} | Eps: {epsilon:.2f}")

        # Зменшуємо epsilon після кожного епізоду
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

        rewards_history.append(total_reward)

        if (i + 1) % 50 == 0:
            print(f"Епізод {i + 1}: Нагорода = {total_reward}, Епсилон = {epsilon:.2f}")
            np.save(MODEL_FILE, q_table)

    print("\nНавчання завершено!")
    pygame.quit()

    # Малюємо графік результатів
    plt.plot(rewards_history)
    plt.title("Прогрес навчання агента")
    plt.xlabel("Епізод")
    plt.ylabel("Сумарна нагорода")
    plt.show()

if __name__ == "__main__":
    train()