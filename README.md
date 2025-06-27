<<<<<<< HEAD
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
├── gui.py                 # Graphical user interface
├── launcher.py            # Application launcher (CLI or GUI)
├── app.py                 # Web application server
├── templates/             # HTML templates for web interface
├── static/                # Static files for web interface
│   ├── css/               # CSS stylesheets
│   └── js/                # JavaScript files
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
```

## How to Run

### Web Interface

1. Ensure you have Python installed on your system.
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the web server:
   ```
   python app.py
   ```
4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Using the Launcher (Desktop App)

1. Ensure you have Python installed on your system.
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the launcher script:
   ```
   python launcher.py
   ```
4. Choose between Command Line Interface or Graphical User Interface.

### Command Line Interface

1. Ensure you have Python installed on your system.
2. Navigate to the project directory:
   ```
   cd intrusion_detection_kmp
   ```
3. Run the detection script:
   ```
   python detect.py
   ```

### Graphical User Interface

1. Ensure you have Python installed on your system.
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the GUI:
   ```
   python gui.py
   ```

## Features

### Web Interface Features
- Modern, responsive interface accessible from any device with a browser
- Upload custom signature and log files
- Interactive results with performance comparison chart
- Tabbed interface to compare KMP and naive search algorithms
- Visual performance metrics

### GUI Features
- File selection for signature and log files
- Preview of signatures and log content
- Tabbed results showing both KMP and naive search matches
- Performance timing comparison between algorithms
- Simple controls for running detection and clearing results

## Expected Output

The system will scan log files for malicious patterns listed in signatures files using both the KMP and naive search algorithms. It will show matches found and the time taken by each algorithm.

## Customization

- Modify `signatures.txt` to add or remove malicious patterns.
- Replace `sample_log.txt` with your own log data for testing.

## Dependencies

- Python 3.x
- Tkinter (included with standard Python installation)
- Flask (for web interface)

## License

This project is open-source and available under the MIT License. 
=======
# DAA-lab-el
dijkstras shortest path
>>>>>>> ced6b04eaa15e4df779d200fed98dcd7a51b6ad4
