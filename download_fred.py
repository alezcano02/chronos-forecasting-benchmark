# Monthly macro series from FRED (Federal Reserve Bank of St. Louis), saved in one csv
import io

import pandas as pd
import requests

series = {
    "CPIAUCSL": "US consumer prices (CPI)", "PCEPI": "US PCE price index", "UNRATE": "US unemployment rate",
    "PAYEMS": "US nonfarm payrolls", "INDPRO": "US industrial production", "RSAFS": "US retail sales",
    "HOUST": "US housing starts", "M2SL": "US money supply M2", "UMCSENT": "US consumer sentiment (Michigan)",
    "GS10": "US 10-year Treasury yield", "FEDFUNDS": "Fed funds rate", "EXUSEU": "Dollar per euro",
    "CP0000EZ19M086NEST": "Euro area HICP", "LRHUTTTTFRM156S": "France unemployment rate",
    "IRLTLT01FRM156N": "France 10-year government bond yield", "CSUSHPISA": "US house prices (Case-Shiller)",
}
datos = []
for sid, nombre in series.items():
    r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": sid}, timeout=60)
    d = pd.read_csv(io.StringIO(r.text))
    d.columns = ["date", "value"]
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    d["series"], d["name"] = sid, nombre
    datos.append(d.dropna())
    print(sid, len(d), d["date"].min(), d["date"].max())
pd.concat(datos).to_csv("data/fred_monthly.csv", index=False)
