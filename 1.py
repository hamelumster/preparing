
# Реализуем класс Stack
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def __size__(self):
        return len(self.items)


# Проверим сбалансированны ли последовательности скобок

def check_stack(string):
    stack = Stack()
    matching_brackets = {')': '(',
                         '}': '{',
                         ']': '['}

    for el in string:
        if el in matching_brackets.values():
            stack.push(el)
        elif el in matching_brackets.keys():
            if stack.is_empty() or stack.pop() != matching_brackets[el]:
                return 'Несбаланисированно'
    return 'Сбалансированно' if stack.is_empty() else 'Несбалансированно'


# Проверка
print(check_stack("(((([{}]))))"))           # Сбалансированно
print(check_stack("[([])((([[[]]])))]{()}")) # Сбалансированно
print(check_stack("{{[()]}}"))               # Сбалансированно
print(check_stack("}{}"))                    # Несбалансированно
print(check_stack("{{[(])]}}"))              # Несбалансированно
print(check_stack("[[{())}]"))               # Несбалансированно