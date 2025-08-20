import numpy as np

def values_are_different(val1, val2):
    """Safely check if two values differ, even if they're numpy arrays or different types."""
    try:
        if isinstance(val1, np.ndarray) or isinstance(val2, np.ndarray):
            return not np.array_equal(val1, val2)
        return val1 != val2
    except Exception:
        return True  # Treat as different if comparison fails

def write_semi_custom_planet_module(
    output_path,
    planet_name,
    base_planet,
    semi_custom_planet,
    custom_name=None
):
    # Fixed order of sections (matching original modules)
    ordered_sections = [
        "Bulk",
        "Steps",
        "Ocean",
        "Sil",
        "Do",
        "Core",
        "Seismic",
        "Magnetic"
    ]

    # Section header labels
    section_headers = {
        "Bulk": "Bulk planetary settings",
        "Steps": "Layer step settings",
        "Ocean": "Hydrosphere assumptions/settings",
        "Sil": "Silicate Mantle",
        "Do": "Mantle equation of state model / dynamic options",
        "Core": "Core assumptions",
        "Seismic": "Seismic properties of solids",
        "Magnetic": "Magnetic induction",
    }

    with open(output_path, "w") as f:
        # Header and imports
        f.write(f'"""\nPPSemiCustom{custom_name or planet_name}\n')
        f.write("Auto-generated semi-custom planet module for PlanetProfile.\n")
        f.write("Includes all default values and user-modified settings.\n")
        f.write('"""\n\n')
        f.write("import numpy as np\n")
        f.write("from PlanetProfile.Utilities.defineStructs import PlanetStruct, Constants\n\n")
        f.write(f"Planet = PlanetStruct('{planet_name}')\n\n")

        written_sections = set()

        # Write all sections in defined order
        for section in ordered_sections:
            custom_struct = getattr(semi_custom_planet, section, None)
            base_struct = getattr(base_planet, section, None)

            if custom_struct and hasattr(custom_struct, "__dict__") and vars(custom_struct):
                written_sections.add(section)

                f.write(f'\n"""{section_headers[section]}"""\n')

                for attr_name, new_val in vars(custom_struct).items():
                    old_val = getattr(base_struct, attr_name, None)
                    is_changed = values_are_different(new_val, old_val)

                    value_str = f"'{new_val}'" if isinstance(new_val, str) else repr(new_val)
                    comment = "  # this setting has been changed from the default" if is_changed else ""
                    f.write(f"Planet.{section}.{attr_name} = {value_str}{comment}\n")

        # Catch any remaining sections not listed above
        for category_name in dir(semi_custom_planet):
            if category_name.startswith("_") or category_name in written_sections:
                continue

            custom_struct = getattr(semi_custom_planet, category_name)
            base_struct = getattr(base_planet, category_name, None)

            if hasattr(custom_struct, "__dict__") and vars(custom_struct):
                f.write(f'\n""" {category_name} settings """\n')

                for attr_name, new_val in vars(custom_struct).items():
                    old_val = getattr(base_struct, attr_name, None)
                    is_changed = values_are_different(new_val, old_val)

                    value_str = f"'{new_val}'" if isinstance(new_val, str) else repr(new_val)
                    comment = "  # this setting has been changed from the default" if is_changed else ""
                    f.write(f"Planet.{category_name}.{attr_name} = {value_str}{comment}\n")

        f.write("\n# End of auto-generated module\n")
