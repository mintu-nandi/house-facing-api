def get_street_view_image(lat, lon):
    google_api_key = "YOUR_GOOGLE_API_KEY"
    url = f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={lat},{lon}&key={google_api_key}"
    return url  # Returns the image URL
