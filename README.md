# DEX Aggregator Gas Fee Simulator

> Open-source Solana swap simulator. Look up any token by address, simulate a SOL swap, and estimate network fees at different transaction speeds. Built with Python, Flask and vanilla JS.

A small web app that estimates what a Solana token swap will cost in network fees. Paste any Solana token address, load its live price, and simulate a swap between SOL and that token.



## Features

- Live SOL price from Binance, with Coinbase as a fallback
- Token lookup by contract address, with price, ticker and name
- Swap simulator with a flip button and an input toggle for tokens or USD
- Network fee estimate in dollars and in SOL
- Three transaction speeds (Economy, Standard, Fast) that change the fee
- Automatic fallbacks between price sources if one fails

## How the fee is estimated

```
fee (lamports) = 5,000 base fee + (200,000 compute units x priority rate / 1,000,000)
fee (SOL)      = fee (lamports) / 1,000,000,000
fee (USD)      = fee (SOL) x current SOL price
```

The priority rates are fixed estimates:

| Speed    | Priority rate (microlamports per compute unit) |
|----------|------------------------------------------------|
| Economy  | 1,500                                          |
| Standard | 5,200                                          |
| Fast     | 92,000                                         |

These are not pulled from the live network yet (see Roadmap).

## Data sources

| Data           | Source                                              |
|----------------|-----------------------------------------------------|
| SOL price      | Binance, then Coinbase                              |
| Token price    | DexScreener, then Jupiter, then pump.fun            |

For DexScreener, the app only uses pairs where your token is the base token, so the price and ticker belong to the token you searched for.

## Getting started

### 1. Install Python

Download Python 3.8 or newer from [python.org/downloads](https://www.python.org/downloads/).

On Windows, tick **Add python.exe to PATH** on the first screen of the installer. Without it, the `python` and `pip` commands won't work in your terminal.

Check that it worked by opening a terminal and running:

```bash
python --version
```

On macOS and Linux you may need to use `python3` instead of `python`.

### 2. Get the code

With Git:

```bash
git clone https://github.com/a-s-adkhan123/Solana-Gas-Fees-Analyzer.git
cd Solana-Gas-Fees-Analyzer
```

Or on GitHub, click **Code** then **Download ZIP**, and unzip it. Keep the folder layout the same, because Flask needs `index.html` to stay inside the `templates` folder.

### 3. Install the dependencies

This project uses two Python libraries, Flask and Requests. There is nothing to enable. Installing them with `pip` is enough:

```bash
pip install -r requirements.txt
```

Or install them directly:

```bash
pip install flask requests
```

If you get "pip is not recognized" or "command not found", run it through Python instead:

```bash
python -m pip install flask requests
```

### 4. Run the app

**In a terminal:** from the project folder, run

```bash
python app.py
```

**In VS Code:**

1. Install [Visual Studio Code](https://code.visualstudio.com/) and the **Python** extension from the Extensions tab.
2. Choose **File > Open Folder** and open the project folder.
3. Open a terminal with **Terminal > New Terminal** (or press Ctrl+`).
4. Run `pip install -r requirements.txt`, then `python app.py`. You can also open `app.py` and click the **Run** (play) button at the top right.

Either way, open http://127.0.0.1:5000 in your browser when the terminal says the server is running. To stop the app, click the terminal and press Ctrl+C.

## Project structure

```
.
├── app.py              # Flask backend and price API routes
└── templates/
    └── index.html      # Frontend (HTML, CSS and JavaScript in one file)
```

## API routes

| Route                              | What it returns                                         |
|------------------------------------|---------------------------------------------------------|
| `GET /api/tracker-data`            | Current SOL price                                       |
| `GET /api/solana-token?address=`   | Price, symbol, name and source for a Solana token       |

## Troubleshooting

- **A token won't load:** very new tokens can take a minute or two to appear on DexScreener. Check the terminal, where each failed source prints a `[TOKEN]` line with the reason.
- **Price looks wrong:** compare it with the token's page on DexScreener. Thinly traded tokens can move quickly.
- **Fonts look different:** the page loads Manrope and JetBrains Mono from Google Fonts, so it needs an internet connection to match the screenshots.

## Roadmap

- Pull live priority fees from Solana's `getRecentPrioritizationFees` RPC method
- Add a README screenshot and a short demo clip
- Let the user set the compute unit limit

## Disclaimer

This is a personal project for learning and demonstration. Fee and token amounts are estimates, not quotes, and nothing here is financial advice. Memecoins are extremely risky, so do your own research.

## Contributing

Issues and pull requests are welcome.

## Note on AI

Parts of this code were generated with the help of AI.
