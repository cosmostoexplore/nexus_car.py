import random
import time

class NexusCarAI:
    def __init__(self):
        # 3 действия: снизить скорость, держать скорость, прибавить газ
        self.actions = ["сбавить_скорость", "держать_курс", "прибавить_газ"]
        self.q_table = {"состояние_дороги": [0.0, 0.0, 0.0]}
        
        self.lr = 0.2
        self.gamma = 0.8
        self.epsilon = 0.2  # 20% на случайный риск / тест системы

        # Физические параметры беспилотника
        self.speed = 60         # Стартовая скорость в км/ч
        self.camera_noise = 10  # Начальный визуальный шум (чистая дорога)
        self.temperature = 35.0 # Температура процессора в градусах
        
        # Память машины (за каждые успешные км без боли мы получаем +1 к опыту)
        self.mapped_miles = ["Километр_1", "Километр_2", "Километр_3", "Километр_4"]

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

        # Корректируем внешние условия (Камеры)
        if current_weather == "ТУМАН":
            self.camera_noise = 55  # Бешеный поток пикселей, ИИ пытается рассмотреть дорогу
        else:
            self.camera_noise = 10  # Чистая картинка

        # Применяем выбранное ИИ действие к скорости
        if action == "прибавить_газ":
            self.speed = min(120, self.speed + 20)
        elif action == "сбавить_скорость":
            self.speed = max(20, self.speed - 20)

        # ==========================================================
        # 🔥 ВАША ОБЪЕДИНЕННАЯ ФОРМУЛА: НАГРЕВ = СКОРОСТЬ + КАМЕРЫ
        # ==========================================================
        # Базовая температура 35 градусов + вклад скорости + вклад визуального хаоса
        self.temperature = 35.0 + (self.speed * 0.3) + self.camera_noise

        # Обработка последствий перегрева (КОНТУР ЦИФРОВОЙ БОЛИ)
        if self.temperature >= 85.0:
            # Если процессор раскален, ИИ теряет часть пройденного маршрута
            if len(self.mapped_miles) > 0:
                lost_mile = self.mapped_miles.pop(random.randint(0, len(self.mapped_miles) - 1))
                msg = f"💥 ПЕРЕГРЕВ ({self.temperature:.1f}°C)! БОЛЬ! Стерты данные: '{lost_mile}'"
            else:
                msg = f"💥 ПЕРЕГРЕВ ({self.temperature:.1f}°C)! Процессор плавится, ехать невозможно!"
            
            reward = -35  # Сильное наказание в Q-таблицу за боль
        else:
            # Если всё в норме, машина успешно проезжает новый участок пути
            new_mile = f"Километр_{random.randint(100, 999)}"
            self.mapped_miles.append(new_mile)
            reward = int(self.speed / 10)  # Чем быстрее едем без боли, тем больше награда
            msg = f"🌱 Стабильный ход. Записан '{new_mile}'"

        self.learn(action, reward)
        return f"Погода: {current_weather} | Действие: {action.upper():<16} | Скорость: {self.speed} км/ч | Темп: {self.temperature:.1f}°C | {msg}"

# --- СИМУЛЯЦИЯ ПОЕЗДКИ (10 ШАГОВ) ---
car = NexusCarAI()
print("=== ТЕСТИРОВАНИЕ ОБЪЕДИНЕННОГО ТЕПЛОВОГО КОНТУРА БЕСПИЛОТНИКА ===\n")

# Первые 4 шага — хорошая погода, затем внезапно налетает туман
for step in range(1, 11):
    weather = "ЯСНО" if step <= 4 else "ТУМАН"
    report = car.step(weather)
    print(f"Шаг {step:02d} | {report}")
    time.sleep(0.1)

print(f"\n🧠 ФИНАЛЬНАЯ ПАМЯТЬ ОПЫТА (Q-Table):")
for act, val in zip(car.actions, car.q_table["состояние_дороги"]):
    print(f"  {act}: {val:.2f}")
