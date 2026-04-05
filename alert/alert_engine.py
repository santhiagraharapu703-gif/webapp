def check_alerts(df):
    alerts = []

    avg_aqi = df["aqi"].mean()
    avg_forest = df["forest_cover_percentage"].mean()

    if avg_aqi > 200:
        alerts.append("🚨 High Pollution Alert")

    if avg_forest < 20:
        alerts.append("🌿 Forest Improvement Needed")

    if avg_aqi > 300 and avg_forest < 15:
        alerts.append("⚠ Environmental Risk Critical")

    return alerts