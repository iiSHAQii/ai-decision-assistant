"""Static ISO 3166-1 alpha-2 -> alpha-3 mapping for common countries.

Open-Meteo geocoding returns alpha-2 codes; the World Bank API consumes
alpha-3. This map covers the countries most likely to appear in our demo
inputs. Add entries as new use cases come up — these codes don't change.
"""

ISO2_TO_ISO3: dict[str, str] = {
    "AR": "ARG", "AT": "AUT", "AU": "AUS", "BE": "BEL", "BG": "BGR",
    "BR": "BRA", "CA": "CAN", "CH": "CHE", "CL": "CHL", "CN": "CHN",
    "CO": "COL", "CZ": "CZE", "DE": "DEU", "DK": "DNK", "EE": "EST",
    "EG": "EGY", "ES": "ESP", "FI": "FIN", "FR": "FRA", "GB": "GBR",
    "GR": "GRC", "HK": "HKG", "HR": "HRV", "HU": "HUN", "ID": "IDN",
    "IE": "IRL", "IL": "ISR", "IN": "IND", "IS": "ISL", "IT": "ITA",
    "JP": "JPN", "KR": "KOR", "LT": "LTU", "LU": "LUX", "LV": "LVA",
    "MX": "MEX", "MY": "MYS", "NG": "NGA", "NL": "NLD", "NO": "NOR",
    "NZ": "NZL", "PE": "PER", "PH": "PHL", "PL": "POL", "PT": "PRT",
    "RO": "ROU", "RS": "SRB", "RU": "RUS", "SA": "SAU", "SE": "SWE",
    "SG": "SGP", "SI": "SVN", "SK": "SVK", "TH": "THA", "TR": "TUR",
    "TW": "TWN", "UA": "UKR", "US": "USA", "VN": "VNM", "ZA": "ZAF",
}
