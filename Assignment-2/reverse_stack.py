from stack_implementation import Stack
from typing import Any


def stackToList(stack: Stack) -> list[Any]:
    """
    Pops every element off [stack], top first.
    Note: this leaves the stack empty.
    """
    items: list[Any] = []
    while not stack.isEmpty():
        items.append(stack.pop())
    return items


stack: Stack = Stack()
for i in range(0, 10):
    stack.push(i)

rev_stack: Stack = Stack()
for i in range(9, -1, -1):
    rev_stack.push(i)

new_stack: Stack = Stack()
while not stack.isEmpty():
    new_stack.push(stack.pop())

print(stackToList(new_stack) == stackToList(rev_stack))