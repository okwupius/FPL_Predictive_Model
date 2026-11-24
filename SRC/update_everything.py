import subprocess
import time
import webbrowser

print("\n" + "=" * 70)
print("⚽ FPL PLATFORM UPDATE")
print("=" * 70)

steps = [

    ("Download FPL Data",
     "src/fpl_download.py"),

    ("Download Fixtures",
     "src/download_fixtures.py"),

    ("Build Next Fixtures",
     "src/next_fixture_lookup.py"),

    ("Build Fixture Runs",
     "src/build_fixture_run_table.py"),

    ("Build Forecast V11",
     "src/build_forecast_v11.py"),

    ("Generate Predictions",
     "src/fpl_predict_v11.py"),

    ("Generate Rankings",
     "src/fpl_rankings_v11.py"),

    ("Save Snapshot",
     "src/save_snapshot.py")
]

successful = 0
failed = []

for step_name, script in steps:

    print("\n" + "-" * 70)
    print(f"RUNNING: {step_name}")
    print("-" * 70)

    try:

        result = subprocess.run(
            ["python", script],
            capture_output=True,
            text=True,
            check=True
        )

        successful += 1

        print("✅ SUCCESS")

        if result.stdout:
            print(result.stdout[:500])

    except subprocess.CalledProcessError as e:

        failed.append(
            (step_name, script)
        )

        print("❌ FAILED")

        if e.stderr:
            print(e.stderr)

    time.sleep(1)

# =================================================
# SUMMARY
# =================================================

print("\n" + "=" * 70)
print("UPDATE SUMMARY")
print("=" * 70)

print(
    f"\nSuccessful Steps: "
    f"{successful}/{len(steps)}"
)

if len(failed) == 0:

    print("\n✅ UPDATE COMPLETE")

    print("\n🚀 Launching Dashboard...")

    subprocess.Popen(
        [
            "python",
            "-m",
            "streamlit",
            "run",
            "Dashboards/app.py"
        ]
    )

    time.sleep(5)

    webbrowser.open(
        "http://localhost:8501"
    )

else:

    print("\n⚠ Some steps failed:")

    for item in failed:

        print(
            f"\n- {item[0]}"
        )

        print(
            f"  {item[1]}"
        )

print("\n" + "=" * 70)