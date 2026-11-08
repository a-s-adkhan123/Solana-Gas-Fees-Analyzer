from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


@app.route('/')
def home():
    return render_template('index.html')


def get_sol_price():
    # Source 1: Binance
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price",
                         params={"symbol": "SOLUSDT"}, timeout=4)
        r.raise_for_status()
        return float(r.json()["price"])
    except Exception as e:
        print("[SOL] Binance failed:", e)

    # Source 2: Coinbase fallback
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/SOL-USD/spot", timeout=4)
        r.raise_for_status()
        return float(r.json()["data"]["amount"])
    except Exception as e:
        print("[SOL] Coinbase failed:", e)

    return 185.0  # last-resort default


@app.route('/api/tracker-data')
def get_tracker_data():
    return jsonify({"status": "success", "prices": {"SOL": get_sol_price()}})


@app.route('/api/solana-token')
def get_solana_token():
    address = request.args.get('address', '').strip()
    if not address:
        return jsonify({"status": "error", "message": "Missing address parameter"}), 400

    # Source 1: DexScreener (free, no key, covers pump.fun + graduated tokens)
    try:
        r = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address}",
                         headers=HEADERS, timeout=6)
        r.raise_for_status()
        pairs = r.json().get("pairs") or []

        # Only keep Solana pairs where YOUR token is the base token.
        # DexScreener also returns pairs where your token is the quote token,
        # and in those pairs priceUsd and the symbol belong to the OTHER token.
        pairs = [
            p for p in pairs
            if p.get("chainId") == "solana"
            and p.get("priceUsd")
            and (p.get("baseToken") or {}).get("address") == address
        ]
        if pairs:
            # pick the pair with the most liquidity
            best = max(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0)
            return jsonify({
                "status": "success",
                "price": float(best["priceUsd"]),
                "symbol": best["baseToken"].get("symbol", ""),
                "name": best["baseToken"].get("name", ""),
                "source": "dexscreener",
            })
        print("[TOKEN] DexScreener: no pair with this token as base for", address)
    except Exception as e:
        print("[TOKEN] DexScreener failed:", e)

    # Source 2: Jupiter price API (price only, no symbol)
    try:
        r = requests.get("https://lite-api.jup.ag/price/v3",
                         params={"ids": address}, headers=HEADERS, timeout=6)
        r.raise_for_status()
        entry = r.json().get(address)
        if entry and entry.get("usdPrice"):
            return jsonify({"status": "success", "price": float(entry["usdPrice"]),
                            "symbol": "", "name": "", "source": "jupiter"})
        print("[TOKEN] Jupiter: no price for", address)
    except Exception as e:
        print("[TOKEN] Jupiter failed:", e)

    # Source 3: pump.fun frontend API (bonding-curve tokens, may be blocked)
    try:
        r = requests.get(f"https://frontend-api-v3.pump.fun/coins/{address}",
                         headers=HEADERS, timeout=6)
        r.raise_for_status()
        coin = r.json()
        mc = coin.get("usd_market_cap")
        if mc:
            return jsonify({"status": "success", "price": float(mc) / 1_000_000_000.0,
                            "symbol": coin.get("symbol", ""), "name": coin.get("name", ""),
                            "source": "pump.fun"})
        print("[TOKEN] pump.fun: no usd_market_cap")
    except Exception as e:
        print("[TOKEN] pump.fun failed:", e)

    return jsonify({"status": "error", "message": "Token not found on any source"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)