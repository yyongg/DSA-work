# Exercise 3

## Question
How would you reverse the elements in a stack (i.e., put the elements at the top of the stack on the bottom and vice versa)? You can use as many additional stacks and queues as temporary storage in your approach.

## Solution
> Use a new stack, pop all elements on current stack into new stack. New stack is now the reverse of the old stack.

# Exercise 4

## Question
Come up with a strategy to solve the valid parentheses problem.

## Solution
> Create a mapping dictionary mapping each open brackets to a closed one. Then, create a stack to place all open brackets into. Lastly, iterate through list adding open brackets to stack and finding a match for every closed bracket encounter. If a match is not found after encountering a closed bracket, return False. Otherwise, after iterating through list, return True.

## Exercise 5

## Question
Solve the copy stack problem (source: University of Washington CSE122)

Given a stack return a copy of the original stack (i.e., a new stack with the same values as the original, stored in the same order as the original). Your method should create the new stack and fill it up with the same values that are stored in the original stack.

You may use one queue as auxiliary storage.

## Solution
> Iteratively pop all items of stack, enqueuing each into queue. Then, dequeue iteratively and push all dequeued items into a new stack. This stack should be the same as original stack.
