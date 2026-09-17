from typing import Any
from doubly_linked_list import LinkedList

class Stack:
    def __init__(self) -> None:
        self._list: LinkedList = LinkedList()

    def push(self, data: Any):
        """
        Add [data] to the top of the stack.
        """
        self._list.pushFront(data)

    def pop(self):
        """
        Remove the element at the top of the stack. If the stack is empty, it remains unchanged.

        Returns:
            The value at the top of the stack, or None if none exists.
        """
        return self._list.popFront()

    def peek(self):
        """
        Returns:
            The value on the top of the stack, or None if none exists.
        """
        return self._list.peekFront()

    def isEmpty(self) -> bool:
        """
        Returns:
            True if the stack is empty and False otherwise.
        """
        return self._list.isEmpty()
