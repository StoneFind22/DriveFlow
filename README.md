# DriveFlow

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green?style=flat)
![SQL Server](https://img.shields.io/badge/SQL%20Server-Database-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Desktop car rental management system with clean architecture (MVVM + 3-Layer).

## Quick Start

```bash
git clone https://github.com/StoneFind22/DriveFlow.git
cd DriveFlow
python -m venv venv
source venv/bin/activate  # Windows: ./venv/Scripts/Activate
pip install -r requirements.txt
copy .env.example .env     # Edit with your credentials
python main.py
```

## Architecture

```
UI Layer (MVVM)
    ├── Views: Tkinter windows
    └── ViewModels: Presentation logic
    
Domain Layer
    ├── Models: Business entities
    ├── UseCases: Business logic
    └── Repositories: Contracts
    
Data Layer
    ├── DataSources: DB connections
    └── Repositories: Implementations
```

## Features

- Client CRUD operations
- Dark theme interface
- SOLID principles

## Requirements

- Python 3.8+
- SQL Server + ODBC Driver 17

## License

MIT © [StoneFind22](https://github.com/StoneFind22)
