from random import randint
import requests
from datetime import datetime, timedelta  # Исправлено: добавлен timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.hp = randint(25,100)
        self.power = randint(15,40)
        self.last_feed_time = datetime.now()  # Добавлено: атрибут времени кормления

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "Pikachu"

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            shance = randint(1,5)
            if shance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "
        
    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now() 
        delta_time = timedelta(hours=feed_interval)
        
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            next_feed_time = self.last_feed_time + delta_time
            time_left = next_feed_time - current_time
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            return f"Следующее время кормления покемона через {hours} ч {minutes} мин"

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покемона: {self.name}, Здоровье: {self.hp} "

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

class Wizard(Pokemon):
    def feed(self, feed_interval=15, hp_increase=15):  # Добавлен метод feed для Wizard
        return super().feed(feed_interval, hp_increase)

class Fighter(Pokemon):
    def attack(self, enemy):
        super_power = randint(5,15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\n Боец применил супер-атаку силой:{super_power} "
    
    def feed(self, feed_interval=10, hp_increase=20):  # Добавлен метод feed для Fighter
        return super().feed(feed_interval, hp_increase)

# Тестирование
wizard = Wizard("pokemon1")
fighter = Fighter("pokemon2")

print(fighter.attack(wizard))
print(wizard.feed())  # Тест метода feed
print(fighter.feed())  # Тест метода feed