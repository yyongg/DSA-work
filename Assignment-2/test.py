import unittest

from doubly_linked_list import LinkedList
from queue_implementation import Queue
from stack_implementation import Stack


class TestLinkedList(unittest.TestCase):
    def setUp(self) -> None:
        self.list = LinkedList()

    # Empty list

    def testNewListIsEmpty(self):
        self.assertTrue(self.list.isEmpty())

    def testPeekEmptyReturnsNone(self):
        self.assertIsNone(self.list.peekFront())
        self.assertIsNone(self.list.peekBack())

    def testPopEmptyReturnsNone(self):
        self.assertIsNone(self.list.popFront())
        self.assertIsNone(self.list.popBack())
        self.assertTrue(self.list.isEmpty())

    # One element

    def testPushFrontOneElement(self):
        self.list.pushFront(1)
        self.assertFalse(self.list.isEmpty())
        self.assertEqual(self.list.peekFront(), 1)
        self.assertEqual(self.list.peekBack(), 1)

    def testPushBackOneElement(self):
        self.list.pushBack(1)
        self.assertFalse(self.list.isEmpty())
        self.assertEqual(self.list.peekFront(), 1)
        self.assertEqual(self.list.peekBack(), 1)

    def testPopFrontOnlyElementEmptiesList(self):
        self.list.pushBack(1)
        self.assertEqual(self.list.popFront(), 1)
        self.assertTrue(self.list.isEmpty())
        self.assertIsNone(self.list.peekFront())
        self.assertIsNone(self.list.peekBack())

    def testPopBackOnlyElementEmptiesList(self):
        self.list.pushFront(1)
        self.assertEqual(self.list.popBack(), 1)
        self.assertTrue(self.list.isEmpty())
        self.assertIsNone(self.list.peekFront())
        self.assertIsNone(self.list.peekBack())

    # Many elements

    def testPushFrontReversesOrder(self):
        for i in [1, 2, 3]:
            self.list.pushFront(i)
        self.assertEqual(self.list.peekFront(), 3)
        self.assertEqual(self.list.peekBack(), 1)
        self.assertEqual([self.list.popFront() for _ in range(3)], [3, 2, 1])
        self.assertTrue(self.list.isEmpty())

    def testPushBackKeepsOrder(self):
        for i in [1, 2, 3]:
            self.list.pushBack(i)
        self.assertEqual(self.list.peekFront(), 1)
        self.assertEqual(self.list.peekBack(), 3)
        self.assertEqual([self.list.popFront() for _ in range(3)], [1, 2, 3])
        self.assertTrue(self.list.isEmpty())

    def testPushBackThenPopBack(self):
        for i in [1, 2, 3]:
            self.list.pushBack(i)
        self.assertEqual([self.list.popBack() for _ in range(3)], [3, 2, 1])
        self.assertTrue(self.list.isEmpty())

    def testPushFrontThenPopBack(self):
        # Walks the prev pointers that pushFront sets up
        for i in [1, 2, 3]:
            self.list.pushFront(i)
        self.assertEqual([self.list.popBack() for _ in range(3)], [1, 2, 3])
        self.assertTrue(self.list.isEmpty())

    def testMixedPushes(self):
        self.list.pushBack(2)
        self.list.pushFront(1)
        self.list.pushBack(3)
        self.list.pushFront(0)
        self.assertEqual([self.list.popFront() for _ in range(4)], [0, 1, 2, 3])

    def testPopFromBothEnds(self):
        for i in [1, 2, 3, 4, 5]:
            self.list.pushBack(i)
        self.assertEqual(self.list.popFront(), 1)
        self.assertEqual(self.list.popBack(), 5)
        self.assertEqual(self.list.popFront(), 2)
        self.assertEqual(self.list.popBack(), 4)
        self.assertEqual(self.list.popFront(), 3)
        self.assertTrue(self.list.isEmpty())
        self.assertIsNone(self.list.popBack())

    def testPeekDoesNotRemove(self):
        self.list.pushBack(1)
        self.list.pushBack(2)
        self.assertEqual(self.list.peekFront(), 1)
        self.assertEqual(self.list.peekFront(), 1)
        self.assertEqual(self.list.peekBack(), 2)
        self.assertEqual(self.list.peekBack(), 2)
        self.assertEqual([self.list.popFront() for _ in range(2)], [1, 2])

    def testPeekAfterPop(self):
        for i in [1, 2, 3]:
            self.list.pushBack(i)
        self.list.popFront()
        self.assertEqual(self.list.peekFront(), 2)
        self.list.popBack()
        self.assertEqual(self.list.peekBack(), 2)
        self.assertEqual(self.list.peekFront(), 2)

    def testReuseAfterEmptying(self):
        self.list.pushBack(1)
        self.list.popBack()
        self.list.pushFront(2)
        self.list.pushBack(3)
        self.assertEqual(self.list.peekFront(), 2)
        self.assertEqual(self.list.peekBack(), 3)
        self.assertEqual([self.list.popFront() for _ in range(2)], [2, 3])

    def testFalsyValues(self):
        # 0, "" and False are real values, not "nothing"
        for value in [0, "", False]:
            self.list.pushBack(value)
        self.assertFalse(self.list.isEmpty())
        self.assertEqual(self.list.peekFront(), 0)
        self.assertEqual(self.list.popFront(), 0)
        self.assertEqual(self.list.popFront(), "")
        self.assertIs(self.list.popFront(), False)
        self.assertTrue(self.list.isEmpty())

    def testManyElements(self):
        for i in range(1000):
            self.list.pushBack(i)
        self.assertEqual([self.list.popFront() for _ in range(1000)], list(range(1000)))
        self.assertTrue(self.list.isEmpty())


