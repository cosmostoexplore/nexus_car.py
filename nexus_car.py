import random
import time

class PhysicalNexusCar:
    def __init__(self):
        self.actions = ["сбавить_скорость", "держать_курс", "прибавить_газ"]
        self.q_table = {"состояние_дороги": [0.0, 0.0, 0.0]}
        
        self.lr = 0.2
        self.gamma = 0.8
        self.epsilon = 0.15  # Робот стал опытнее, меньше рискует наугад

        # Физические параметры беспилотника
        self.speed = 80         # Стартуем на хорошей скорости
        self.camera_noise = 10  
        self.abs_esp_load = 0   # Нагрузка от датчиков скольжения колес
        self.temperature = 35.0 
        
        # Состояние салона
        self.cabin_music = "ВКЛЮЧЕНА"
        self.cabin_light = "🌱 ЗЕЛЕНЫЙ"
        
        self.mapped_miles = ["Км_1", "Км_2", "Км_3"]

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

    def step(self, weather, road_condition):
        action = self.choose_action()
        reward = 0

        # 1. Влияние погоды на КАМЕРЫ
        self.camera_noise = 45 if weather == "ТУМАН" else 10

        # 2. Влияние покрытия на ДАТЧИКИ КОЛЕС (ABS/ESP)
        if road_condition == "ГОЛОЛЁД":
            # На льду частота расчетов микрозаносов увеличивается в разы
            self.abs_esp_load = 50 
        else:
            self.abs_esp_load = 0

        # Обработка действий ИИ
        if action == "прибавить_газ":
            self.speed = min(120, self.speed + 20)
        elif action == "сбавить_скорость":
            self.speed = max(20, self.speed - 20)

        # =====================================================================
        # 🔥 ФИНАЛЬНАЯ МУЛЬТИМОДАЛЬНАЯ ФОРМУЛА: НАГРЕВ = СКОРОСТЬ + КАМЕРЫ + ЛЕД
        # =====================================================================
        self.temperature = 35.0 + (self.speed * 0.25) + self.camera_noise + self.abs_esp_load

        # Аварийная мобилизация систем при перегреве
        if self.temperature >= 80.0:
            self.cabin_music = "ВЫКЛЮЧЕНА (Спасение процессора)"
            self.cabin_light = "🚨 ТРЕВОЖНЫЙ ЯНТАРНЫЙ"
            self.temperature -= 15.0  # Врубаем фреоновый обдув чипа
            cooling_active = True
        else:
            self.cabin_music = "ВКЛЮЧЕНА (Громкость 50%)"
            self.cabin_light = "🌱 ПРИЯТНЫЙ ЗЕЛЕНЫЙ"
            cooling_active = False

        # Контур истинной боли (разрушение структуры данных при перегреве)
        if self.temperature >= 85.0:
            if len(self.mapped_miles) > 0:
                lost_mile = self.mapped_miles.pop(random.randint(0, len(self.mapped_miles) - 1))
                msg = f"💥 БОЛЬ! Из-за перегрева стерт: '{lost_mile}'"
            else:
                msg = f"💥 КРИТИЧЕСКИЙ ТЕПЛОВОЙ СБОЙ!"
            reward = -40  
        else:
            new_mile = f"Км_{random.randint(100, 999)}"
            self.mapped_miles.append(new_mile)
            reward = int(self.speed / 10) if road_condition == "НОРМА" else int(self.speed / 20)
            msg = f"Отрезок пройден. Записан '{new_mile}'"

        self.learn(action, reward)
        
        print(f"\n[Условия] {weather} | Дорога: {road_condition}")
        print(f"[⚡ Робот ] Действие: {action.upper()} | Скорость: {self.speed} км/ч | Чип: {self.temperature:.1f}°C")
        print(f"[🚗 Салон ] Музыка: {self.cabin_music} | Свет: {self.cabin_light} | {msg}")
        return "ALIVE"

# --- СИМУЛЯЦИЯ ПОЕЗДКИ С РАЗНЫМИ ТИПАМИ ДОРОГИ (9 ШАГОВ) ---
car = PhysicalNexusCar()
print("=== ТЕСТИРОВАНИЕ ПОЛНОГО КОНТУРА ФИЗИЧЕСКОГО ИИ NEXUS-CAR ===\n")

for step in range(1, 10):
    # Динамически меняем условия: сначала ясно, потом туман на асфальте, потом чистый лед
    if step <= 3:
        w, r = "ЯСНО", "НОРМА"
    elif step <= 6:
        w, r = "ТУМАН", "НОРМА"
    else:
        w, r = "ЯСНО", "ГОЛОЛЁД"  # Солнечно, но дорога — зеркальный лед!
        
    print(f"\n--- ШАГ {step:02d} ---")
    car.step(w, r)
    time.sleep(0.1)
