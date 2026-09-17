from typing import Optional, Any

class Node:
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional[Node] = None  # Pointer to the next node
        self.prev: Optional[Node] = None  # Pointer to the previous node


class LinkedList:
    def __init__(self):
        self.head: Any = None  # Start of the list
        self.tail: Any = None  # End of the list

    def pushFront(self, data: Any):
        """
        Adds the element [data] to the front of the linked list.
        """
        node: Node = Node(data)

        if not self.head:  # if list empty
            self.tail = node

        else:
            node.next = self.head
            self.head.prev = node

        self.head = node

    def pushBack(self, data: Any):
        """
        Adds the element [data] to the back of the linked list.
        """
        node: Node = Node(data)

        if not self.head:  # if list empty
            self.head = node

        else:
            node.prev = self.tail
            self.tail.next = node

        self.tail = node

    def popFront(self) -> Any:
        """
        Removes an element from the front of the list. If the list is empty, it is unchanged.

        Returns:
            The value at the front of the list, or None if none exists.
        """
        if not self.head:
            return None

        elif self.head == self.tail:
            pop: Any = self.head.data
            self.head = None
            self.tail = None

        else:
            pop: Any = self.head.data
            self.head = self.head.next
            self.head.prev = None

        return pop

    def popBack(self) -> Any:
        """
        Removes an element from the back of the list. If the list is empty, it is unchanged.

        Returns:
            The value at the back of the list, or None if none exists.
        """
        if not self.tail:
            return None

        elif self.head == self.tail:
            pop: Any = self.head.data
            self.head = None
            self.tail = None

        else:
            pop: Any = self.tail.data
            self.tail = self.tail.prev
            self.tail.next = None

        return pop

    def peekFront(self) -> Any:
        """
        Returns:
            The value at the front of the list, or None if none exists.
        """
        return self.head.data

    def peekBack(self) -> Any:
        """
        Returns:
            The value at the back of the list, or None if none exists.
        """
        return self.tail.data

    def isEmpty(self) -> bool:
        """
        Returns:
            True if the list is empty and False otherwise.
        """
        return self.head
