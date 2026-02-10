import time
import random
import pygame
from games.chess_env import ChessEnv

def run_chess_demo():
    # 1. Ініціалізація середовища
    env = ChessEnv()
    env.reset()
    
    done = False
    total_reward = 0
    move_count = 0

    print("Запуск демонстрації шахів (Self-Play)...")

    while not done:
        # Обробка виходу з програми
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 2. Отримання списку всіх легальних ходів
        legal_moves = list(env.board.legal_moves)
        
        if not legal_moves:
            break

        # 3. Вибір випадкового ходу (аналог Exploration)
        chosen_move = random.choice(legal_moves)
        move_uci = chosen_move.uci()

        # 4. Виконання ходу в середовищі
        state, reward, done = env.step(move_uci)
        total_reward += reward
        move_count += 1

        # 5. Візуалізація
        env.render()
        pygame.display.set_caption(f"Хід: {move_count} | Нагорода: {total_reward} | Останній: {move_uci}")
        
        # Затримка, щоб ми встигли побачити хід (0.5 секунди)
        time.sleep(0.5)

    print(f"Гра завершена за {move_count} ходів. Фінальна нагорода: {total_reward}")
    
    # Чекаємо трохи перед закриттям
    time.sleep(3)
    pygame.quit()

if __name__ == "__main__":
    run_chess_demo()