#!/usr/bin/env python3
"""
analyze_photo.py - Extract EXIF metadata and infer content from a photo.

Usage: python3 analyze_photo.py <image_path>

Outputs JSON with:
  date            - from EXIF DateTimeOriginal (YYYY-MM-DD)
  camera          - from EXIF Make + Model
  location        - reverse geocoded from GPS (requires geopy)
  suggested_title - inferred by Claude Vision
  suggested_tags  - inferred by Claude Vision
  description     - one-sentence description from Claude Vision

Dependencies:
  pip install Pillow anthropic
  pip install geopy  # optional, for GPS→location
"""

import sys
import json
import os
from datetime import datetime


def extract_exif(image_path):
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS

    result = {}

    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if not exif_data:
            return result

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag == "DateTimeOriginal":
                try:
                    result["date"] = datetime.strptime(value, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    pass

            elif tag == "Make":
                result["_make"] = value.strip()

            elif tag == "Model":
                result["_model"] = value.strip()

            elif tag == "GPSInfo":
                gps_data = {}
                for gps_tag_id, gps_value in value.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_data[gps_tag] = gps_value
                result["_gps"] = gps_data

    # Combine make + model, avoiding duplication (e.g. "Olympus Olympus OM-D")
    make = result.pop("_make", "")
    model = result.pop("_model", "")
    if make and model:
        result["camera"] = model if model.lower().startswith(make.lower()) else f"{make} {model}"
    elif model:
        result["camera"] = model

    return result


def gps_to_decimal(coord, ref):
    """Convert EXIF GPS tuple (degrees, minutes, seconds) + ref to decimal degrees."""
    try:
        d, m, s = coord
        decimal = float(d) + float(m) / 60 + float(s) / 3600
        if ref in ("S", "W"):
            decimal = -decimal
        return decimal
    except Exception:
        return None


def reverse_geocode(gps_data):
    """Return a human-readable location string from GPS EXIF data."""
    try:
        from geopy.geocoders import Nominatim

        lat = gps_to_decimal(gps_data.get("GPSLatitude"), gps_data.get("GPSLatitudeRef", "N"))
        lon = gps_to_decimal(gps_data.get("GPSLongitude"), gps_data.get("GPSLongitudeRef", "E"))

        if lat is None or lon is None:
            return None

        geolocator = Nominatim(user_agent="pieter-photo-analyzer/1.0")
        location = geolocator.reverse(f"{lat}, {lon}", language="en", timeout=10)

        if not location:
            return None

        addr = location.raw.get("address", {})
        # Build "City, Country" or "Country" style string
        parts = []
        for key in ("city", "town", "village", "municipality", "county"):
            if key in addr:
                parts.append(addr[key])
                break
        if "country" in addr:
            parts.append(addr["country"])

        return ", ".join(parts) if parts else location.address.split(",")[-1].strip()

    except ImportError:
        return None  # geopy not installed
    except Exception:
        return None


def analyze_with_claude(image_path):
    """Use Claude Vision to infer title, tags, and description."""
    import anthropic
    import base64

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    ext = os.path.splitext(image_path)[1].lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    media_type = media_types.get(ext, "image/jpeg")

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Analyze this photograph and respond with JSON only (no markdown fences):\n"
                            '{\n'
                            '  "title": "Short descriptive title, 3-6 words, Title Case",\n'
                            '  "tags": ["tag1", "tag2"],\n'
                            '  "description": "One sentence describing the subject and mood."\n'
                            '}\n\n'
                            "For tags choose 2-5 lowercase values. Good tag examples: "
                            "wildlife, landscape, portrait, macro, street, architecture, nature, "
                            "travel, birds, mammals, insects, flowers, water, mountains, urban, "
                            "africa, europe, asia — be specific where helpful (e.g. 'elephant' "
                            "not just 'wildlife')."
                        ),
                    },
                ],
            }
        ],
    )

    text = message.content[0].text.strip()

    # Strip markdown code fences if the model added them anyway
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    return json.loads(text)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 analyze_photo.py <image_path>"}))
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(json.dumps({"error": f"File not found: {image_path}"}))
        sys.exit(1)

    result = {}

    # 1. Extract EXIF data
    try:
        exif = extract_exif(image_path)
        gps_data = exif.pop("_gps", None)
        result.update(exif)
    except ImportError:
        result["warning"] = "Pillow not installed — run: pip install Pillow"
        gps_data = None
    except Exception as e:
        result["exif_error"] = str(e)
        gps_data = None

    # 2. Reverse-geocode GPS → location
    if gps_data:
        location = reverse_geocode(gps_data)
        if location:
            result["location"] = location

    # 3. Claude Vision inference
    try:
        claude = analyze_with_claude(image_path)
        result["suggested_title"] = claude.get("title", "")
        result["suggested_tags"] = claude.get("tags", [])
        result["description"] = claude.get("description", "")
    except ImportError:
        result["claude_error"] = "anthropic not installed — run: pip install anthropic"
    except Exception as e:
        result["claude_error"] = str(e)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
