# Intrusion Detection System using KMP String Matching Algorithm

This project demonstrates an Intrusion Detection System (IDS) that scans log files for known malicious patterns using the Knuth-Morris-Pratt (KMP) string matching algorithm. It also includes a naive string matching implementation for comparison.

## Project Structure

```
/intrusion_detection_kmp/
│
├── signatures.txt         # List of malicious patterns
├── sample_log.txt         # Sample data to scan
├── kmp.py                 # KMP algorithm implementation
├── naive_search.py        # Naive string matching (for comparison)
├── detect.py              # Main detection script
├── README.md              # Project documentation
```

## How to Run

1. Ensure you have Python installed on your system.
2. Navigate to the project directory:
   ```
   cd intrusion_detection_kmp
   ```
3. Run the detection script:
   ```
   python detect.py
   ```

## Expected Output

The script will scan the `sample_log.txt` file for malicious patterns listed in `signatures.txt` using both the KMP and naive search algorithms. It will print the matches found and the time taken by each algorithm.

## Customization

- Modify `signatures.txt` to add or remove malicious patterns.
- Replace `sample_log.txt` with your own log data for testing.

## Dependencies

- Python 3.x

## License

This project is open-source and available under the MIT License. 