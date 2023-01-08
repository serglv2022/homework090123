class FlatIteratorPlus:

    def __init__(self, multilist):
        "Атрибут для хранения списка списков"
        self.multilist = multilist

    def __iter__(self):
        "Атрибуты для итерации по списку"
        self.iterators_queue = []  # определяем вложенный список для добавления элементов очереди итераторов
        self.current_iterator = iter(self.multilist)  # определяем итератор для списка
        return self

    def __next__(self):
        "Определяет и возвращает следующий элемент списка списков"
        while True:
            try:
                self.current_element = next(self.current_iterator)   # получаем следующий элемент списка
            except StopIteration:  # или получаем исключение, если следующий элемент отсутствует
                if not self.iterators_queue:  # если не осталось элементов в очереди, возвращаем исключение
                    raise StopIteration
                else:
                    self.current_iterator = self.iterators_queue.pop()  # или получаем следующий элемент очереди
                    continue
            if isinstance(self.current_element, list):  # проверяем тип следующего элемента (список или нет)
                self.iterators_queue.append(self.current_iterator)  # если список, то добавляем в очередь
                self.current_iterator = iter(self.current_element)  # смещаем указатель текущего итератора
            else:  # если не список, то возвращаем сам этот элемент
                return self.current_element
#---------------------------------------------------------------
def flat_generator_Plus(multilist):
    "Генератор позволяет  возвращать эелементы из списка списков с любым уровнем вложености"
    for element in multilist:
        if isinstance(element, list):  # узнаем, является ли следующий элемент списком
            for sub_elem in flat_generator_Plus(element):  # если список, то опять рекуррентно вызываем этот же генератор
                yield sub_elem
        else:
            yield element  # если не список, то возвращаем сам этот элемент
#---------------------------------------------------------------
if __name__ == '__main__':

    nested_list = [
        ['a', ['b'], 'c'],
        ['d', 'e', [[[[['f']]]]], 'h', False],
        [1, [[[2]]], None],
    ]

    print('_' * 30)
    print('Вызов расширенного итератора')
    for item in FlatIteratorPlus(nested_list):
        print(item)
    print('_' * 30)

    print('_' * 30)
    print('Вызов расширенного генератора')
    for item in flat_generator_Plus(nested_list):
        print(item)
    print('_' * 30)

    print('_' * 30)
    print('Вызов компоновки списка')
    flat_list = [item for item in FlatIteratorPlus(nested_list)]
    print(flat_list)
    print('_' * 30)
