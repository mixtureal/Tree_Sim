import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Паттерн "Стратегия" для расчета скорости роста
class GrowthStrategy(ABC):
    @abstractmethod
    def calculate_growth(self, environment, tree):
        pass

class DefaultGrowthStrategy(GrowthStrategy):
    def calculate_growth(self, environment, tree):
        # Простая формула роста: среднее из условий
        growth = (environment.temperature + environment.humidity + environment.light + environment.soil_quality + environment.precipitation) / 50
        return growth

class TemperatureGrowthStrategy(GrowthStrategy):
    def calculate_growth(self, environment, tree):
        # Рост зависит от температуры: оптимальная температура 20°C
        optimal_temp = tree.optimal_temperature
        deviation = abs(environment.temperature - optimal_temp)
        growth = max(0, 1 - (deviation / 50))  # Чем ближе к оптимальной, тем выше рост
        return growth * tree.base_growth_rate

class HumidityGrowthStrategy(GrowthStrategy):
    def calculate_growth(self, environment, tree):
        # Рост зависит от влажности: оптимальная влажность задана деревом
        optimal_humidity = tree.optimal_humidity
        deviation = abs(environment.humidity - optimal_humidity)
        growth = max(0, 1 - (deviation / 100))
        return growth * tree.base_growth_rate

class LightGrowthStrategy(GrowthStrategy):
    def calculate_growth(self, environment, tree):
        # Рост зависит от освещенности: оптимальная светимость задана деревом
        optimal_light = tree.optimal_light
        deviation = abs(environment.light - optimal_light)
        growth = max(0, 1 - (deviation / 1000))
        return growth * tree.base_growth_rate

class SoilQualityGrowthStrategy(GrowthStrategy):
    def calculate_growth(self, environment, tree):
        # Рост зависит от качества почвы: оптимальное значение задано деревом
        optimal_soil = tree.optimal_soil_quality
        deviation = abs(environment.soil_quality - optimal_soil)
        growth = max(0, 1 - (deviation / 100))
        return growth * tree.base_growth_rate

class PrecipitationGrowthStrategy(GrowthStrategy):
    def calculate_growth(self, environment, tree):
        # Рост зависит от количества осадков: оптимальное значение задано деревом
        optimal_precipitation = tree.optimal_precipitation
        deviation = abs(environment.precipitation - optimal_precipitation)
        growth = max(0, 1 - (deviation / 200))
        return growth * tree.base_growth_rate

# Класс для представления внешних условий
class Environment:
    def __init__(self, temperature=20, humidity=50, light=800, soil_quality=50, precipitation=100):
        self.temperature = temperature          # в градусах Цельсия
        self.humidity = humidity                # в процентах
        self.light = light                      # в люксах
        self.soil_quality = soil_quality        # индекс качества почвы (0-100)
        self.precipitation = precipitation      # количество осадков в мм

# Базовый класс дерева
class Tree(ABC):
    def __init__(self, name, height=0):
        self.name = name
        self.height = height  # в метрах
        self.growth_strategies = []
        self.history = [height]
        self.base_growth_rate = 1  # Базовая скорость роста

    def add_growth_strategy(self, strategy):
        self.growth_strategies.append(strategy)

    def grow(self, environment):
        total_growth = 0
        for strategy in self.growth_strategies:
            growth = strategy.calculate_growth(environment, self)
            total_growth += growth
        self.height += total_growth
        self.history.append(self.height)
        return total_growth

    @abstractmethod
    def species_characteristics(self):
        pass

# Конкретные виды деревьев
class Oak(Tree):
    def __init__(self, height=0):
        super().__init__("Дуб", height)
        self.add_growth_strategy(TemperatureGrowthStrategy())
        self.add_growth_strategy(PrecipitationGrowthStrategy())
        self.optimal_temperature = 20
        self.optimal_humidity = 50
        self.optimal_light = 700
        self.optimal_soil_quality = 60
        self.optimal_precipitation = 100
        self.base_growth_rate = 0.8

    def species_characteristics(self):
        return "Дуб - прочное дерево с медленным ростом."

class Pine(Tree):
    def __init__(self, height=0):
        super().__init__("Сосна", height)
        self.add_growth_strategy(LightGrowthStrategy())
        self.add_growth_strategy(SoilQualityGrowthStrategy())
        self.optimal_temperature = 15
        self.optimal_humidity = 40
        self.optimal_light = 900
        self.optimal_soil_quality = 50
        self.optimal_precipitation = 80
        self.base_growth_rate = 1.0

    def species_characteristics(self):
        return "Сосна - быстрорастущее дерево, предпочитающее солнечные места."

class Birch(Tree):
    def __init__(self, height=0):
        super().__init__("Береза", height)
        self.add_growth_strategy(HumidityGrowthStrategy())
        self.add_growth_strategy(SoilQualityGrowthStrategy())
        self.optimal_temperature = 18
        self.optimal_humidity = 60
        self.optimal_light = 800
        self.optimal_soil_quality = 55
        self.optimal_precipitation = 90
        self.base_growth_rate = 0.9

    def species_characteristics(self):
        return "Береза - дерево, хорошо растущее во влажных условиях."

