class Node[T]:
    def __init__(self, data: T):
        self.data: T = data
        self.next: Node = None  # Pointer to the next node
        self.prev: Node = None  # Pointer to the previous node


class LinkedList[T]:
    def __init__(self):
        self.head: T|None = None  # Start of the list
        self.tail: T|None = None  # End of the list
    
    """
    Adds the element [data] to the front of the linked list.
    """
    def pushFront(self, data: T):
        if not self.head:
            self.head = data

        else:
            

    """
     * Adds the element [data] to the back of the linked list.
    """
    def pushBack(self, data: T):
        return None

    """
     * Removes an element from the front of the list. If the list is empty, it is unchanged.
     * @return the value at the front of the list or nil if none exists
     """
    def popFront() -> T:
        return None

    """
     * Removes an element from the back of the list. If the list is empty, it is unchanged.
     * @return the value at the back of the list or nil if none exists
     """
    def popBack() -> T:
        return None

    """
     * @return the value at the front of the list or nil if none exists
     """
    def peekFront() -> T:
        return None

    """
     * @return the value at the back of the list or nil if none exists
     """
    def peekBack() -> T:
        return None

    """
     * @return true if the list is empty and false otherwise
     """
    def isEmpty() -> bool:
        return None