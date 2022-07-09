"""
Это программный модуль фитнес-трекера, который обрабатывает данные для
трех видов тренировок: бега, спортивной ходьбы и плавания.
Модуль принимает от блока датчиков информацию о прошедшей тренировке,
отрабатывает возможные ошибки некорректности данных, определяет
вид тренировки, рассчитывает результаты тренировки, выводит
информационное сообщение о результатах тренировки.
"""

from dataclasses import dataclass
# Импорт для аннотации типов при создании словаря типов тренировки и
# списка с данными тренировок
from typing import Dict, Type, List, Tuple, ClassVar


@dataclass
class InfoMessage:
    """
    Класс для создания информационного сообщения о тренировке.
    """

    # Вид тренировки
    training_type: str
    # Продолжительность тренировки в часах
    duration: float
    # Пройденная дистанция в километрах
    distance: float
    # Скорость в км/ч
    speed: float
    # Потраченные калории
    calories: float

    def get_message(self) -> str:
        """
        Создать и вернуть строку с информационным сообщением о
        тренировке.
        """
        return (f'Тип тренировки: {self.training_type}; Длительность:'
                f' {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} '
                f'км; Ср. скорость: {self.speed:.3f} '
                f'км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.')


@dataclass
class Training:
    """
    Базовый класс тренировки. Родительский класс для классов типов
    тренировок: Running, SportsWalking и Swimming.
    """

    # Количество шагов или гребков
    action: int
    # Продолжительность тренировки в часах
    duration: float
    # Вес пользователя в кг
    weight: float

    # Длина шага в метрах
    LEN_STEP: ClassVar[float] = 0.65
    # Константа для перевода из метров в километры
    M_IN_KM: ClassVar[int] = 1000
    # Константа для перевода часов в минуты
    MINUTES_PER_HOUR: ClassVar[int] = 60
    # Коэффициенты для расчета потраченных калорий
    CALORIES_COEFFICIENT_1: ClassVar[int] = 2
    CALORIES_COEFFICIENT_2: ClassVar[float] = 1.1

    def get_distance(self) -> float:
        """
        Получить пройденную дистанцию в км.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """
        Получить и вернуть среднюю скорость движения.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий. Метод переопределяется
        в дочерних классах.
        """
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """
        Создать и вернуть информационное сообщение о выполненной
        тренировке.
        """
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


@dataclass
class Running(Training):
    """
    Дочерний класс типа тренировки: бег.
    """

    # Коэффициенты для подсчета потраченных калорий в беге
    RUNNING_COEFFICIENT_1: ClassVar[int] = 18
    RUNNING_COEFFICIENT_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """
        Вычислить и вернуть количество потраченных калорий.
        """
        return ((self.RUNNING_COEFFICIENT_1 * self.get_mean_speed()
                 - self.RUNNING_COEFFICIENT_2) * self.weight
                / self.M_IN_KM * self.duration * self.MINUTES_PER_HOUR)


@dataclass
class SportsWalking(Training):
    """
    Дочерний класс типа тренировки: спортивная ходьба.
    """

    # Рост пользователя в см
    height: float

    # Коэффициенты для подсчета потраченных калорий в спортивной ходьбе
    WALKING_COEFFICIENT_1: ClassVar[float] = 0.035
    WALKING_COEFFICIENT_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """
        Вычислить и вернуть количество потраченных калорий.
        """
        return ((self.WALKING_COEFFICIENT_1 * self.weight
                 + (self.get_mean_speed()
                    ** self.CALORIES_COEFFICIENT_1
                    // self.height) * self.WALKING_COEFFICIENT_2
                 * self.weight) * self.duration
                * self.MINUTES_PER_HOUR)


@dataclass
class Swimming(Training):
    """
    Дочерний класс типа тренировки: плавание.
    """

    # Длина бассейна в метрах
    length_pool: int = 0
    # Кол-во раз, которые ползователь проплыл бассейн в 1 сторону
    count_pool: int = 0

    # Длина гребка в метрах
    LEN_STEP: ClassVar[float] = 1.38

    def get_spent_calories(self) -> float:
        """
        Вычислить и вернуть количество потраченных калорий.
        """
        return ((self.get_mean_speed() + self.CALORIES_COEFFICIENT_2)
                * self.CALORIES_COEFFICIENT_1 * self.weight)

    def get_mean_speed(self) -> float:
        """
        Получить и вернуть среднюю скорость движения.
        """
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)


def read_package(workout_category: str, workout_data: List) -> Training:
    """
    Принять пакет данных, полученный от датчиков, содержащий строку с
    типом активности и список с данными тренировки.
    Определить класс, соответствующий полученному типу активности.
    Вернуть объект класса с передачей ему параметров путем распаковки
    списка данных.
    """
    # Словарь с кодами активности и соответствующими им классами
    workout_codes_classes: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    # Сообщения об ошибках данных
    invalid_key_message: str = 'Невозможно определить вид тренировки.'
    corrupt_data_message: str = 'Некорректные данные тренировки.'
    incomplete_data_message: str = 'Данные тренировки неполные.'

    # Присвоить переменной соответствующий класс из словаря
    try:
        workout_class = workout_codes_classes[workout_category]
    # Отработка ошибки некорректного вида тренировки
    except KeyError:
        print(invalid_key_message)
        raise SystemExit

    # Проверить корректность данных тренировки
    if all(isinstance(num, int) for num in workout_data):
        # Вернуть объект соответствующего класса с нужными параметрами
        try:
            object_training = workout_class(*workout_data)
        # Отработка ошибки недостающих данных тренировки
        except TypeError:
            print(incomplete_data_message)
            raise SystemExit
        return object_training
    # В случае ошибки вывести сообщение о некорректных данных тренировки
    print(corrupt_data_message)
    raise SystemExit


def main(training_class_object: Training) -> None:
    """
    Главная функция модуля.
    Принять экземпляр класса Training.
    Вызвать для него метод, возвращающий экземпляр класса InfoMessage, и
    присвоить его переменной.
    Вызвать для переменной метод, возвращающий строку с результатами
    тренировки.
    Вывести строку на экран.
    """
    # Присвоить переменной значение экземпляра класса InfoMessage
    info = training_class_object.show_training_info()

    # Вывести на экран строку с результатами тренировки
    print(info.get_message())
    return None


if __name__ == '__main__':
    # Список кортежей с информацией о тренировках
    packages: List[Tuple[str, List[float]]] = [
        ('SWM', [720, 1, 80, 25, 40, ]),
        ('RUN', [15000, 1, 75, ]),
        ('WLK', [9000, 1, 75, 180, ]),
    ]

    # Сообщение о некорректности данных
    bad_package_message: str = 'Тестовый пакет содержит некорректные данные.'

    # Распаковка списка с информацией о тренировках
    try:
        for workout_type, data in packages:
            # Создание объектов класса Training
            training = read_package(workout_type, data)
            # Обращение к главной функции модуля
            main(training)
    # Отработка ошибки недостающих данных
    except ValueError:
        print(bad_package_message)
        raise SystemExit
