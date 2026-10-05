"""Sorting algorithms implementation"""

def quick_sort(arr: list[int]) -> list[int]:
    """
    Uses quick sort approach to sort array in O(N) = nlog(n)
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[-1]
    left: list[int] = []
    right: list[int] = []

    for n in arr[:-1]:
        if n <= pivot:
            left.append(n)
        else:
            right.append(n)

    return quick_sort(left) + [pivot] + quick_sort(right)


def check_all(arr: list[int]) -> list[int]:
    """
    Checks all values against each other in array to get O(N) = n^2
    """
    res: list[int] = []

    for _ in range(len(arr)):
        min = arr[0]
        for n in arr:
            if n < min:
                min = n

        arr.remove(min)
        res.append(min)

    return res


def merge(left: list[int], right: list[int]) -> list[int]:
    """
    Helper function for merge sort
    left and right are both sorted lists
    """

    merged: list[int] = []
    l = r = 0

    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            merged.append(left[l])
            l+=1
        else:
            merged.append(right[r])
            r+=1

    merged += (left[l:] + right[r:])
    return merged


def merge_sort(arr: list[int]) -> list[int]:
    """
    Implementation of merge sort algorithm to achieve O(N) = nlog(n)
    """

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left_divided = merge_sort(left)
    right_divided = merge_sort(right)

    return merge(left_divided,right_divided)


def insertion_sort(arr: list[int]) -> list[int]:
    """
    Implementation of insertion sort algorithm to achieve O(n^2)
    """
    for i in range(1,len(arr)):
        key = arr[i]
        for j in range(i-1,-1,-1):
            if arr[j] > key:
                arr[j+1] = arr[j]
                arr[j] = key
            else:
                arr[j+1] = key
                break

    return arr
                
