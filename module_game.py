from superwires import games
from random import randint


games.init(screen_width=626, screen_height=417, fps=50)
wall_image = games.load_image('background_1.jpg', transparent=False)
games.screen.background = wall_image

bin_banana = games.load_image('bin_1.png')
bin_bottle = games.load_image('bin_2.png')
bin_text = games.load_image('bin_3.png')
bin = games.load_image('bin.png')


class BinSprite(games.Sprite):
    def __init__(self, x, type_name):
        self.type_name = type_name
        if type_name == 'banana':
            super(BinSprite, self).__init__(image=bin_banana, x=x, y=350)
        elif type_name == 'bottle':
            super(BinSprite, self).__init__(image=bin_bottle, x=x, y=350)
        elif type_name == 'paper':
            super(BinSprite, self).__init__(image=bin_text, x=x, y=350)
        else:
            super(BinSprite, self).__init__(image=bin, x=x, y=350)

    # обработать клик
    def handle_click(self):
        if len(builder.visible_waste) > 0:
            lowest_waste = builder.visible_waste[0]
            if lowest_waste.type_name == self.type_name:
                builder.visible_waste.remove(lowest_waste)
                games.screen.remove(lowest_waste)

    def update(self):
        # вытягивать пересекающие спрайты
        overlapping_sprites = self.get_overlapping_sprites()

        for sprite in overlapping_sprites:
            if sprite.type_name != self.type_name:
                games.screen.quit()


class WasteSprite(games.Sprite):
    def __init__(self, image, type_name):
        self.type_name = type_name
        # dy - скорость падения вниз
        super(WasteSprite, self).__init__(image=image, x=games.screen.width / 2, y=games.screen.height - 417, dx=0, dy=2)


class WasteBuilderSprite(games.Sprite):

    def __init__(self):
        self.in_removal_mode = False
        self.click_was_handled = False
        # интервал появления мусора
        self.frames_interval = 60
        self.passed_frames = 0
        self.created_waste = 0
        self.visible_waste = []
        super(WasteBuilderSprite, self).__init__(image=bin, x=-200, y=-200)

    def update(self):
        # сколько прошло
        if self.passed_frames == 0:
            # +1 к созданому мусору
            self.created_waste += 1
            # дописать функцию
            new_waste = random_waste()
            self.visible_waste.append(new_waste)
            games.screen.add(new_waste)

        # прошол один кадр
        self.passed_frames += 1

        if self.passed_frames == self.frames_interval:
            self.passed_frames = 0

        if self.created_waste == 20:
            # уменшения интервала - сколько кадров пройдет между
            # появлением мусора
            self.frames_interval = 45
        elif self.created_waste == 40:
            self.frames_interval = 30
        elif self.created_waste == 60:
            self.frames_interval = 20

        # обработка клика мыши, 0 значит левая кнопка
        if games.mouse.is_pressed(0):
            # не в режиме удаления
            if self.in_removal_mode is False:
                self.in_removal_mode = True
                # клик еще не обработан
                self.click_was_handled = False
        # кнопку отпустили - выходим из режима удаления
        elif self.click_was_handled:
            self.in_removal_mode = False

        # в режиме удаления и еще не обработали клик
        if self.in_removal_mode and self.click_was_handled is False:
            if check_point(games.mouse.x, games.mouse.y, bin_banana):
                bin_banana.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bin_bottle):
                bin_bottle.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bin_paper):
                bin_paper.handle_click()

            self.click_was_handled = True

# создали 3 спрайта
bin_banana = BinSprite(x=106, type_name="banana")
bin_bottle = BinSprite(x=313, type_name="bottle")
bin_paper = BinSprite(x=521, type_name="paper")

builder = WasteBuilderSprite()

# точка внутри Спрайта
def check_point(x, y, sprite):
    return sprite.left <= x <= sprite.right and sprite.top <= y <= sprite.bottom


def random_waste():
    value = randint(1, 3)

    if value == 1:
        return banana_waste()
    elif value == 2:
        return bottle_waste()
    else:
        return paper_waste()


def banana_waste():
    return WasteSprite(image=games.load_image('banana_2.png'), type_name="banana")


def bottle_waste():
    return WasteSprite(image=games.load_image('bottle_2.png'), type_name="bottle")


def paper_waste():
    return WasteSprite(image=games.load_image('text-document_2.png'), type_name="paper")


games.screen.add(bin_banana)
games.screen.add(bin_bottle)
games.screen.add(bin_paper)
games.screen.add(builder)

games.screen.mainloop()
