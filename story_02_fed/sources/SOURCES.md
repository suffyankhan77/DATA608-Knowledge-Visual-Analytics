# Data and methodological sources

- BLS Public Data API v2: https://www.bls.gov/developers/api_signature_v2.htm
- BLS CPI-U all items, seasonally adjusted (`CUSR0000SA0`): https://www.bls.gov/cpi/
- BLS civilian unemployment rate, seasonally adjusted (`LNS14000000`): https://www.bls.gov/cps/
- FRED monthly effective federal funds rate (`FEDFUNDS`): https://fred.stlouisfed.org/series/FEDFUNDS
- FRED mirrors of BLS CPI and unemployment (`CPIAUCSL`, `UNRATE`), used in the verified run after the BLS anonymous API quota was exhausted: https://fred.stlouisfed.org/series/CPIAUCSL and https://fred.stlouisfed.org/series/UNRATE
- Federal Reserve longer-run goals statement: https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf

The CPI index is converted into 12-month percentage change. The Fed's 2% inflation objective applies to PCE inflation, so CPI is a related indicator rather than the exact target measure. Maximum employment has no fixed unemployment threshold. Monthly data may be revised. The October 2025 BLS CPI and unemployment entries were unavailable in the downloaded series; no value was imputed. The presentation omits that month from the native charts, joining adjacent observed months, while Plotly displays a gap.

Retrieved on September 27, 2026. The notebook's printed status identifies whether a later run used the BLS API or FRED mirrors.

The `data/raw/` folder also includes two successful direct BLS API responses captured during development, covering CPI in 2000–2009 and unemployment in 2025–2026. They demonstrate the coded endpoint works for those requested periods. The full verified 25-year dataset used FRED mirrors after the shared anonymous BLS quota was reached. Do not describe these two partial responses as a full BLS API retrieval.
