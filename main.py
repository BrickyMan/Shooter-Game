from pygame import *
from random import randint

# Окно
WIDTH = 700
HEIGHT = 500
root = display.set_mode((WIDTH, HEIGHT))
bg = transform.scale(image.load('galaxy.jpg'), (WIDTH, HEIGHT))

# Игровой таймер
clock = time.Clock()

# Глобальные счётики
score = 0
lost = 0

class GameSprite(sprite.Sprite):
	def __init__(self, sprite_image, x, y, w, h, speed):
		sprite.Sprite.__init__(self)
		# Картинка объекта
		self.image = transform.scale(image.load(sprite_image), (w, h))
		self.speed = speed
		# Хитбокс
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	# Отрисовка объекта
	def redraw(self):
		root.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x > 5:
			self.rect.x -= self.speed
		if keys[K_RIGHT] and self.rect.x < WIDTH - 80:
			self.rect.x += self.speed

	# Выстрел
	def fire(self):
		bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15))

# Противник
class Enemy(GameSprite):
	def update(self):
		self.rect.y += self.speed
		global lost
		if self.rect.y > HEIGHT:
			self.rect.y = -40
			self.rect.x = randint(80, WIDTH - 80)
			lost += 1
			print(lost)

# Выстрел
class Bullet(GameSprite):
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y < 0:
			self.kill()

# Подготовка звука
mixer.init()
# Фоновый звук
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

# Подготовка шрифта
font.init()
my_font = font.Font(None, 36)
finish_font = font.Font(None, 60)

# Создание спрайтов
ship = Player('rocket.png', 5, 400, 80, 100, 10)

# Группа для спрайтов выстрелов
bullets = sprite.Group()
print()

# Группа для спрайтов противников
enemies = sprite.Group()
for i in range(5):
	enemies.add(Enemy('ufo.png', randint(80, WIDTH - 80), randint(-160, -40), 80, 50, randint(1, 5)))

# Флаги
game_on = True
finish = False

BLACK = (255, 255, 255)

# Игровой цикл
while game_on:
	# Перебор событий
	for e in event.get():
		if e.type == QUIT:
			game_on = False
		# Подписка на событие - выстрел
		elif e.type == KEYDOWN:
			if e.key == K_SPACE:
				fire_sound.play()
				ship.fire()

	if not finish:
		# Отрисовка фона
		root.blit(bg, (0, 0))

		# Вывод счёта
		text_score = my_font.render(f'Счёт: {score}', True, BLACK)
		root.blit(text_score, (10, 20))

		# Вывод пропущенных противников
		text_lost = my_font.render(f'Пропущено: {lost}', True, BLACK)
		root.blit(text_lost, (10, 50))

		# Обновление состояния корбаля
		ship.update()
		# Перерисовка корабля
		ship.redraw()

		# Обновление состояния выстрелов
		bullets.update()
		# Отрисовка выстрелов
		bullets.draw(root)

		# Обновление состояния противников
		enemies.update()
		# Отрисовка противников
		enemies.draw(root)

		# Столкновения групп спрайтов
		collides = sprite.groupcollide(enemies, bullets, True, True)
		# Цикл повторяется столько раз, сколько случилось коллизий
		for i in range(len(collides)):
			score += 1
			enemies.add(Enemy('ufo.png', randint(80, WIDTH - 80), randint(-160, -40), 80, 50, randint(1, 5)))

		# Коллизиция противников с игроком
		if sprite.spritecollide(ship, enemies, False) or lost >= 3:
			finish = True
			text_gameover = finish_font.render('Game over', True, BLACK)
			root.blit(text_gameover, (230, 230))

		if score >= 10:
			finish = True
			text_win = finish_font.render('You win!', True, BLACK)
			root.blit(text_win, (260, 230))

		# Обновление состояния игры
		display.update()
	# Частота обновления состояния игры
	clock.tick(60)