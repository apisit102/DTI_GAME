import pygame
import sys

# เริ่มต้นการใช้งาน Pygame
pygame.init()

# ตั้งค่าหน้าจอแสดงผล
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game Menu")

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (133, 193, 233)
BORDER_COLOR = (174, 214, 241)
SHADOW_COLOR = (93, 173, 226)
BOX_COLOR = (210, 231, 238)

# ฟอนต์ที่เหมาะกับเกม RPG
try:
    font = pygame.font.Font("medieval.ttf", 74)
    small_font = pygame.font.Font("medieval.ttf", 36)
except:
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

# สถานะของเกม
current_state = "menu"

# ฟังก์ชันวาดปุ่ม 3D พร้อมข้อความ
def draw_3d_button(rect, text, color=BUTTON_COLOR, border_color=BORDER_COLOR, shadow_color=SHADOW_COLOR):
    pygame.draw.rect(screen, shadow_color, rect.move(3, 3))  # วาดเงา
    pygame.draw.rect(screen, color, rect)  # วาดปุ่มหลัก
    pygame.draw.rect(screen, border_color, rect, 2)  # วาดขอบ
    text_surf = small_font.render(text, True, BLACK)
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))

# ฟังก์ชันวาดเมนูหลัก
def draw_menu():
    screen.fill(BLACK)
    title_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 4 - 50, 400, 100)
    draw_3d_button(title_rect, "Good Knight", color=BOX_COLOR)

    # วาดปุ่มต่างๆ
    start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)
    option_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
    exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 60)
    
    draw_3d_button(start_button_rect, "Play Game")
    draw_3d_button(option_button_rect, "Options")
    draw_3d_button(exit_button_rect, "Exit")
    pygame.display.flip()

# ฟังก์ชันแสดงหน้าจอการเล่นเกม
def draw_play_screen():
    screen.fill(BLACK)
    play_text = font.render("Playing Game", True, WHITE)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - play_text.get_height() // 2))
    
    # วาดปุ่มย้อนกลับที่มุมขวาล่าง
    back_button_rect = pygame.Rect(WIDTH - 80, HEIGHT - 60, 60, 40)
    draw_3d_button(back_button_rect, "Back")  # ใช้ฟังก์ชัน draw_3d_button
    pygame.display.flip()

# ฟังก์ชันวาดเมนูตัวเลือก
def draw_options():
    screen.fill(BLACK)
    options_text_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 4 - 30, 300, 60)
    draw_3d_button(options_text_rect, "Options", color=BOX_COLOR)
    
    # วาดปุ่มย้อนกลับ
    back_button_rect = pygame.Rect(WIDTH - 80, HEIGHT - 60, 60, 40)
    draw_3d_button(back_button_rect, "Back")  # ใช้ฟังก์ชัน draw_3d_button
    pygame.display.flip()

# ฟังก์ชันจัดการคลิกในเมนูหลัก
def handle_menu_click(mouse_y):
    if HEIGHT // 2 - 30 < mouse_y < HEIGHT // 2 + 30:  # Play Game
        return "play"
    elif HEIGHT // 2 + 50 < mouse_y < HEIGHT // 2 + 110:  # Options
        return "options"
    elif HEIGHT // 2 + 130 < mouse_y < HEIGHT // 2 + 190:  # Exit
        pygame.quit()
        sys.exit()
    return current_state

# ฟังก์ชันจัดการคลิกในหน้าจอการเล่นเกม
def handle_play_click(mouse_x, mouse_y):
    back_button_rect = pygame.Rect(WIDTH - 80, HEIGHT - 60, 60, 40)
    if back_button_rect.collidepoint(mouse_x, mouse_y):
        return "menu"
    return current_state

# ฟังก์ชันจัดการคลิกในเมนูตัวเลือก
def handle_options_click(mouse_x, mouse_y):
    back_button_rect = pygame.Rect(WIDTH - 80, HEIGHT - 60, 60, 40)
    if back_button_rect.collidepoint(mouse_x, mouse_y):
        return "menu"
    return current_state

# วนลูปเกมหลัก
def main():
    global current_state
    clock = pygame.time.Clock() 
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if current_state == "menu":
                    current_state = handle_menu_click(mouse_y)
                elif current_state == "play":
                    current_state = handle_play_click(mouse_x, mouse_y)
                elif current_state == "options":
                    current_state = handle_options_click(mouse_x, mouse_y)

        # วาดหน้าจอที่เหมาะสมตามสถานะ
        if current_state == "menu":
            draw_menu()
        elif current_state == "play":
            draw_play_screen()
        elif current_state == "options":
            draw_options()

        clock.tick(60)
        
# เรียกใช้งานฟังก์ชันหลัก
if __name__ == "__main__":
    main()