class TestStack(unittest.TestCase):
    def setUp(self) -> None:
        self.stack = Stack()

    def testNewStackIsEmpty(self):
        self.assertTrue(self.stack.isEmpty())

    def testPeekEmptyReturnsNone(self):
        self.assertIsNone(self.stack.peek())

    def testPopEmptyReturnsNone(self):
        self.assertIsNone(self.stack.pop())
        self.assertTrue(self.stack.isEmpty())

    def testPushThenPeek(self):
        self.stack.push(1)
        self.assertFalse(self.stack.isEmpty())
        self.assertEqual(self.stack.peek(), 1)

    def testPeekShowsTop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.peek(), 2)

    def testPeekDoesNotRemove(self):
        self.stack.push(1)
        self.assertEqual(self.stack.peek(), 1)
        self.assertEqual(self.stack.peek(), 1)
        self.assertFalse(self.stack.isEmpty())

    def testLastInFirstOut(self):
        for i in [1, 2, 3]:
            self.stack.push(i)
        self.assertEqual([self.stack.pop() for _ in range(3)], [3, 2, 1])
        self.assertTrue(self.stack.isEmpty())
        self.assertIsNone(self.stack.pop())

    def testInterleavedPushPop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.stack.push(3)
        self.assertEqual(self.stack.peek(), 3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.isEmpty())

    def testReuseAfterEmptying(self):
        self.stack.push(1)
        self.stack.pop()
        self.stack.push(2)
        self.assertEqual(self.stack.peek(), 2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertTrue(self.stack.isEmpty())

    def testFalsyValue(self):
        self.stack.push(0)
        self.assertFalse(self.stack.isEmpty())
        self.assertEqual(self.stack.peek(), 0)
        self.assertEqual(self.stack.pop(), 0)
        self.assertTrue(self.stack.isEmpty())


class TestQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = Queue()

    def testNewQueueIsEmpty(self):
        self.assertTrue(self.queue.isEmpty())

    def testPeekEmptyReturnsNone(self):
        self.assertIsNone(self.queue.peek())

    def testDequeueEmptyReturnsNone(self):
        self.assertIsNone(self.queue.dequeue())
        self.assertTrue(self.queue.isEmpty())

    def testEnqueueThenPeek(self):
        self.queue.enqueue(1)
        self.assertFalse(self.queue.isEmpty())
        self.assertEqual(self.queue.peek(), 1)

    def testPeekShowsFront(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.peek(), 1)

    def testPeekDoesNotRemove(self):
        self.queue.enqueue(1)
        self.assertEqual(self.queue.peek(), 1)
        self.assertEqual(self.queue.peek(), 1)
        self.assertFalse(self.queue.isEmpty())

    def testFirstInFirstOut(self):
        for i in [1, 2, 3]:
            self.queue.enqueue(i)
        self.assertEqual([self.queue.dequeue() for _ in range(3)], [1, 2, 3])
        self.assertTrue(self.queue.isEmpty())
        self.assertIsNone(self.queue.dequeue())

    def testInterleavedEnqueueDequeue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.dequeue(), 1)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.peek(), 2)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertTrue(self.queue.isEmpty())

    def testReuseAfterEmptying(self):
        self.queue.enqueue(1)
        self.queue.dequeue()
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.peek(), 2)
        self.assertEqual([self.queue.dequeue() for _ in range(2)], [2, 3])
        self.assertTrue(self.queue.isEmpty())

    def testFalsyValue(self):
        self.queue.enqueue(0)
        self.assertFalse(self.queue.isEmpty())
        self.assertEqual(self.queue.peek(), 0)
        self.assertEqual(self.queue.dequeue(), 0)
        self.assertTrue(self.queue.isEmpty())


if __name__ == "__main__":
    unittest.main(verbosity=2)
