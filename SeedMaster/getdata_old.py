#!/usr/bin/env python3
"""Fetch and display EQTiming results for Mattias Ottosson."""

import json
import sys
import urllib.request

CONTESTANTS_URL = "https://live.eqtiming.com/api/Contestants/75342"
RESULTS_URL = "https://live.eqtiming.com/api/Result/Total/75342/310587?justTimeData=true&count=10000"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def build_ed_to_contestant(contestants):
    """Map EtappeDeltakerUID -> contestant entry."""
    mapping = {}
    for _cuid, contestant in contestants.items():
        for ed_uid, _etappe in contestant.get("EtappeDeltaker", {}).items():
            mapping[int(ed_uid)] = contestant
    return mapping


def get_ed_uid(contestant):
    """Get the EtappeDeltakerUID for a contestant."""
    for ed_uid in contestant.get("EtappeDeltaker", {}):
        return int(ed_uid)
    return None


def format_row(
    name, time, place_total, place_class, diff_total, diff_class, club=""
):
    """Print a compact single-line result row."""
    club_str = f"  ({club})" if club else ""
    print(f"  {name}{club_str}")
    print(
        f"    {time:>12s}   P{place_total} overall / P{place_class} class \\  +{diff_total} / +{diff_class}"
    )


def display_results(
    winner_c, winner_r, class_winner_c, class_winner_r, mattias_c, mattias_r
):
    klasse = (
        mattias_c.get("Klasse", {}).get("Navn", "")
        if mattias_c.get("Klasse")
        else ""
    )

    print(f"  42 km Tävling — {klasse}")
    print(f"{'=' * 60}")

    rows = [
        ("WINNER", winner_c, winner_r),
    ]
    if class_winner_r is not winner_r:
        rows.append(("CLASS WINNER", class_winner_c, class_winner_r))
    rows.append(("YOU", mattias_c, mattias_r))

    # Header
    print(f"  {'':14s} {'Time':>12s}   {'Place':17s}  {'Diff (total/class)'}")
    print(f"  {'-' * 56}")

    for label, contestant, result in rows:
        utover = contestant.get("Utover", {})
        name = utover.get("NavnFormatert", "Unknown")
        club = utover.get("Klubbnavn", "")
        plassering = result.get("Plassering", {})
        diff = result.get("Diff", {})
        time_str = result.get("Formatert", "-")
        p_total = plassering.get("Total", "-")
        p_class = plassering.get("Klasse", "-")
        d_total = diff.get("TotalFormatert", "-")
        d_class = diff.get("KlasseFormatert", "-")
        splitt = result.get("Splitt", {})
        speed = (
            f"{splitt['Hastighet']:.1f} km/h"
            if splitt.get("Hastighet")
            else ""
        )

        print(
            f"  {label:14s} {time_str:>12s}   P{p_total:<3} / P{p_class:<3} class  +{d_total:>10s} / +{d_class}"
        )
        print(f"  {'':14s} {name} ({club})  {speed}")
        print()


def eq_timing_data():
    print("Fetching data from EQTiming...\n")
    try:
        contestants = fetch_json(CONTESTANTS_URL)
        results_data = fetch_json(RESULTS_URL)
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    ed_map = build_ed_to_contestant(contestants)
    items = results_data.get("Items", [])

    if not items:
        print("No results available yet.")
        sys.exit(0)

    # Find Mattias's contestant entry and his EtappeDeltakerUID
    mattias = contestants.get(str(TARGET_UID))
    if not mattias:
        for _key, c in contestants.items():
            if (
                c.get("Utover", {}).get("NavnFormatert", "").lower()
                == "mattias ottosson"
            ):
                mattias = c
                break

    if not mattias:
        print("Mattias Ottosson not found in contestant list.")
        sys.exit(1)

    mattias_ed_uid = get_ed_uid(mattias)
    mattias_klasse_uid = (
        mattias.get("Klasse", {}).get("UID") if mattias.get("Klasse") else None
    )

    # Find Mattias's result, the overall winner, and the class winner
    mattias_result = None
    overall_winner_result = None
    class_winner_result = None

    for item in items:
        plassering = item.get("Plassering", {})

        if item.get("EtappeDeltakerUID") == mattias_ed_uid:
            mattias_result = item

        if plassering.get("Total") == 1:
            overall_winner_result = item

        if (
            mattias_klasse_uid
            and item.get("KlasseUID") == mattias_klasse_uid
            and plassering.get("Klasse") == 1
        ):
            class_winner_result = item

    # Display compact results
    winner_contestant = (
        ed_map.get(overall_winner_result["EtappeDeltakerUID"])
        if overall_winner_result
        else None
    )
    class_winner_contestant = (
        ed_map.get(class_winner_result["EtappeDeltakerUID"])
        if class_winner_result
        else None
    )

    if mattias_result and winner_contestant and class_winner_contestant:
        display_results(
            winner_contestant,
            overall_winner_result,
            class_winner_contestant,
            class_winner_result,
            mattias,
            mattias_result,
        )
    elif mattias_result:
        print(f"  Time: {mattias_result.get('Formatert', '-')}")
    else:
        print("Mattias Ottosson has no result yet (DNS/not finished).")


def get_skidor_data():
    url = (
        "https://live.skidor.com/GetResultlist/6695/56016"
        "?Ipos=999&Count=50&From=0&Level=1&Gender=N"
    )

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    results = data["ResultList"]

    # Filter to athletes with a finish time (Ipos 999) and status OK
    finishers = [
        r for r in results if r["Status"] == "OK" and "999" in r["Times"]
    ]

    # Sort by finish time rank
    finishers.sort(key=lambda r: r["Times"]["999"]["RankClass"])

    # Show the winner
    winner = finishers[0]
    finish = winner["Times"]["999"]
    print(f"Winner: {winner['FormatedName']}")
    print(f"Club:   {winner['Club']}")
    print(f"Time:   {finish['RunTime']}")

    # Show top 5
    print("\nTop 5:")
    for i, r in enumerate(finishers[:5], 1):
        t = r["Times"]["999"]
        print(
            f"  {i}. {r['FormatedName']:30s} {t['RunTime']}  (+{t['DiffClass']})"
        )


if __name__ == "__main__":
    eq_timing_data()
