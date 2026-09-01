import iris
from pathlib import Path

# Path to the directory containing pp files
data_dir = Path(
    "/home/users/jonathan.lillis/cylc-run/CMEW/CMEW_cmm_test/share/"
    "data/cdds/cdds_data/GCModelDev/ESMVal/"
    "UKESM1-0-LL_amip-u-dq123_r1i1p1f1/round-1/input/u-dq123/apm/"
)

# Find all pp files in the directory
pp_files = sorted(data_dir.glob("*.pp"))

if not pp_files:
    print(f"No .pp files found in {data_dir}")
else:
    print(f"Found {len(pp_files)} .pp files\n")

    surface_altitude_coords = {}

    for pp_file in pp_files:
        try:
            print(f"Loading: {pp_file.name}")
            cubes = iris.load(str(pp_file))

            for cube in cubes:
                if (
                    cube.name() == "mass_fraction_of_carbon_dioxide_in_air"
                    and cube.coords("surface_altitude")
                ):
                    coord = cube.coord("surface_altitude")
                    surface_altitude_coords[pp_file.name] = {
                        "shape": coord.shape,
                        "dtype": coord.dtype,
                        "units": coord.units,
                        "data_sample": (
                            coord.points[:5]
                            if len(coord.points) > 0
                            else "empty"
                        ),
                    }
                    print(
                        "  ✓ Found surface_altitude for "
                        "mass_fraction_of_carbon_dioxide_in_air: "
                        f"shape={coord.shape}, dtype={coord.dtype}, "
                        f"units={coord.units}"
                    )
                    break
        except Exception as e:
            print(f"  ✗ Error loading {pp_file.name}: {e}")

    # Compare surface_altitude coordinates
    print("\n" + "=" * 80)
    print("COMPARISON OF surface_altitude COORDINATES:")
    print("=" * 80)

    if surface_altitude_coords:
        for filename, coord_info in surface_altitude_coords.items():
            print(f"\n{filename}:")
            for key, value in coord_info.items():
                print(f"  {key}: {value}")
    else:
        print("No surface_altitude coordinates found in any files")
