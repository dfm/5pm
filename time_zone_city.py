import json

import pycountry
from unidecode import unidecode


zone_map = {
    "America/Caracas": "Caracas, Venezuela",
    "America/La_Paz": "La Paz, Bolivia",
    "Antarctica/DumontDUrville": "Dumont d'Urville Station, Antarctica",
    "Antarctica/Macquarie": "Macquarie Station, Antarctica",
    "Indian/Chagos": "The Chagos Archipelago",
    "Indian/Kerguelen": "The Kerguelen Islands",
}

country_map = {
    "Russian Federation": "Russia",
    "Syrian Arab Republic": "Syria",
    "State of Palestine": "Palestine",
    "Viet Nam": "Vietnam",
    "Democratic People's Republic of Korea": "North Korea",
    "Republic of Korea": "South Korea",
    "Province of China Taiwan": "Taiwan",
    "Islamic Republic of Iran": "Iran",
    "Falkland Islands (Malvinas)": "Falkland Islands",
    "Republic of Moldova": "Moldova",
}


results = []
with open("time-zones.csv", "r") as f:
    for line in f:
        cc, zone = line.strip().split(",")

        # Deal with custom zones
        if zone in zone_map:
            results.append({"zone": zone, "name": zone_map[zone]})
            continue

        # Split the time zone
        parts = zone.replace("_", " ").split("/")

        # Look up the country and format it properly
        country = unidecode(pycountry.countries.get(alpha_2=cc).name)
        country = " ".join(country.split(", ")[::-1])
        country = country_map.get(country, country)

        # Be a little US-centric
        if country == "United States":
            results.append({"zone": zone, "name": ", ".join(parts[1:][::-1]) + ", USA"})
            continue

        # If the zone already refers to a conuntry, don't double count
        query = parts[-1]
        if country.startswith(query):
            name = country
        else:
            name = f"{query}, {country}"
        results.append({"zone": zone, "name": name})


with open("time-zones.json", "w") as f:
    json.dump(results, f, indent=2, sort_keys=True)
