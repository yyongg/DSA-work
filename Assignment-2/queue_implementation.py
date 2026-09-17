from typing import Any
from doubly_linked_list import LinkedList

class Queue:
    def __init__(self) -> None:
        self._list: LinkedList = LinkedList()

    def enqueue(self, data: Any):
        """
        Add [data] to the end of the queue.
        """
        self._list.pushBack(data)

    def dequeue(self) -> Any:
        """
        Remove the element at the front of the queue. If the queue is empty, it remains unchanged.

        Returns:
            The value at the front of the queue, or None if none exists.
        """
        return self._list.popFront()

    def peek(self) -> Any:
        """
        Returns:
            The value at the front of the queue, or None if none exists.
        """
        return self._list.peekFront()

    def isEmpty(self) -> bool:
        """
        Returns:
            True if the queue is empty and False otherwise.
        """
        return self._list.isEmpty()
