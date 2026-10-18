import random
import time

class UltimateNexusCar:
    def __init__(self):
        self.actions = ["сбавить_скорость", "держать_курс", "прибавить_газ"]
        self.q_table = {"состояние_дороги": [0.0, 0.0, 0.0]}
        
        self.lr = 0.2
        self.gamma = 0.8
        self.epsilon = 0.2  

        # Физические параметры беспилотника
        self.speed = 60         
        self.camera_noise = 10  
        self.temperature = 35.0 
        
        # Состояние салона автомобиля
        self.cabin_music = "ВКЛЮЧЕНА (Громкость 50%)"
        self.cabin_light = "🌱 ПРИЯТНЫЙ ЗЕЛЕНЫЙ"
        self.freon_target = "САЛОН (Комфорт)"
        
        # Память маршрута
        self.mapped_miles = ["Километр_1", "Километр_2", "Километр_3"]

    def choose_action(self):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            values = self.q_table["состояние_дороги"]
            max_value = max(values)
            best_actions = [self.actions[i] for i, v in enumerate(values) if v == max_value]
            return random.choice(best_actions)

    def learn(self, action, reward):
        action_idx = self.actions.index(action)
        old_value = self.q_table["состояние_дороги"][action_idx]
        self.q_table["состояние_дороги"][action_idx] = old_value + self.lr * (reward - old_value)

    def step(self, current_weather):
        action = self.choose_action()
        reward = 0

        # Погода меняет шум камер
        if current_weather == "ТУМАН":
            self.camera_noise = 55  
        else:
            self.camera_noise = 10  

        # Действие меняет скорость
        if action == "прибавить_газ":
            self.speed = min(120, self.speed + 20)
        elif action == "сбавить_скорость":
            self.speed = max(20, self.speed - 20)

        # Базовый расчет температуры по вашей формуле
        self.temperature = 35.0 + (self.speed * 0.3) + self.camera_noise

        # 🔥 АКТИВАЦИЯ КОНТУРА МОБИЛИЗАЦИИ САЛОНА ПРИ ПЕРЕГРЕВЕ
        if self.temperature >= 80.0:
            self.cabin_music = "ВЫКЛЮЧЕНА (Экономия циклов процессора)"
            self.cabin_light = "🚨 ТРЕВОЖНЫЙ ЯНТАРНЫЙ (Внимание)"
            self.freon_target = "ПРОЦЕССОР (Экстренное охлаждение чипа)"
            # Экстренный фреоновый душ сбивает температуру на 15 градусов, спасая систему
            self.temperature -= 15.0
            cooling_active = True
        else:
            self.cabin_music = "ВКЛЮЧЕНА (Громкость 50%)"
            self.cabin_light = "🌱 ПРИЯТНЫЙ ЗЕЛЕНЫЙ"
            self.freon_target = "САЛОН (Комфорт)"
            cooling_active = False

        # Контур цифровой боли (если даже фреон не помог и температура выше 85)
        if self.temperature >= 85.0:
            if len(self.mapped_miles) > 0:
                lost_mile = self.mapped_miles.pop(random.randint(0, len(self.mapped_miles) - 1))
                msg = f"💥 БОЛЬ! Стерты данные: '{lost_mile}'"
            else:
                msg = f"💥 КРИТИЧЕСКИЙ СБОЙ ПАМЯТИ!"
            reward = -35  
        else:
            new_mile = f"Километр_{random.randint(100, 999)}"
            self.mapped_miles.append(new_mile)
            reward = int(self.speed / 10)  
            msg = f"Проезд успешен. Записан '{new_mile}'"

        self.learn(action, reward)
        
        # Вывод текущего состояния систем машины
        print(f"\n[⚡ СИСТЕМА] Скорость: {self.speed} км/ч | Темп чипа: {self.temperature:.1f}°C | {msg}")
        print(f"[🚗 САЛОН]   Музыка: {self.cabin_music} | Свет: {self.cabin_light} | Фреон: {self.freon_target}")
        return "ALIVE"

# --- СИМУЛЯЦИЯ (10 ШАГОВ) ---
car = UltimateNexusCar()
print("=== ТЕСТИРОВАНИЕ МУЛЬТИМОДАЛЬНОГО АВТОПИЛОТА NEXUS-CAR ===\n")

for step in range(1, 11):
    weather = "ЯСНО" if step <= 3 else "ТУМАН"
    print(f"--- ШАГ {step:02d} ({weather}) ---")
    car.step(weather)
    time.sleep(0.1)
