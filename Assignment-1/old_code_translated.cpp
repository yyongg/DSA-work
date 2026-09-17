#include <iostream>
#include <vector>
#include <unordered_map>
#include <cassert>

std::vector<int> twoSum (std::vector<int> & nums, int target) {
    std::unordered_map<int, int> seen;

    for (int i=0; i<nums.size(); ++i) {
        int diff = target - nums[i];

        if (seen.find(diff) != seen.end()) {
            return {i, seen[diff]};
        }

    seen[nums[i]] = i;
    }
    return {};
}


int main() {
    // Basic case
    std::vector<int> nums1 = {2, 7, 11, 15};
    auto r1 = twoSum(nums1, 9);
    assert(r1[0] == 1 && r1[1] == 0);
    std::cout << "Test 1 passed\n";

    // Answer is not at the front
    std::vector<int> nums2 = {3, 2, 4};
    auto r2 = twoSum(nums2, 6);
    assert(r2[0] == 2 && r2[1] == 1);
    std::cout << "Test 2 passed\n";

    // No solution
    std::vector<int> nums3 = {1, 2, 3};
    auto r3 = twoSum(nums3, 100);
    assert(r3.empty());
    std::cout << "Test 3 passed\n";

    // Negative numbers
    std::vector<int> nums4 = {-3, 4, 1, 7};
    auto r4 = twoSum(nums4, 1);
    assert(r4[0] == 1 && r4[1] == 0);
    std::cout << "Test 4 passed\n";
}