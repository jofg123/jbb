import databasemanager

name = 'Доктор кто'

hp = 100000 ** databasemanager.get_variable('doctor_num', 1)
damage_range =  ( 0, 50 )

coins = 0

loot = [ 'fez', 'laser_screwdriver' ]

def enter(user, reply):
	reply('Кто-кто?..')

	number = databasemanager.get_variable('doctor_num', 1)
	name = databasemanager.get_variable('doctor_killer')

	reply('Я — _{0}_й Доктор!'.format(number))

	if name is not None:
		reply('Я реинкарнация после убийства доктора от руки игрока {0}'.format(name))

def get_actions(user):
	return user.get_fight_actions() + [ 'Сдаться' ]

def make_damage(user, reply, dmg):
	hp = user.get_room_temp('hp', 0)
	hp -= max(1, dmg - user.rooms_count // 10)

	if hp <= 0:
		number = databasemanager.get_variable('doctor_num', 1)
		databasemanager.set_variable('doctor_num', number + 1)
		databasemanager.set_variable('doctor_killer', user.name)

		databasemanager.add_to_leaderboard(user, hp, databasemanager.DOCTOR_TABLE)
		user.won(reply)
	else:
		user.set_room_temp('hp', hp)

def action(user, reply, text):
	if text == 'Сдаться':
		reply('Доктор с ухмылкой сует Лазерную отвертку тебе в нос.')

		user.leave(reply)
	else:
		user.fight_action(reply, text)
