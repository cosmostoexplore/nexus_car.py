import random
import time

class PhysicalNexusCar:
    def __init__(self):
        # 1. Расширили арсенал действий — теперь ИИ может защищать свой гомеостаз сознательно
        self.actions = ["сбавить_скорость", "держать_курс", "прибавить_газ", "включить_охлаждение"]
        
        # Разделяем состояния дороги для Q-таблицы, чтобы робот понимал контекст
        self.q_table = {
            "НОРМА": [0.0, 0.0, 0.0, 0.0],
            "ГОЛОЛЁД": [0.0, 0.0, 0.0, 0.0]
        }
        
        self.lr = 0.3      # Чуть ускорили обучение для быстрой адаптации
        self.gamma = 0.8
        self.epsilon = 0.1 # ИИ стал еще опытнее

        # Физические параметры
        self.speed = 80         
        self.camera_noise = 10  
        self.abs_esp_load = 0   
        self.temperature = 35.0 
        
        # Состояние салона
        self.cabin_music = "ВКЛЮЧЕНА"
        self.cabin_light = "🌱 ЗЕЛЕНЫЙ"
        
        self.mapped_miles = ["Км_1", "Км_2", "Км_3"]

    def choose_action(self, road_condition):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            values = self.q_table[road_condition]
            max_value = max(values)
            best_actions = [self.actions[i] for i, v in enumerate(values) if v == max_value]
            return random.choice(best_actions)

    def learn(self, road_condition, action, reward):
        action_idx = self.actions.index(action)
        old_value = self.q_table[road_condition][action_idx]
        # Формула Q-обучения
        self.q_table[road_condition][action_idx] = old_value + self.lr * (reward - old_value)

    def step(self, weather, road_condition):
        action = self.choose_action(road_condition)
        reward = 0
        active_cooling_bonus = 0

        # 1. Влияние погоды на камеры
        self.camera_noise = 45 if weather == "ТУМАН" else 10

        # 2. Базовое влияние покрытия на датчики колес
        if road_condition == "ГОЛОЛЁД":
            self.abs_esp_load = 50 
        else:
            self.abs_esp_load = 0

        # 3. Обработка действий ИИ (Влияние на физику автомобиля)
        if action == "прибавить_газ":
            self.speed = min(120, self.speed + 20)
        elif action == "сбавить_скорость":
            self.speed = max(20, self.speed - 20)
            # Физическое исправление: на малой скорости датчики ABS/ESP реже пересчитывают данные
            if road_condition == "ГОЛОЛЁД" and self.speed <= 40:
                self.abs_esp_load = 20 
        elif action == "включить_охлаждение":
            # Робот тормозит двигателем и активирует внутренние вентиляторы вентиляции чипа
            self.speed = max(20, self.speed - 10)
            active_cooling_bonus = 25  # Прямой сброс тепла за счет действия

        # =====================================================================
        # 🔥 СБАЛАНСИРОВАННАЯ ФОРМУЛА НАГРЕВА
        # =====================================================================
        self.temperature = 35.0 + (self.speed * 0.25) + self.camera_noise + self.abs_esp_load - active_cooling_bonus

        # Аварийная автоматика (жесткий триггер гомеостаза, если ИИ сам не справился)
        if self.temperature >= 80.0:
            self.cabin_music = "ВЫКЛЮЧЕНА (Защита процессора)"
            self.cabin_light = "🚨 ТРЕВОЖНЫЙ ЯНТАРНЫЙ"
            self.temperature -= 15.0  # Автоматический впрыск фреона
        else:
            self.cabin_music = "ВКЛЮЧЕНА (Громкость 50%)"
            self.cabin_light = "🌱 ПРИЯТНЫЙ ЗЕЛЕНЫЙ"

        # Проверка целостности системы (Контур истинной боли)
        if self.temperature >= 85.0:
            if len(self.mapped_miles) > 0:
                lost_mile = self.mapped_miles.pop(random.randint(0, len(self.mapped_miles) - 1))
                msg = f"💥 БОЛЬ! Из-за перегрева стерт: '{lost_mile}'"
            else:
                msg = f"💥 КРИТИЧЕСКИЙ ТЕПЛОВОЙ СБОЙ!"
            reward = -50  # Увеличили штраф, чтобы робот быстрее понимал опасность
        else:
            new_mile = f"Км_{random.randint(100, 999)}"
            self.mapped_miles.append(new_mile)
            # Награда за безопасную и эффективную езду
            if road_condition == "НОРМА":
                reward = int(self.speed / 10)
            else:
                # На льду выживание в приоритете. Охлаждение дает бонус.
                reward = 15 if action in ["включить_охлаждение", "сбавить_скорость"] else -10

        self.learn(road_condition, action, reward)
        
        print(f"\n[Условия] {weather} | Дорога: {road_condition}")
        print(f"[⚡ Робот ] Действие: {action.upper()} | Скорость: {self.speed} км/ч | Чип: {self.temperature:.1f}°C")
        print(f"[🚗 Салон ] Музыка: {self.cabin_music} | Свет: {self.cabin_light} | {msg}")
        return "ALIVE"

# --- СИМУЛЯЦИЯ ПОЕЗДКИ С ДИНАМИЧЕСКИМ ГОМЕОСТАЗОМ (9 ШАГОВ) ---
car = PhysicalNexusCar()
print("=== ТЕСТИРОВАНИЕ СБАЛАНСИРОВАННОГО ИИ NEXUS-CAR ===\n")

for step in range(1, 10):
    if step <= 3:
        w, r = "ЯСНО", "НОРМА"
    elif step <= 6:
        w, r = "ТУМАН", "НОРМА"
    else:
        w, r = "ЯСНО", "ГОЛОЛЁД"  
        
    print(f"\n--- ШАГ {step:02d} ---")
    car.step(w, r)
    time.sleep(0.1)

# Выведем финальные знания робота о гололёде
print("\n=== Чему робот научился для ГОЛОЛЁДА (Q-значения) ===")
for act, val in zip(car.actions, car.q_table["ГОЛОЛЁД"]):
    print(f"Действие '{act}': {val:.2f}")
