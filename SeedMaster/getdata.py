import requests

# URLS
SKIDOR_URL = "https://live.skidor.com/GetResultlist/6695/56016?Ipos=999&Count=50&From=0&Level=1&Gender=N"


def get_eqtiming_ids(start_date, end_date, printdata=False):
    """
    Searches for races within a specific date range. Format: YYYY-MM-DD
    """
    # Base URL
    url = "https://live.eqtiming.com/api/Events"

    # Parameters
    params = {
        "dateFrom": start_date,
        "dateTo": end_date,
        "organizationId": 371,
        "dateSort": "true",
        "onlyValidated": "false",
    }

    print(f"Searching for races from {start_date} to {end_date}...\n")

    response = requests.get(url, params=params)

    if response.status_code != 200:
        # If error
        print(f"Error: {response.status_code}\n")
        race_dict = dict()
        print(" - Empty dictionary created. - ")

    else:
        races = response.json()

        if printdata is True:
            # Header
            print(
                f"{'Race-ID':<8} {'Org-ID':<8} {'Sport-ID':<8} {'Country':<10} {'Date':<12} {'Race Name'}"
            )
            print("-" * 90)
            for race in races:
                # Get data
                rid = race.get("Id")  # RaceID
                name = race.get("Name")  # Race Name
                date = race.get("Date", "N/A")[:10]  # Race Date
                org_data = race.get("Organization", {})  # Race Type
                org_id = org_data.get("Id", "N/A")
                country = org_data.get("Country", {}).get("Name", "N/A")
                sport_data = race.get("Sport", {})
                sport_id = sport_data.get("Id", "N/A")

                # Print each race
                print(
                    f"{rid:<8} {org_id:<8} {sport_id:<8} {country:<10} {date:<12} {name}"
                )
            print("")

        # Create new dictionary
        race_dict = {}
        for race in races:
            rid = race.get("Id")
            raw_name = race.get("Name", "").strip()
            year = race.get("Date", "N/A")[:4]
            date = race.get("Date", "N/A")[:10]

            # If the year is NOT already in the name, add it
            if year != "N/A" and year not in raw_name:
                clean_name = f"{raw_name} {year}"
            else:
                clean_name = raw_name

            race_dict[rid] = {"name": clean_name, "date": date, "year": year}

        num_races = len(race_dict)
        print(f" - Dictionary created with {num_races} unique Race IDs. - \n")

        # Header
        print(f"{'Race-ID':<8} {'Date':<12} {'Race Name'}")
        print("-" * 45)
        # Loop over dict.
        for rid in race_dict:
            name = race_dict[rid]["name"]
            date = race_dict[rid]["date"]
            print(f"{rid:<8} {date:<12} {name}")

        # Return
        return race_dict


def get_eqtiming_results(race_dict, race_list=None):
    if race_list is None:


if __name__ == "__main__":
    eq_races = get_eqtiming_ids("2024-12-01", "2026-12-01", printdata=False)
