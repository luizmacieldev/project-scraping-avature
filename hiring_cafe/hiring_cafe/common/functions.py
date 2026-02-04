import yaml
from pathlib import Path

def normalize_key(label: str):
    """
    Convert job field labels to standardized keys.
    
    Args:
        label: Raw label text (e.g., "Work Location", "Posted Date")
    
    Returns:
        Standardized key or None if no match found.
    """
    label = label.lower().strip()
    mappings = {
        "work location": "work_location",
        "location": "work_location",
        "posted date": "posted_date",
        "business area": "business_area",
        "duration": "duration",
    }
    for k, v in mappings.items():
        if k in label:
            return v
    return None


def load_avature_sites():
    """
    Load Avature site configurations from a YAML file.

    This function reads the `avature_sites.yaml` configuration file and returns
    the list of Avature career sites to be scraped.

    Expected YAML structure:
        avature_sites:
          - name: <site_name>
            base_url: <career_search_url>

    Returns:
        list[dict]: A list of dictionaries containing Avature site configurations.
                    Each dictionary must include:
                        - name (str): Identifier for the site
                        - base_url (str): Base URL for job search pages
    """

    # Resolve the absolute path to the config/avature_sites.yaml file
    config_path = Path(__file__).resolve().parent.parent / "config" / "avature_sites.yaml"

    # Load and parse the YAML configuration file safely
    with open(config_path, "r") as f:
        return yaml.safe_load(f)["avature_sites"]
