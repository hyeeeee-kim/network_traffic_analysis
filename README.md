# Network Traffic Analysis

This project analyzes network traffic data to identify cybersecurity attacks and gain insights into network protocols and packet behavior.

## Features
- Load and analyze network traffic data from CSV files
- Visualize attack types, protocol distribution, and packet statistics
- Interactive web interface built with Flask and Jinja2 templates
- Multiple analysis views: attack type, protocol, packet analysis

## Project Structure
```
app.py                # Main Flask application
requirements.txt      # Python dependencies

data/
  cybersecurity_attacks.csv  # Sample network traffic dataset
  README.md                  # Data description

templates/
  *.html               # Jinja2 HTML templates for web views

venvs/
  network_dataproject/ # Python virtual environment
```

## Getting Started
1. **Clone the repository**
2. **Create and activate a Python virtual environment**
   - Example: `python -m venv venvs/network_dataproject`
   - Activate: `venvs/network_dataproject/Scripts/activate` (Windows)
3. **Install dependencies**
   - `pip install -r requirements.txt`
4. **Run the application**
   - `python app.py`
5. **Open your browser**
   - Visit `http://localhost:5000`

## Dependencies
- Flask
- pandas
- matplotlib
- seaborn

## Data
The main dataset is located in `data/cybersecurity_attacks.csv`. See `data/README.md` for details.

## License
This project is for educational purposes.
