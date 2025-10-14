# Analysis of the various complexities and resources used: gate count, gate depth, and number of ancillas as n → ∞.

- Using the methods proposed in Barenco et al, the number of ancillas used is 0 for all n: O(1). 
- Gate count: at each level n of recursion, the number of gates is f(n) = 6(2) + 2 + f(n-1) = 14 + 14 + f(n-2) = 14(n-1) + 6 → O(14n - 8) = O(n)
- Gate depth: at each level n of recursion, the longest path is experienced by the target bit: f(n) = 5(2) + f(n-1) = 10 + 10 + f(n-2) = 10(n) --> O(n) also

