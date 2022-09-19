from math import floor
import pygame
import random
pygame.init()


class DrawInformation:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('consolas', 15)
    LARGE_FONT = pygame.font.SysFont('consolas', 25)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD)/len(lst))
        self.block_height = floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        lst.append(random.randint(min_val, max_val))

    return lst


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    current_algo = draw_info.LARGE_FONT.render(
        f"{algo_name} : {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLUE)
    draw_info.window.blit(
        current_algo, (draw_info.width/2 - current_algo.get_width()/2, 5))

    controls = draw_info.FONT.render(
        "R - Reset | Space - Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(
        controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort | C - Counting Sort | S - Selection Sort" , 1, draw_info.BLACK)
    draw_info.window.blit(
        sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_lst(draw_info)
    pygame.display.update()


def draw_lst(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width -
                      draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,
                         draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i*draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val)*draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color,
                         (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_lst(draw_info, {j: draw_info.BLUE,
                         j + 1: draw_info.RED}, True)
                yield True
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        key = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > key and ascending
            descending_sort = i > 0 and lst[i-1] < key and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = key
            draw_lst(draw_info, {i: draw_info.BLUE, i-1: draw_info.RED}, True)
            yield True
    return lst


def counting_sort(draw_info, ascending=True):
    lst = draw_info.lst
    k = max(lst)
    lst_out = []
    dict_c = {}
    
    for p in range(len(lst)):
        lst_out.append(lst[p])

    for i in range(k + 1):
        dict_c[i] = 0

    for m in range(len(lst)):
        if lst[m] in dict_c:
            if ascending:
                dict_c[lst[m]] += 1
            if not ascending:
                dict_c[lst[m]] += -1

    for l in range(1, k+1):
        dict_c[l] += dict_c[l-1]

    for j in range(len(lst) - 1, -1, -1):
        if ascending:
            lst_out[dict_c[lst[j]]-1] = lst[j]
            dict_c[lst[j]] += -1
        if not ascending:
            lst_out[dict_c[lst[j]]+1] = lst[j]
            dict_c[lst[j]] += 1
        draw_info.set_list(lst_out)
        draw_lst(draw_info, {j: draw_info.BLUE, j + 1: draw_info.RED}, True)
        yield True
    return lst_out

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for j in range(len(lst) - 1):
        cur_index = j
        for i in range(j + 1, len(lst)):
            if ascending:
                if lst[cur_index] > lst[i]:
                    cur_index = i
            if not ascending:
                if lst[cur_index] < lst[i]:
                    cur_index = i
        if cur_index != j:
            lst[j], lst[cur_index] = lst[cur_index], lst[j]
            draw_lst(draw_info, {cur_index: draw_info.BLUE, j: draw_info.RED}, True)
            yield True
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(
                    draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_c and not sorting:
                sorting_algorithm = counting_sort
                sorting_algorithm_name = "Counting Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
