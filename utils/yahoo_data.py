import pandas as pd
import yfinance as yf


def get_market_data(
    symbol,
    period="30d",
    interval="1h"
):

    try:

        df = yf.download(
            tickers=symbol,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
            threads=False
        )

        if df.empty:
            return pd.DataFrame()

        # Corrige MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Conversão numérica
        for col in [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]:

            if col in df.columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

        df.dropna(inplace=True)

        return df

    except Exception as e:

        print(
            f"Erro Yahoo Finance: {e}"
        )

        return pd.DataFrame()
