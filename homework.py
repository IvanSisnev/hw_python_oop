"""
Это программный модуль фитнес-трекера, который обрабатывает данные для
трех видов тренировок: бега, спортивной ходьбы и плавания.
Модуль принимает от блока датчиков информацию о прошедшей тренировке,
отрабатывает возможные ошибки некорректности данных, определяет
вид тренировки, рассчитывает результаты тренировки, выводит
информационное сообщение о результатах тренировки.
"""

# Импорт для аннотации типов при создании словаря типов тренировки и
# списка с данными тренировок
from typing import Dict, Type, List, Tuple


class InfoMessage:
    """
    Класс для создания информационного сообщения о тренировке.
    """

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = InfoMessage.formatted(duration)
        self.distance = InfoMessage.formatted(distance)
        self.speed = InfoMessage.formatted(speed)
        self.calories = InfoMessage.formatted(calories)

    @classmethod
    def formatted(cls, num: float) -> str:
        """
        Преобразовать число в строку с тремя знаками после запятой и
        вернуть ее.
        """
        return f'{num:.3f}'

    def get_message(self) -> str:
        """
        Создать и вернуть строку с информационным сообщением о
        тренировке.
        """
        message = (f'Тип тренировки: {self.training_type}; Длительность:'
                   f' {self.duration} ч.; Дистанция: {self.distance} км; Ср.'
                   f' скорость: {self.speed} км/ч; '
                   f'Потрачено ккал: {self.calories}.')
        return message


class Training:
    """
    Базовый класс тренировки. Родительский класс для классов типов
    тренировок: Running, SportsWalking и Swimming.
    """

    # Длина шага в метрах
    LEN_STEP: float = 0.65
    # Константа для перевода из метров в километры
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        # Количество шагов или гребков
        self.action = action
        # Продолжительность тренировки в часах
        self.duration = duration
        # Вес пользователя в кг
        self.weight = weight

    def get_distance(self) -> float:
        """
        Получить пройденную дистанцию в км.
        """
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """
        Получить и вернуть среднюю скорость движения.
        """
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий. Метод переопределяется
        в дочерних классах.
        """
        pass

    def show_training_info(self) -> InfoMessage:
        """
        Создать и вернуть информационное сообщение о выполненной
        тренировке.
        """
        result = InfoMessage(self.__str__(),
                             self.duration,
                             self.get_distance(),
                             self.get_mean_speed(),
                             self.get_spent_calories(),
                             )
        return result


class Running(Training):
    """
    Дочерний класс типа тренировки: бег.
    """

    # Коэффициенты для подсчета потраченных калорий в беге
    RUNNING_COEFFICIENT_1: int = 18
    RUNNING_COEFFICIENT_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """
        Вычислить и вернуть количество потраченных калорий.
        """
        calories = ((self.RUNNING_COEFFICIENT_1 * self.get_mean_speed() -
                     self.RUNNING_COEFFICIENT_2) * self.weight /
                    self.M_IN_KM * self.duration * 60)
        return calories

    def __str__(self) -> str:
        """
        Метод представления объекта класса в виде строки.
        """
        return 'Running'


class SportsWalking(Training):
    """
    Дочерний класс типа тренировки: спортивная ходьба.
    """

    # Коэффициенты для подсчета потраченных калорий в спортивной ходьбе
    WALKING_COEFFICIENT_1: float = 0.035
    WALKING_COEFFICIENT_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        # Рост пользователя в см
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Вычислить и вернуть количество потраченных калорий.
        """
        calories = ((self.WALKING_COEFFICIENT_1 * self.weight +
                     (self.get_mean_speed() ** 2 // self.height) *
                     self.WALKING_COEFFICIENT_2 * self.weight)
                    * self.duration * 60)

        return calories

    def __str__(self) -> str:
        """
        Метод представления объекта класса в виде строки.
        """
        return 'SportsWalking'


class Swimming(Training):
    """
    Дочерний класс типа тренировки: плавание.
    """

    # Длина гребка в метрах
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)

        # Длина бассейна в метрах
        self.length_pool = length_pool
        # Кол-во раз, которые ползователь проплыл бассейн в 1 сторону
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """
        Вычислить и вернуть количество потраченных калорий.
        """
        calories = (self.get_mean_speed() + 1.1) * 2 * self.weight

        return calories

    def get_mean_speed(self) -> float:
        """
        Получить и вернуть среднюю скорость движения.
        """
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration)

        return speed

    def __str__(self) -> str:
        """
        Метод представления объекта класса в виде строки.
        """
        return 'Swimming'


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
    invalid_key_message = 'Невозможно определить вид тренировки.'
    corrupt_data_message = 'Некорректные данные тренировки.'
    incomplete_data_message = 'Данные тренировки неполные.'

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
    # Вывести сообщение о некорректных данных тренировки
    else:
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
