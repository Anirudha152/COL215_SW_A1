# 2D Gate Packing Algorithm (COL215 Assignment 1)

**Authors:** Aditya Narware, Anirudha Saraf

## Project Description
This project implements a heuristic algorithm to solve a two-dimensional packing problem for gate-level circuit layouts. The objective is to arrange a set of rectangular logic gates, each with specified dimensions, into a non-overlapping physical layout that minimizes the area of the enclosing bounding box.

The algorithm effectively maximizes packing efficiency by minimizing blank space, adhering to the constraint that gates cannot be re-oriented or rotated.

## Algorithm Overview
The solution is inspired by skyline and bin-packing algorithms. The core logic involves the following steps:

1.  **Sorting:** Gates are first sorted in decreasing order of height to prioritize placing larger blocks first.
2.  **Width Iteration:** The algorithm iterates through potential bounding box widths starting from 1 up to the total area of the gates.
3.  **Bin Packing Strategy:**
    * Gates are placed into "bins" (empty rectangular spaces).
    * Placement uses a "bottom-left" heuristic: searching bins from bottom to top and placing the gate in the first bin where it fits, at the leftmost valid position.
4.  **Bin Splitting:** When a gate is placed, the remaining empty space in that bin is split into two new bins (one to the right and one above) to maintain efficient space usage.
5.  **Optimization:** The process is repeated by iterating over heights (sorting by width first) to ensure the global minimum area is found.

## Time Complexity
The time complexity analysis for the key components of the system is as follows:

* **Sorter:** $O(n \log n)$.
* **Packing Function:** $O(n^2)$ (dominated by the nested search for suitable bins).
* **Main Execution:** $O(n^2 \sqrt{A})$
    * Where $n$ is the number of gates and $A$ is the total area of all gates. The term $\sqrt{A}$ accounts for the loop iterating over possible widths.

## Detailed Results
The algorithm was tested extensively against various dataset types to ensure robustness. The tests were conducted with height and width limits set to 100 units.

### 1. Random Data
Standard random dataset where dimensions range from 1 to 100 units.

| Number of Gates | Time to Run (seconds) | Packing Efficiency |
| :--- | :--- | :--- |
| 25 | 0.02 | 0.91 |
| 50 | 0.04 | 0.91 |
| 100 | 0.14 | 0.94 |
| 250 | 0.70 | 0.96 |
| 500 | 1.91 | 0.97 |


### 2. Random Low Variance Data
Gates generated with low variance in dimensions to provide a uniform dataset.

| Number of Gates | Time to Run (seconds) | Packing Efficiency |
| :--- | :--- | :--- |
| 25 | 0.02 | 0.91 |
| 50 | 0.04 | 0.94 |
| 100 | 0.08 | 0.95 |
| 250 | 0.20 | 0.97 |
| 500 | 0.36 | 0.98 |


### 3. Random High Variance Data
Gates generated with significant differences in sizes to test handling of varied data.

| Number of Gates | Time to Run (seconds) | Packing Efficiency |
| :--- | :--- | :--- |
| 25 | 0.02 | 0.90 |
| 50 | 0.05 | 0.94 |
| 100 | 0.16 | 0.96 |
| 250 | 0.75 | 0.98 |
| 500 | 2.20 | 0.98 |


### 4. Extreme Aspect Ratio Data
Gates with very different width-to-height proportions.

| Number of Gates | Time to Run (seconds) | Packing Efficiency |
| :--- | :--- | :--- |
| 25 | 0.01 | 0.75 |
| 50 | 0.02 | 0.87 |
| 100 | 0.06 | 0.90 |
| 250 | 0.29 | 0.94 |
| 500 | 0.88 | 0.96 |


### 5. Random Squares
A dataset composed entirely of square gates with randomly chosen side lengths.

| Number of Gates | Time to Run (seconds) | Packing Efficiency |
| :--- | :--- | :--- |
| 25 | 0.02 | 0.94 |
| 50 | 0.05 | 0.94 |
| 100 | 0.16 | 0.96 |
| 250 | 0.80 | 0.97 |
| 500 | 2.54 | 0.98 |


### Accuracy Verification (Sample Cases)
Comparison of our output against the provided sample test case benchmarks.

| Case (Inputs) | Expected Output Area | Our Output Area |
| :--- | :--- | :--- |
| 1 (3 gates) | 110 | 110 |
| 2 (3 gates) | 30 | 30 |
| 3 (10 gates) | 1800 | 1800 |
| 4 (5 gates) | 80 | 90 |
| 5 (35 gates) | 500 | 518 |


## Visualization
The project includes a custom visualization module built with `tkinter` that renders the final calculated layout. This allows for visual verification of the optimized bounding box and gate positions.

## Usage
To run the packing algorithm:
```bash
# Example usage to run all testcases
python3 grid.py
```

## Disclaimer
This code was developed as part of an academic assignment for the COL215 course at IIT Delhi. It is intended for educational purposes and was completed in August 2024, it is no longer being actively updated or maintained, please reach out to me over email or linkedin for any queries. Please cite appropriately if used in research or projects. Please refer to the included report for more details

