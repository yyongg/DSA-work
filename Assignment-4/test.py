"""test cases for sorting algorithms"""

from sort_algorithms import quick_sort, check_all, merge_sort, insertion_sort
import random

arr1 = random_ints = [random.randint(1, 50) for _ in range(10)]
print(f"Random List: {random_ints}\n")

ans = sorted(arr1)
quick_sort_res = quick_sort(arr1)
check_all_res = check_all(arr1.copy())
merge_sort_res = merge_sort(arr1)
insertion_sort_res = insertion_sort(arr1.copy())

print(f"""
Quick Sort: {quick_sort_res} {quick_sort_res==ans}
Check All: {check_all_res} {check_all_res==ans}
Merge Sort: {merge_sort_res} {merge_sort_res==ans}
Insertion Sort: {insertion_sort_res} {insertion_sort_res==ans}
""")