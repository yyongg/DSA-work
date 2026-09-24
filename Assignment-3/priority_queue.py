from typing import Any
import heapq

"""
MinPriorityQueue maintains a priority queue where the lower
the priority value, the sooner the element will be removed from
the queue.

@param T the representation of the items in the queue
 """

class Min_Priority_Queue():
    def __init__(self) -> None:
        self.q: list[Any] = []
        self.entry_map: dict[Any,Any] = {} # to keep track of updated priorities

    def is_empty(self) -> bool:
        """
        return true if the queue is empty, false otherwise
        """
        return True if self.q else False

    def add_with_priority(self, elem: Any, priority: float):
        """
        Add [elem] with at level [priority]
        """
        self.entry_map[elem] = priority
        heapq.heappush(self.q,(elem,priority))

    def next_elem(self) -> Any:
        """
        Get the next (highest priority) element and remove this element from the queue.
        return the next element in terms of priority.  If empty, return null.
        """
        while self.q:
            priority, elem = heapq.heappop(self.q)

            # if element's priority does not match recorded on entry map, skip
            if elem not in self.entry_map or self.entry_map[elem] != priority:
                continue

            del self.entry_map[elem]
            return elem

        return None

    def adjust_priority(self, elem: Any, new_priority: float):
        """
        Adjust the priority of the given element
        param elem whose priority should change
        param newPriority the priority to use for the element
        the lower the priority the earlier the element int
        the order.
        """
        self.entry_map[elem] = new_priority
        heapq.heappush(self.q,(new_priority,elem))