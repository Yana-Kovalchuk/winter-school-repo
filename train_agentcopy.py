import numpy as np
import random
import time
import pygame
import os
from games.grid_env import GridGame 

def train():
    # 1. Ініціалізація середовища
    env = GridGame()
    
    # Файл для збереження "мізків" агента
    MODEL_FILE = "q_table_brains.npy"
    
    # Гіперпараметри
    alpha = 0.1          
    gamma = 0.95         
    epsilon = 0.2        
    episodes = 500       
    
    # 2. Завантаження або створення Q-таблиці
    if os.path.exists(MODEL_FILE):
        print(f"Знайдено збережену модель! Завантажую {MODEL_FILE}...")
        q_table = np.load(MODEL_FILE)
    else:
        print("Створюю нову Q-таблицю...")
        q_table = np.zeros([25, 4])

    print("Починаємо навчання агента...")

    for i in range(episodes):
        env.reset() 
        state = int(env.agent_pos[0] * 5 + env.agent_pos[1])
        done = False
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Exploration vs Exploitation
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3) 
            else:
                action = np.argmax(q_table[state]) 

            _, reward, done = env.step(action)
            next_state = int(env.agent_pos[0] * 5 + env.agent_pos[1])

            # Візуалізація (можна закоментувати для прискорення навчання)
            env.render()
            time.sleep(0.01) # Пришвидшив для навчання

            # Рівняння Белмана
            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])
            q_table[state, action] = old_value + alpha * (reward + gamma * next_max - old_value)
            
            state = next_state

        if (i + 1) % 50 == 0:
            print(f"Епізод {i + 1} завершено. Зберігаю прогрес...")
            np.save(MODEL_FILE, q_table)

    print("\n--- НАВЧАННЯ ЗАВЕРШЕНО ---")
    print("Демонстрація фінального результату:")
    
    # 3. Перевірка навченого агента
    env.reset()
    done = False
    steps = 0
    while not done:
        state = int(env.agent_pos[0] * 5 + env.agent_pos[1])
        action = np.argmax(q_table[state]) # Тепер тільки досвід
        
        _, _, done = env.step(action)
        steps += 1
        env.render()
        time.sleep(0.3)
        
    print(f"Перемога! Агент знайшов монету всього за {steps} кроків.")
    time.sleep(2)
    pygame.quit()

if __name__ == "__main__":
    train()