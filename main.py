import numpy as np
import pygame

# константы
FPS = 60
WIDTH = 600  # размеры игрового поля
K = 5  # масштаб
WORK_SPACE = WIDTH // K
INFO_SPACE = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (240, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# здесь происходит инициация, создание объектов и др.
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('arial', INFO_SPACE)
window = pygame.display.set_mode((WIDTH, WIDTH + INFO_SPACE))
clock = pygame.time.Clock()

button_pause = pygame.Rect(WIDTH - INFO_SPACE * 3, WIDTH, INFO_SPACE, INFO_SPACE)
button_step = pygame.Rect(WIDTH - INFO_SPACE * 2, WIDTH, INFO_SPACE, INFO_SPACE)
button_go = pygame.Rect(WIDTH - INFO_SPACE, WIDTH, INFO_SPACE, INFO_SPACE)

pygame.display.update()
clock.tick(FPS)


def random_gen():
    return np.random.choice([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], size=(WORK_SPACE, WORK_SPACE))


def file_gen(filename):
    # Первое число файла: n - кол-во элементов в строке и кол-во столбцов
    matrix = np.zeros(shape=(WORK_SPACE, WORK_SPACE))
    with open(filename, 'r') as file:
        n = int(file.readline())
        for i in range(n):
            line = list(map(int, file.readline().split()))
            for j in range(n):
                matrix[i][j] = line[j]
    return matrix


def life_update(array):
    temp_matrix = np.zeros(shape=(WORK_SPACE, WORK_SPACE))
    # нахождение потенциально умерших\рожденных клеток в данной эпохе
    for i in range(WORK_SPACE):
        for j in range(WORK_SPACE):
            right = i + 1 if i < WORK_SPACE - 1 else 0
            left = i - 1 if i > 0 else WORK_SPACE - 1
            up = j - 1 if j > 0 else WORK_SPACE - 1
            down = j + 1 if j < WORK_SPACE - 1 else 0
            count = array[left][up] + array[i][up] + array[right][up] + array[left][j] + array[right][j] \
                    + array[left][down] + array[i][down] + array[right][down]
            if array[i][j] == 1 and (count < 2 or count > 3):
                temp_matrix[i][j] = -1
            elif array[i][j] == 0 and count == 3:
                temp_matrix[i][j] = 1
    # рождение\смерть клеток в данной эпохе
    for i in range(WORK_SPACE):
        for j in range(WORK_SPACE):
            if temp_matrix[i][j] == -1:
                array[i][j] = 0
            if temp_matrix[i][j] == 1:
                array[i][j] = 1
    return array


def array_print(array):
    for i in range(len(array)):
        print(array[i])
    print("--------------------")


def life_draw(life_matrix):
    for i in range(WORK_SPACE):
        pygame.draw.line(window, GREEN, [0, i * K], [WIDTH, i * K])
        pygame.draw.line(window, GREEN, [i * K, 0], [i * K, WIDTH])
        for j in range(WORK_SPACE):
            if life_matrix[i][j] == 1:
                pygame.draw.rect(window, BLACK, (i * K + 1, j * K + 1, K - 1, K - 1))


def main():
    life_matrix = random_gen()  # первичная генерация
    button_event = 'step'
    epoch = 0
    while True:
        # цикл обработки событий
        window.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_step.collidepoint(mouse_pos):
                    button_event = 'step'
                elif button_go.collidepoint(mouse_pos):
                    button_event = 'go'
            if event.type == pygame.QUIT:
                exit()

        if button_event != 'pause':
            # перерисовка живых клеток
            life_draw(life_matrix)

            pygame.draw.rect(window, RED, button_step)
            pygame.draw.rect(window, BLUE, button_go)

            epoch_text = font.render('Epoch: {}'.format(epoch), 1, BLACK)
            window.blit(epoch_text, (0, WIDTH))
            epoch += 1

            # обновление матрицы живых клеток
            life_update(life_matrix)

            if button_event == 'step':
                button_event = 'pause'

            pygame.display.update()


if __name__ == '__main__':
    main()
