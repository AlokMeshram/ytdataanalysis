# 📊 YouTube Analytics Dashboard

A Flask-based web application that visualizes global YouTube statistics with interactive charts and data tables. The application loads data from CSV files into a local SQLite database and presents insights through a clean, responsive web interface.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-orange?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## ✨ Features

- 📈 **Interactive Data Visualization**: View YouTube channel statistics with dynamic charts
- 🗃️ **SQLite Database Integration**: Efficient local data storage and retrieval
- 🔄 **Flexible Data Loading**: Automatically normalizes CSV column names and handles various data formats
- 🌍 **Global Statistics**: Analyze YouTube channels by country and performance metrics
- 📱 **Responsive Design**: Clean, modern web interface that works on all devices
- 🛡️ **Error Handling**: Graceful handling of missing data or database issues

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/AlokMeshram/ytdataanalysis.git
   cd ytdataanalysis
   ```

2. **Create and activate a virtual environment**

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your data**
   - Place your `Global YouTube Statistics.csv` file in the project root directory
   - The CSV should contain columns like channel names, subscribers, views, and country data

5. **Load data into the database**
   ```bash
   python data_loader.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the dashboard**
   - Open your web browser and navigate to `http://127.0.0.1:5000/`
   - Click "Go to Dashboard" to view your analytics

## 📁 Project Structure

```
ytdataanalysis/
├── app.py                          # Main Flask application
├── data_loader.py                  # CSV to SQLite data loader
├── Global YouTube Statistics.csv   # Sample data file
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
└── youtube.db                     # SQLite database (created after data loading)
```

## 🛠️ Technologies Used

- **Backend**: Flask 3.0.3
- **Data Processing**: Pandas 2.2.2
- **Database**: SQLite with SQLAlchemy 2.0.35
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js (for data visualization)

## 📊 Data Format

The application expects CSV data with the following columns (column names are automatically normalized):

| Column | Description | Example |
|--------|-------------|---------|
| Channel Name | YouTube channel name | "MrBeast" |
| Subscribers | Number of subscribers | 100000000 |
| Views | Total channel views | 25000000000 |
| Country | Channel's country | "United States" |

**Note**: The data loader is flexible and can handle various column name formats (spaces, hyphens, different cases).

## 🔧 Configuration

### Custom CSV File
To use a different CSV file, modify the file path in `data_loader.py`:

```python
if __name__ == "__main__":
    load_data_to_db('your_custom_file.csv')
```

### Database Location
The SQLite database is created as `youtube.db` in the project root. To change this, update the `DB_PATH` in `app.py`.

## 🐛 Troubleshooting

### Common Issues

**"CSV file not found" error:**
- Ensure your CSV file is in the project root directory
- Check that the filename matches exactly (case-sensitive on some systems)

**Empty dashboard:**
- Verify that `data_loader.py` ran successfully
- Check that the `youtube.db` file was created
- Ensure your CSV has the expected column structure

**Module import errors:**
- Make sure you're in the activated virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Alok Meshram**
- GitHub: [@AlokMeshram](https://github.com/AlokMeshram)

## 🙏 Acknowledgments

- Thanks to the Flask community for the excellent documentation
- Chart.js for providing beautiful, responsive charts
- The open-source community for inspiration and best practices

---

⭐ If you found this project helpful, please consider giving it a star!
