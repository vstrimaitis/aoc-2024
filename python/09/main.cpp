#include <bits/stdc++.h>
using namespace std;

struct File {
    int id;
    int position;
    int size;
};

// ostream& operator<<(ostream& out, const File& f) {
//     return out << "File(" << f.id << ", " << f.position << ", " << f.size << ")";
// }

// void printSpaces(const map<int, set<int>>& spaces) {
//     for(auto& e : spaces) {
//         cout << e.first << ":";
//         for(auto x : e.second) {
//             cout << " " << x;
//         }
//         cout << endl;
//     }
// }

// incorrect, WIP
int main() {
    string s; cin >> s;

    vector<File> files;
    int currPos = 0;
    int currId = 0;
    for(int i = 0; i < s.length(); i += 2) {
        int size = s[i] - '0';
        files.push_back(File{currId, currPos, size});
        currId++;
        currPos += size;
        if (i+1 < s.length()) {
            currPos += s[i+1] - '0';
        }
    }
    
    map<int, set<int>> spaces;
    for(int i = 1; i < files.size(); i++) {
        auto f1 = files[i-1];
        auto f2 = files[i];
        int spaceStart = f1.position + f1.size;
        int spaceSize = f2.position - spaceStart;
        spaces[spaceSize].insert(spaceStart);
    }

    vector<File> newFiles;
    for(int i = files.size()-1; i >= 0; i--) {
        auto f = files[i];
        auto it = spaces.lower_bound(f.size);
        if (it == spaces.end()) { // not found
            newFiles.push_back(f);
        } else {
            int spaceSize = it->first;
            int pos = *it->second.begin();
            if (pos < f.position) {
                newFiles.push_back(File{f.id, pos, f.size});
                it->second.erase(pos);
                if (it->second.empty()) {
                    spaces.erase(spaceSize);
                }
                int newSpaceSize = spaceSize - f.size;
                int newSpacePosition = pos + f.size;
                spaces[newSpaceSize].insert(newSpacePosition);
            } else {
                newFiles.push_back(f);
            }
        }
    }

    sort(newFiles.begin(), newFiles.end(), [](auto f1, auto f2) {
        return f1.position < f2.position;
    });

    long long checksum = 0;
    int pos = 0;
    for(auto f : newFiles) {
        while(pos < f.position) {
            pos++;
        }
        for(int i = 0; i < f.size; i++) {
            checksum += pos * f.id;
            pos++;
        }
    }
    cout << checksum << endl;
}