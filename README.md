# QuantBot

QuantBot is a practical trading system foundation for Windows 10/11, Python 3.12+, and MetaTrader 5. The project is structured so it can be used for demo testing first and then evolved toward live operation with strict risk controls and a lightweight terminal dashboard.

## What is included

- modular Python package structure
- configuration-driven risk and strategy controls
- position sizing and risk guardrails
- MT5 connector abstraction with safe fallback behavior
- trade journaling and terminal monitoring
- automated tests for core components

## Project structure

- [quantbot](quantbot) - core trading engine package
  - [quantbot/strategy](quantbot/strategy) - strategy logic
  - [quantbot/risk](quantbot/risk) - risk and position sizing
  - [quantbot/mt5](quantbot/mt5) - MetaTrader 5 integration layer
  - [quantbot/utils](quantbot/utils) - helpers and environment loading
- [config](config) - configuration examples
- [tests](tests) - regression tests
- [run_demo.py](run_demo.py) - demo and dashboard entrypoint
- [run_dashboard.bat](run_dashboard.bat) - Windows launcher

## Requirements

- Python 3.12+
- Windows 10/11 64-bit
- MetaTrader 5 installed for real trading integration
- MetaTrader5 Python package for live broker connectivity

## Installation

```bat
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Running

```bat
python run_demo.py
```

Or on Windows:

```bat
run_dashboard.bat
```

## Configuration

Edit [.env.example](.env.example) and create a local .env with:

- MT5 terminal path
- MT5 login
- MT5 password
- MT5 server
- risk and sizing settings

## Live trading readiness

The system is now organized around the following live-trading principles:

- strict risk limits before order submission
- configuration-driven behavior rather than hard-coded parameters
- safe fallback when broker connectivity is unavailable
- structured logging and journaling for auditability
- low-overhead terminal monitoring for long-running operation

## Recommended next step

Use the project first in a MetaTrader 5 demo account, validate the connection and risk controls, then move to a live account only after stable behavior is confirmed.
