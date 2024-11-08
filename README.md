# Yatırım Bot | @yatirimhaberi | 2024
[![Made With Love](https://img.shields.io/badge/Made%20With-Love-orange.svg)](https://github.com/chetanraj/awesome-github-badges) [![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT) [![GitHub pull-requests](https://img.shields.io/github/issues-pr/Descite-Co/yatirimbot.svg)](https://GitHub.com/Descite-Co/yatirimbot/pulls/) [![GitHub pull-requests](https://img.shields.io/github/issues/Descite-Co/yatirimbot.svg)](https://GitHub.com/Descite-Co/yatirimbot/pulls/)

[![Twitter Follow](https://img.shields.io/twitter/follow/yatirimhaberi?style=social)](https://x.com/yatirimhaberi)

Yatırım Bot is a Python-based project designed to automate the sharing of financial updates and trading signals on Twitter. It provides timely information about market activities, including stock prices, commodities, and cryptocurrency updates, ensuring that users stay informed about critical financial events throughout the week.

## Installation

### Install UV

1. On macOS and Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. On Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. Using pip:
```bash
pip install uv
```

## Getting Started

1. Configure Environment Variables:
- `EMAIL`: Email of the sender
- `PASSWORD`: Password for the sender SMTP
- `RECEIVER`: Email for the receiver of test functions

2. Run the project:
```bash
uv run main.py
```

## Operating Schedule

### Weekdays (Monday - Friday)
- 10:17 - BIST market opening signal
- 10:20 - IPO operations
- 10:30 - Gold price update
- 11:30 - Silver price update
- 12:30 - Exchange rate update
- 13:30 - Natural Gas price update
- 16:00 & 16:46 - BIST 30 and US market opening
- 16:30 - Gold price update
- 18:17 - BIST market closing signal
- 19:30 - BIST 30 changes
- 20:00 & 20:30 - Crude Oil and BIST 30 changes
- 23:16 & 23:30 - US market closing and Heating Oil price update

### Daily (Including Weekends)
- 06:30 & 18:00 - Cryptocurrency updates
- 11:00, 15:00 & 19:00 - BIST stock operations based on timing
- 17:30 & 23:49 - Long-term stock updates

## Requirements
- Stable internet connection
- Accurate system time settings
- Python 3.x

## Repo Activity
![Alt](https://repobeats.axiom.co/api/embed/da97e089788d838318a0730bca98b374442292eb.svg "Repobeats analytics image")

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
