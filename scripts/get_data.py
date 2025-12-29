import requests
import pandas as pd
# Q47554 - Toruń
# Q570116 - zabytek historyczny
query = """
SELECT ?item ?itemLabel ?description ?lat ?lon ?image WHERE {
  ?item wdt:P31/wdt:P279* wd:Q570116;
        wdt:P625 ?coord.
  OPTIONAL { ?item wdt:P18 ?image }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "pl,en". }
  
  BIND(geof:latitude(?coord) AS ?lat)
  BIND(geof:longitude(?coord) AS ?lon)
  
  FILTER(?lat > 53.0 && ?lat < 53.1)
  FILTER(?lon > 18.55 && ?lon < 18.65)
}

"""

url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json"

headers = {
    "Accept": "application/sparql+json",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "TorunMap/1.0 (kontakt@example.com)"  # <- OBOWIĄZKOWE
}

response = requests.post(url, headers=headers, params={"query": query}, timeout=60)

print("STATUS:", response.status_code)
print("CONTENT-TYPE:", response.headers.get("Content-Type"))
print("RESPONSE LENGTH:", len(response.text))
print("RESPONSE TEXT (first 500 chars):")
print(response.text[:500])


if response.status_code == 200:
    data = response.json()
    df = pd.json_normalize(data["results"]["bindings"])
    df.to_csv("torun_historical_monuments.csv", index=False)
    print("Data saved to torun_historical_monuments.csv")
else:
    print(f"Error: {response.status_code}")