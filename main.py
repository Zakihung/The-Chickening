import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Kích thước màn hình mặc định
    pygame.display.set_caption("The Chickening")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Nền đen tạm thời
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()