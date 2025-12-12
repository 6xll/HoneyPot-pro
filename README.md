# HoneyPot 🍯

A comprehensive honeypot system built with Cowrie, featuring real-time monitoring and visualization through an ELK (Elasticsearch, Logstash, Kibana) dashboard.

## Overview

This project implements a honeypot infrastructure designed to detect, analyze, and visualize malicious activities. By simulating vulnerable systems, it attracts and logs attack attempts, providing valuable insights into attacker behavior and threat patterns.

## Architecture

The system consists of three main components:

### 1. **Cowrie Honeypot** 🐄
- Medium-interaction SSH and Telnet honeypot
- Simulates a vulnerable Linux shell environment
- Logs all interaction attempts, commands, and file downloads
- Captures attacker credentials and behavior patterns

### 2. **Data Processing with Pandas** 🐼
- Exports and processes Cowrie logs
- Cleans and transforms raw log data
- Prepares datasets for ingestion into the ELK stack
- Enables custom data analysis and filtering

### 3. **ELK Stack Dashboard** 📊
- **Elasticsearch**: Stores and indexes honeypot data
- **Logstash**: Processes and ingests log data
- **Kibana**: Provides real-time visualization and analytics

## Features

- ✅ Real-time attack monitoring
- ✅ Comprehensive logging of SSH/Telnet interactions
- ✅ Attacker behavior analysis
- ✅ Credential harvesting
- ✅ Geolocation tracking of attack sources
- ✅ Custom visualizations and dashboards
- ✅ Historical data analysis

## Architecture Diagram

```
[Attackers] 
    ↓
[Cowrie Honeypot] → [Logs]
    ↓
[Pandas Processing]
    ↓
[Logstash] → [Elasticsearch] → [Kibana Dashboard]
```

## Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.8+
- Pandas library
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Cowrie honeypot

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/6xll/HoneyPot.git
cd HoneyPot
```

### 2. Set Up Cowrie
```bash
# Install Cowrie dependencies
# Configure Cowrie to log in JSON format
# Start Cowrie honeypot
```

### 3. Install Python Dependencies
```bash
pip install pandas elasticsearch
```

### 4. Configure ELK Stack
```bash
# Start Elasticsearch, Logstash, and Kibana
# Configure Logstash pipeline for Cowrie logs
# Set up Kibana dashboards
```

## Usage

### Starting the Honeypot
```bash
# Start Cowrie honeypot
./start_cowrie.sh
```

### Processing Logs with Pandas
```bash
# Export and process Cowrie logs
python process_logs.py
```

### Viewing the Dashboard
Access Kibana dashboard at `http://localhost:5601`

## Data Analysis

The Pandas processing script performs:
- Log parsing and normalization
- Timestamp conversion
- IP geolocation enrichment
- Attack pattern identification
- Data export to Elasticsearch

## Dashboard Visualizations

The Kibana dashboard includes:
- Real-time attack attempts
- Geographic distribution of attackers
- Most common credentials used
- Command execution patterns
- Timeline of attack activities
- Top attacking IP addresses

## Configuration

### Cowrie Configuration
Edit `cowrie.cfg` to customize:
- Listening ports
- Hostname and system details
- Log output format
- File system simulation

### ELK Configuration
Modify `logstash.conf` for:
- Input sources
- Data parsing rules
- Output destinations

## Security Considerations

⚠️ **Important Security Notes:**
- Deploy honeypots in isolated network segments
- Never expose production systems
- Monitor honeypot activities regularly
- Ensure proper firewall rules are in place
- Keep all components updated

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Cowrie](https://github.com/cowrie/cowrie) - SSH/Telnet honeypot
- [Elastic Stack](https://www.elastic.co/elastic-stack) - Search and analytics
- [Pandas](https://pandas.pydata.org/) - Data analysis library

## Disclaimer

This honeypot system is designed for educational and research purposes. Use responsibly and in accordance with applicable laws and regulations. The author is not responsible for any misuse of this software.

## Contact

Project Maintainer: [@6xll](https://github.com/6xll)

Project Link: [https://github.com/6xll/HoneyPot](https://github.com/6xll/HoneyPot)

---

**Stay vigilant, stay secure! 🔒**