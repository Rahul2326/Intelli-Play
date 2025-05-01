import pygame
import sys
import heapq
import random
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
AI_MODE = 3
MANUAL_MODE = 4

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mouse, Cats, and Cheese")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        self.state = MENU
        self.mode = None
        self.algorithm = None
        
        # Game elements
        self.mouse_pos = None
        self.cats = []
        self.cheese = None
        self.walls = []
        
        # For visualization
        self.visited = set()
        self.path = []
        
        # Game stats
        self.score = 0
        self.steps = 0
        
    def reset_game(self):
        self.mouse_pos = (random.randint(0, GRID_SIZE-1), (random.randint(0, GRID_SIZE-1)))
        self.cats = []
        for _ in range(2):  # Two cats
            while True:
                pos = (random.randint(0, GRID_SIZE-1), (random.randint(0, GRID_SIZE-1)))
                if pos != self.mouse_pos and pos not in self.cats:
                    self.cats.append(pos)
                    break
                    
        while True:
            self.cheese = (random.randint(0, GRID_SIZE-1), (random.randint(0, GRID_SIZE-1)))
            if self.cheese != self.mouse_pos and self.cheese not in self.cats:
                break
                
        # Generate some random walls
        self.walls = []
        for _ in range(10):
            while True:
                wall = (random.randint(0, GRID_SIZE-1), (random.randint(0, GRID_SIZE-1)))
                if wall != self.mouse_pos and wall != self.cheese and wall not in self.cats and wall not in self.walls:
                    self.walls.append(wall)
                    break
        
        self.visited = set()
        self.path = []
        self.steps = 0
        
    def draw_menu(self):
        self.screen.fill(WHITE)
        title = self.font.render("Mouse, Cats, and Cheese", True, BLACK)
        
        # Color information
        mouse_info = self.small_font.render("Green: Mouse", True, GREEN)
        cat_info = self.small_font.render("Red: Cats (avoid them!)", True, RED)
        cheese_info = self.small_font.render("Yellow: Cheese (collect it!)", True, YELLOW)
        black_info = self.small_font.render("Black: Walls (block paths)", True, BLACK)
        
        # Mode selection
        ai_btn = self.font.render("1. AI Mode", True, BLACK)
        manual_btn = self.font.render("2. Manual Mode", True, BLACK)
        quit_btn = self.font.render("3. Quit", True, BLACK)
        
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw color information
        self.screen.blit(mouse_info, (WIDTH//2 - mouse_info.get_width()//2, 120))
        self.screen.blit(cat_info, (WIDTH//2 - cat_info.get_width()//2, 150))
        self.screen.blit(cheese_info, (WIDTH//2 - cheese_info.get_width()//2, 180))
        self.screen.blit(black_info, (WIDTH//2 - black_info.get_width()//2, 210))
        
        # Draw mode selection
        self.screen.blit(ai_btn, (WIDTH//2 - ai_btn.get_width()//2, 280))
        self.screen.blit(manual_btn, (WIDTH//2 - manual_btn.get_width()//2, 330))
        self.screen.blit(quit_btn, (WIDTH//2 - quit_btn.get_width()//2, 380))
        
    def draw_game(self):
        self.screen.fill(WHITE)
        
        # Draw grid
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))
            
        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(self.screen, BLACK, (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
        # Draw visited cells (for AI visualization)
        for cell in self.visited:
            pygame.draw.rect(self.screen, (200, 230, 200), (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
        # Draw path (for AI visualization)
        for cell in self.path:
            pygame.draw.rect(self.screen, (150, 200, 150), (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
        # Draw cheese
        pygame.draw.rect(self.screen, YELLOW, (self.cheese[0]*CELL_SIZE, self.cheese[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw cats
        for cat in self.cats:
            pygame.draw.rect(self.screen, RED, (cat[0]*CELL_SIZE, cat[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
        # Draw mouse
        pygame.draw.rect(self.screen, GREEN, (self.mouse_pos[0]*CELL_SIZE, self.mouse_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw stats
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        steps_text = self.font.render(f"Steps: {self.steps}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(steps_text, (10, 40))
        
        if self.state == GAME_OVER:
            game_over = self.font.render("GAME OVER - Press R to return to menu", True, RED)
            self.screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2))
            
    def draw_algorithm_choice(self):
        self.screen.fill(WHITE)
        title = self.font.render("Choose Algorithm", True, BLACK)
        bfs_btn = self.font.render("1. Breadth-First Search (BFS)", True, BLACK)
        astar_btn = self.font.render("2. A* Algorithm", True, BLACK)
        back_btn = self.font.render("3. Back to Menu", True, BLACK)
        
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        self.screen.blit(bfs_btn, (WIDTH//2 - bfs_btn.get_width()//2, 200))
        self.screen.blit(astar_btn, (WIDTH//2 - astar_btn.get_width()//2, 250))
        self.screen.blit(back_btn, (WIDTH//2 - back_btn.get_width()//2, 300))
        
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 4-directional movement
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in self.walls:
                neighbors.append((nx, ny))
                
        return neighbors
        
    def bfs(self, start, goal):
        queue = deque()
        queue.append((start, [start]))
        visited = set()
        visited.add(start)
        
        while queue:
            current, path = queue.popleft()
            
            if current == goal:
                return path
                
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    
        return None  # No path found
        
    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    def astar(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        open_set_hash = {start}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
                
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
                        
        return None  # No path found
        
    def move_cats(self):
        new_cats = []
        for cat in self.cats:
            # Try to move toward mouse
            path = self.bfs(cat, self.mouse_pos)
            if path and len(path) > 1:
                new_cats.append(path[1])  # Next step in path
            else:
                new_cats.append(cat)  # Stay in place if no path
                
        self.cats = new_cats
        
    def check_collision(self):
        if self.mouse_pos in self.cats:
            self.state = GAME_OVER
        elif self.mouse_pos == self.cheese:
            self.score += 1
            self.reset_game()
            
    def manual_move(self, dx, dy):
        new_x, new_y = self.mouse_pos[0] + dx, self.mouse_pos[1] + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in self.walls:
            self.mouse_pos = (new_x, new_y)
            self.steps += 1
            self.move_cats()
            self.check_collision()
            
    def ai_move(self):
        if self.algorithm == "BFS":
            path = self.bfs(self.mouse_pos, self.cheese)
        else:  # A*
            path = self.astar(self.mouse_pos, self.cheese)
            
        if path and len(path) > 1:
            # For visualization
            self.visited = set(path)
            self.path = path
            
            # Move to next step in path
            self.mouse_pos = path[1]
            self.steps += 1
            self.move_cats()
            self.check_collision()
            
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if self.state == MENU:
                        if event.key == pygame.K_1:
                            self.state = AI_MODE
                        elif event.key == pygame.K_2:
                            self.state = MANUAL_MODE
                            self.reset_game()
                        elif event.key == pygame.K_3:
                            running = False
                            
                    elif self.state == AI_MODE:
                        if event.key == pygame.K_1:
                            self.algorithm = "BFS"
                            self.state = PLAYING
                            self.mode = "AI"
                            self.reset_game()
                        elif event.key == pygame.K_2:
                            self.algorithm = "A*"
                            self.state = PLAYING
                            self.mode = "AI"
                            self.reset_game()
                        elif event.key == pygame.K_3:
                            self.state = MENU
                            
                    elif self.state == PLAYING:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.state = MENU
                            
                    elif self.state == MANUAL_MODE:
                        if event.key == pygame.K_UP:
                            self.manual_move(0, -1)
                        elif event.key == pygame.K_DOWN:
                            self.manual_move(0, 1)
                        elif event.key == pygame.K_LEFT:
                            self.manual_move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.manual_move(1, 0)
                        elif event.key == pygame.K_r:
                            self.reset_game()
                            self.state = MENU
                            
                    elif self.state == GAME_OVER:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.state = MENU
                            
            # AI makes a move if in AI mode
            if self.state == PLAYING and self.mode == "AI":
                self.ai_move()
                pygame.time.delay(300)  # Slow down AI moves for visualization
                
            # Draw appropriate screen
            if self.state == MENU:
                self.draw_menu()
            elif self.state == AI_MODE:
                self.draw_algorithm_choice()
            else:  # PLAYING, MANUAL_MODE, GAME_OVER
                self.draw_game()
                
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    game = Game()
    game.run()