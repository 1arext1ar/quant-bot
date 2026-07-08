# QuantBot

QuantBot is a professional-grade quantitative trading system scaffold designed for Windows 10/11, Python 3.12+, and MetaTrader 5 integration. The project focuses on modularity, low resource usage, risk management, and a clean architecture suitable for expansion into a long-running live trading system.

## What is included

- Modular Python package structure with clear separation of concerns
- JSON-based configuration for symbols, risk, strategy, and MT5 settings
- Risk-based position sizing module
- Lightweight regime-based strategy scaffold
- MT5 connector abstraction for future live integration
- Demo runner and automated tests

## Project structure

- [quantbot](quantbot) - trading engine package
  - [quantbot/strategy](quantbot/strategy) - strategy modules
  - [quantbot/risk](quantbot/risk) - risk and position sizing
  - [quantbot/mt5](quantbot/mt5) - MetaTrader 5 connector layer
  - [quantbot/utils](quantbot/utils) - shared helpers
- [config](config) - configuration examples
- [tests](tests) - smoke tests for core logic
- [run_demo.py](run_demo.py) - simple demonstration entrypoint

## Requirements

- Python 3.12+
- Windows 10/11 64-bit
- MetaTrader 5 installed for real trading integration
- Optional: MetaTrader5 Python package for full broker connectivity

## Installation

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run the demo

```bash
python run_demo.py
```

## Configuration

Edit [config/example_config.json](config/example_config.json) to adjust:

- risk per trade
- daily stop limits
- lot size bounds
- symbols and timeframes
- MT5 credentials and terminal path

## Architecture notes

The current scaffold follows a pragmatic design:

- KISS and SOLID principles
- small modules with clear responsibilities
- configuration-driven behavior
- testable core logic before live connectivity
- a path for adding multi-symbol orchestration, logging, backtesting, and MT5 order management later

## Next steps for a production-ready system

To evolve this scaffold into a robust live trading platform, the next milestones are:

1. Add a real MetaTrader5 connector and order execution layer
2. Implement a market data adapter and multi-timeframe data pipeline
3. Add trade journaling, telemetry, and structured logging
4. Add a backtest engine and forward-test runner
5. Add drawdown protection, daily loss controls, and live monitoring dashboards

This project is intentionally conservative and modular so it can be maintained reliably over time.