class Maple(Tree):
    def __init__(self, height=0):
        super().__init__("Клен", height)
        self.add_growth_strategy(TemperatureGrowthStrategy())
        self.add_growth_strategy(HumidityGrowthStrategy())
        self.optimal_temperature = 16
        self.optimal_humidity = 55
        self.optimal_light = 850
        self.optimal_soil_quality = 65
        self.optimal_precipitation = 110
        self.base_growth_rate = 0.85

    def species_characteristics(self):
        return "Клен - красивое дерево с яркой листвой, предпочитает умеренный климат."

class Cherry(Tree):
    def __init__(self, height=0):
        super().__init__("Вишня", height)
        self.add_growth_strategy(TemperatureGrowthStrategy())
        self.add_growth_strategy(LightGrowthStrategy())
        self.optimal_temperature = 17
        self.optimal_humidity = 50
        self.optimal_light = 850
        self.optimal_soil_quality = 60
        self.optimal_precipitation = 95
        self.base_growth_rate = 0.95

    def species_characteristics(self):
        return "Вишня - плодовое дерево, требующее хорошего освещения и умеренного климата."

# Графический интерфейс
class TreeSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Симуляция роста деревьев")
        self.environment = Environment()
        self.forest = [
            Oak(),
            Pine(),
            Birch(),
            Maple(),
            Cherry()
        ]
        self.create_widgets()
        self.setup_plot()

    def create_widgets(self):
        # Фрейм для управления
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Ползунки для температуры
        ttk.Label(control_frame, text="Температура (°C):").pack(anchor=tk.W)
        self.temp_slider = ttk.Scale(control_frame, from_= -10, to=40, orient=tk.HORIZONTAL, command=self.update_temperature)
        self.temp_slider.set(self.environment.temperature)
        self.temp_slider.pack(fill=tk.X, pady=5)

        # Ползунки для влажности
        ttk.Label(control_frame, text="Влажность (%):").pack(anchor=tk.W)
        self.humidity_slider = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_humidity)
        self.humidity_slider.set(self.environment.humidity)
        self.humidity_slider.pack(fill=tk.X, pady=5)

        # Ползунки для освещенности
        ttk.Label(control_frame, text="Освещенность (люкс):").pack(anchor=tk.W)
        self.light_slider = ttk.Scale(control_frame, from_=0, to=2000, orient=tk.HORIZONTAL, command=self.update_light)
        self.light_slider.set(self.environment.light)
        self.light_slider.pack(fill=tk.X, pady=5)

        # Ползунки для качества почвы
        ttk.Label(control_frame, text="Качество почвы (0-100):").pack(anchor=tk.W)
        self.soil_slider = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_soil)
        self.soil_slider.set(self.environment.soil_quality)
        self.soil_slider.pack(fill=tk.X, pady=5)

        # Ползунки для осадков
        ttk.Label(control_frame, text="Осадки (мм):").pack(anchor=tk.W)
        self.precipitation_slider = ttk.Scale(control_frame, from_=0, to=300, orient=tk.HORIZONTAL, command=self.update_precipitation)
        self.precipitation_slider.set(self.environment.precipitation)
        self.precipitation_slider.pack(fill=tk.X, pady=5)

        # Кнопка для роста
        self.grow_button = ttk.Button(control_frame, text="Рост деревьев", command=self.grow_trees)
        self.grow_button.pack(pady=10)

        # Кнопка для сброса
        self.reset_button = ttk.Button(control_frame, text="Сброс", command=self.reset_simulation)
        self.reset_button.pack(pady=5)

        # Информация о деревьях
        info_frame = ttk.Frame(self.root)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.info_text = tk.Text(info_frame, height=15, state='disabled')
        self.info_text.pack(fill=tk.BOTH, expand=True)

    def setup_plot(self):
        # Настройка графика
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.lines = {}
        for tree in self.forest:
            line, = self.ax.plot([0], [tree.height], label=tree.name)
            self.lines[tree.name] = line
        self.ax.set_xlabel("Период")
        self.ax.set_ylabel("Высота (м)")
        self.ax.legend()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.period = 0

    def update_plot(self):
        self.period += 1
        for tree in self.forest:
            self.lines[tree.name].set_xdata(range(len(tree.history)))
            self.lines[tree.name].set_ydata(tree.history)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def update_temperature(self, val):
        self.environment.temperature = float(val)

    def update_humidity(self, val):
        self.environment.humidity = float(val)

    def update_light(self, val):
        self.environment.light = float(val)

    def update_soil(self, val):
        self.environment.soil_quality = float(val)

    def update_precipitation(self, val):
        self.environment.precipitation = float(val)

    def grow_trees(self):
        growth_info = ""
        for tree in self.forest:
            growth = tree.grow(self.environment)
            growth_info += f"{tree.name} выросло на {growth:.2f} м. Текущая высота: {tree.height:.2f} м.\n"
        self.display_info(growth_info)
        self.update_plot()

    def reset_simulation(self):
        for tree in self.forest:
            tree.height = 0
            tree.history = [0]
        self.period = 0
        self.ax.cla()
        for tree in self.forest:
            line, = self.ax.plot([0], [tree.height], label=tree.name)
            self.lines[tree.name] = line
        self.ax.set_xlabel("Период")
        self.ax.set_ylabel("Высота (м)")
        self.ax.legend()
        self.canvas.draw()
        self.display_info("Симуляция сброшена.\n")

    def display_info(self, text):
        self.info_text.config(state='normal')
        self.info_text.insert(tk.END, text + "\n")
        self.info_text.see(tk.END)
        self.info_text.config(state='disabled')

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeSimulationApp(root)
    root.mainloop()
