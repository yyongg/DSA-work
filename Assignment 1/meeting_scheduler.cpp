#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;

struct Meeting {
    int start, end;
};

// 1

bool hasConflictNaive(vector<Meeting> meetings) {
    int n = meetings.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (meetings[i].start < meetings[j].end &&
                meetings[j].start < meetings[i].end)
                return true;
    return false;
}

// 2

bool hasConflictSorted(vector<Meeting> meetings) {
    sort(meetings.begin(), meetings.end(),
         [](const Meeting& a, const Meeting& b) { return a.start < b.start; });

    for (int i = 1; i < (int)meetings.size(); i++)
        if (meetings[i].start < meetings[i-1].end)
            return true;
    return false;
}

// unit tests

void runTests() {
    // basic overlap
    assert(hasConflictNaive({{1000,1100},{1300,1400},{1045,1130}}) == true);
    assert(hasConflictSorted({{1000,1100},{1300,1400},{1045,1130}}) == true);

    // no overlap
    assert(hasConflictNaive({{1000,1100},{1300,1400},{1130,1230}}) == false);
    assert(hasConflictSorted({{1000,1100},{1300,1400},{1130,1230}}) == false);

    // back-to-back meetings
    assert(hasConflictNaive({{1000,1100},{1100,1130},{1300,1400}}) == false);
    assert(hasConflictSorted({{1000,1100},{1100,1130},{1300,1400}}) == false);

    // 1 meeting
    assert(hasConflictNaive({{900,1000}}) == false);
    assert(hasConflictSorted({{900,1000}}) == false);

    // no meetings
    assert(hasConflictNaive({}) == false);
    assert(hasConflictSorted({}) == false);

    // identical meetings
    assert(hasConflictNaive({{900,1000},{900,1000}}) == true);
    assert(hasConflictSorted({{900,1000},{900,1000}}) == true);

    cout << "All tests passed.\n";
}

int main() {
    runTests();
}