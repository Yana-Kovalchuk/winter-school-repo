import pygame
import chess
import numpy as np

class ChessEnv:
    def __init__(self):
        # Ініціалізація шахової дошки через python-chess
        self.board = chess.Board()
        
        # Налаштування графіки
        self.SQUARE_SIZE = 60
        self.WINDOW_SIZE = 8 * self.SQUARE_SIZE
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("RL Chess Environment")
        
        # Кольори дошки (класичні зелено-бежеві)
        self.COLOR_LIGHT = (235, 235, 208)
        self.COLOR_DARK = (119, 149, 86)
        
        # Налаштування шрифту для літер-фігур
        self.font = pygame.font.SysFont('Arial', 40, bold=True)

    def reset(self):
        """Скидає гру до початкової позиції"""
        self.board = chess.Board()
        return self._get_state()

    def _get_state(self):
        """Перетворює стан дошки у числовий масив для ШІ"""
        # Створюємо порожню матрицю 8x8
        state = np.zeros((8, 8), dtype=int)
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, 8)
            # Білі фігури (додатні), Чорні (від'ємні)
            val = piece.piece_type
            state[row, col] = val if piece.color == chess.WHITE else -val
        return state

    def step(self, move_uci):
        """Виконує хід та повертає (новий стан, винагорода, кінець гри)"""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                # Перевіряємо, чи є взяття фігури до того, як зробити хід
                is_capture = self.board.is_capture(move)
                
                self.board.push(move)
                
                # --- ЛОГІКА ВИНАГОРОД (Reward Function) ---
                reward = 0
                done = self.board.is_game_over()
                
                if self.board.is_checkmate():
                    reward = 100  # Величезний бонус за перемогу
                elif is_capture:
                    reward = 10   # Бонус за взяття фігури
                else:
                    reward = -0.1 # Мінімальний штраф за кожен хід, щоб агент не "тягнув час"
                
                return self._get_state(), reward, done
            else:
                return self._get_state(), -5, False # Штраф за спробу нелегального ходу
        except:
            return self._get_state(), -5, False

    def render(self):
        """Малює дошку та фігури літерами різних кольорів"""
        pygame.event.pump() # Оновлення внутрішніх подій pygame
        
        # 1. Малюємо клітинки
        for r in range(8):
            for c in range(8):
                # Шаховий порядок кольорів (враховуємо, що 0,0 - це a1 у python-chess)
                color = self.COLOR_LIGHT if (r + c) % 2 == 0 else self.COLOR_DARK
                # В pygame 0,0 - це верхній лівий кут, тому інвертуємо ряд (7-r)
                pygame.draw.rect(self.screen, color, (c * self.SQUARE_SIZE, (7 - r) * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
        
        # 2. Малюємо фігури
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, 8)
            
            # Білі фігури — Білі, Чорні — Темно-сірі
            text_color = (255, 255, 255) if piece.color == chess.WHITE else (35, 35, 35)
            
            symbol = piece.symbol().upper() # Наприклад 'P', 'N', 'Q'
            text_surface = self.font.render(symbol, True, text_color)
            
            # Центрування літери в клітинці
            text_rect = text_surface.get_rect(center=(
                col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, 
                (7 - row) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            ))
            
            # Додаємо чорну тінь для білих літер, щоб їх було краще видно
            if piece.color == chess.WHITE:
                shadow = self.font.render(symbol, True, (0, 0, 0))
                self.screen.blit(shadow, text_rect.move(2, 2))
                
            self.screen.blit(text_surface, text_rect)
            
        pygame.display.flip()

    def close(self):
        pygame.quit()