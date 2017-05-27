import pygame


def dec_to_bin(x):
    return int(bin(x)[2:])


class Base:
    box_width = 1
    box_height = 1

    rows = 400
    cols = 800

    colorize = False

    grid = []

    combinations = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 1],
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]
    ]
    combination_colors = [
        (248, 12, 18),
        (255, 102, 68),
        (254, 174, 45),
        (208, 195, 16),
        (105, 208, 37),
        (18, 189, 185),
        (68, 68, 221),
        (68, 34, 153)
    ]
    starting_row = [int(x) for x in list("010")]

    def screenshot(self, num):
        fname = "images" + ("_colorized" if self.colorize else "") + "/" + num.__str__() + ".png"
        pygame.image.save(self.game_display, fname)

    def gen_next_row(self, prev_row, gen_one):
        next_row = []
        next_row_colors = []

        for col in range(self.cols):
            if col == 0:
                compare_three = [prev_row[0], prev_row[1], prev_row[2]]
            elif col == self.cols - 1:
                compare_three = [prev_row[self.cols - 3], prev_row[self.cols - 2], prev_row[self.cols - 1]]
            else:
                compare_three = [prev_row[col - 1], prev_row[col], prev_row[col + 1]]

            if compare_three in gen_one:
                next_row.append(1)
                if self.colorize:
                    next_row_colors.append(self.combination_colors[self.combinations.index(compare_three)])
                else:
                    next_row_colors.append(self.black)
            else:
                next_row.append(0)
                next_row_colors.append(self.white)

        return next_row, next_row_colors

    def draw_num_box(self, x, y, color):
        pygame.draw.rect(self.game_display, color,
                         (x, y, self.box_width, self.box_height))

    def draw_row(self, row, num_row, colors):
        row_y_pos = num_row * self.box_height
        count = 0
        for _ in row:
            self.draw_num_box(self.box_width * count, row_y_pos, colors[count])
            count += 1

    def draw_cells(self, rule):
        gen_one=[]
        count = 0
        for bit in rule:
            if bit == 1:
                gen_one.append(self.combinations[count])
            count += 1

        self.grid.append([0] * (((self.cols - self.starting_row.__len__()) / 2) + 1) + self.starting_row + [0] * (
        ((self.cols - self.starting_row.__len__())) + 1))

        row = 0
        while True:
            if row <= self.rows - 1:
                row_values = self.gen_next_row(self.grid[-1], gen_one)
                self.grid.append(row_values[0])
                self.draw_row(self.grid[-1], row, row_values[1])
            else:
                break

            pygame.display.update()

            row += 1

    def game_loop(self):
        pattern_num = 1
        while True:
            print pattern_num, '{0:08b}'.format(pattern_num)
            if pattern_num == 256:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            rule = [int(x) for x in list('{0:08b}'.format(pattern_num))]
            self.draw_cells(rule)
            self.screenshot(pattern_num)

            self.grid = []

            self.clock.tick(40)
            self.game_display.fill(self.white)
            pattern_num += 1

    def __init__(self):
        self.display_width = self.box_width * self.cols
        self.display_height = self.box_height * self.rows

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Elementary Cellular Automation")
        self.clock = pygame.time.Clock()

        self.game_loop()

        pygame.quit()
        quit()


if __name__ == "__main__":
    pygame.init()
    Base()
