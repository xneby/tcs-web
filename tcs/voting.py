DIFFICULTY = (
	("Very Easy", 'warning'),
	("Easy", 'info'),
	("Medium", 'success'),
	("Hard", 'important'),
	("Very Hard", 'inverse'),
		)
COOLNESS = (
	("Boring", 'warning'),
	("Typical", 'info'),
	("Not Bad", 'success'),
	("Cool", 'important'),
	("Awesome", 'inverse'),
		)

def make_choices(x):
	for i, (y, _) in enumerate(x):
		yield (i, y)

DIFF_CHOICES = make_choices(DIFFICULTY)
COOL_CHOICES = make_choices(COOLNESS)
