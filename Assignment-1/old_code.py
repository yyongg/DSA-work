def twoSum(nums, target):
    seen = {}
    for i,num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [i,seen[diff]]
        seen[num] = i