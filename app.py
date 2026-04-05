# from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
# import pandas as pd
# import os
# import smtplib
# import mysql.connector
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import numpy as np

# app = Flask(__name__)
# app.secret_key = "ecovision_secret_key"

# # ---------------------------------------------------
# # MYSQL DATABASE CONFIG
# # ---------------------------------------------------
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "Santhi@73966",
#     "database": "userverification"
# }

# def get_db_connection():
#     return mysql.connector.connect(**DB_CONFIG)

# # ---------------------------------------------------
# # EMAIL CONFIG
# # ---------------------------------------------------
# SENDER_EMAIL = "forestsurveyindia@gmail.com"
# SENDER_APP_PASSWORD = ""
# RECEIVER_EMAILS = [
#        "forestsurveyindia@gmail.com"
# ]

# # ---------------------------------------------------
# # DATASET LOAD
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATASET_PATH = os.path.join(BASE_DIR, "dataset", "final_cleaned_dataset122.csv")

# print("Checking dataset path:", DATASET_PATH)

# try:
#     if os.path.exists(DATASET_PATH):
#         df = pd.read_csv(DATASET_PATH)
#         df.columns = df.columns.str.strip().str.lower()

#         if "state_name" in df.columns:
#             df["state_name"] = df["state_name"].astype(str).str.strip()

#         print("Dataset loaded successfully")
#         print("Columns:", df.columns.tolist())
#         print("Total rows:", len(df))
#     else:
#         print("Dataset file not found:", DATASET_PATH)
#         df = pd.DataFrame()
# except Exception as e:
#     print("Dataset loading error:", e)
#     df = pd.DataFrame()

# # ---------------------------------------------------
# # STATE IMAGE MAP
# # ---------------------------------------------------
# STATE_IMAGE_MAP = {
#     "Andhra Pradesh": "AP1.jpg",
#     "Arunachal Pradesh": "Arunachal Pradesh.jpg",
#     "Assam": "Assam.jpg",
#     "Bihar": "Bihar.jpg",
#     "Chhattisgarh": "Chhattisgarh.jpg",
#     "Goa": "Goa.jpg",
#     "Gujarat": "Gujarat.jpg",
#     "Haryana": "Haryana.jpg",
#     "Himachal Pradesh": "Himachal Pradesh.jpg",
#     "Jharkhand": "Jharkhand.jpg",
#     "Karnataka": "Karnataka.jpg",
#     "Kerala": "Kerala.jpg",
#     "Madhya Pradesh": "Madhya Pradesh.jpg",
#     "Maharashtra": "Maharashtra.jpg",
#     "Manipur": "Manipur.jpg",
#     "Meghalaya": "Meghalaya.jpg",
#     "Mizoram": "Mizoram.jpg",
#     "Nagaland": "Nagaland.jpg",
#     "Odisha": "Odisha.jpg",
#     "Punjab": "Punjab.jpg",
#     "Rajasthan": "Rajasthan.jpg",
#     "Sikkim": "Sikkim.jpg",
#     "Tamil Nadu": "Tamil Nadu.jpg",
#     "Telangana": "Telangana.jpg",
#     "Tripura": "Tripura.jpg",
#     "Uttar Pradesh": "Uttar Pradesh.jpg",
#     "Uttarakhand": "Uttarakhand.jpg",
#     "West Bengal": "West Bengal.jpg"
# }

# # ---------------------------------------------------
# # HELPERS
# # ---------------------------------------------------
# def get_col(row, possible_names, default="N/A"):
#     for name in possible_names:
#         if name in row.index:
#             value = row[name]
#             if pd.isna(value):
#                 return default
#             return value
#     return default


# def find_matching_column(columns, keywords):
#     for col in columns:
#         col_clean = str(col).strip().lower()
#         for keyword in keywords:
#             if keyword in col_clean:
#                 return col
#     return None


# def get_co2_value(row):
#     co2 = get_col(
#         row,
#         [
#             "co2_emissions",
#             "co2",
#             "carbon_emissions",
#             "co2 emission",
#             "co2_emission",
#             "co2_emission_tons",
#             "carbon_emission",
#             "co₂_emissions",
#             "co2 levels",
#             "co2_level"
#         ],
#         None
#     )

#     if co2 is not None and not pd.isna(co2):
#         return co2

#     co2_col = find_matching_column(row.index, ["co2", "carbon"])
#     if co2_col and not pd.isna(row[co2_col]):
#         return row[co2_col]

#     return "N/A"


# def normalize_state_name_for_url(state_name):
#     return str(state_name).strip().lower().replace(" ", "-")


# def normalize_state_name_for_match(state_name):
#     return str(state_name).strip().lower().replace("-", " ")


# def to_json_safe(value):
#     if pd.isna(value):
#         return "N/A"

#     if isinstance(value, (np.integer,)):
#         return int(value)

#     if isinstance(value, (np.floating,)):
#         return float(value)

#     if isinstance(value, (np.bool_,)):
#         return bool(value)

#     return value


# def format_decimal_or_na(value, decimals=2):
#     if value == "N/A" or value is None:
#         return "N/A"

#     if isinstance(value, (int, float, np.integer, np.floating)):
#         return round(float(value), decimals)

#     try:
#         return round(float(value), decimals)
#     except Exception:
#         return value


# def get_state_image_filename(state_name):
#     clean_name = str(state_name).strip().title()

#     if clean_name in STATE_IMAGE_MAP:
#         return STATE_IMAGE_MAP[clean_name]

#     candidate = f"{clean_name}.jpg"
#     image_path = os.path.join(BASE_DIR, "static", "images", candidate)

#     if os.path.exists(image_path):
#         return candidate

#     return "logo.jpg"


# def get_alert_details(aqi, forest_cover):
#     try:
#         aqi_num = float(aqi)
#     except Exception:
#         aqi_num = None

#     try:
#         forest_num = float(forest_cover)
#     except Exception:
#         forest_num = None

#     title = "Safe Environmental Status"
#     severity = "safe"
#     message = "Environmental indicators are within manageable range."
#     action = "Continue monitoring and maintain current environmental practices."
#     needs_email = False

#     if aqi_num is not None and forest_num is not None:
#         if aqi_num > 200 and forest_num < 15:
#             title = "Environmental Risk Alert"
#             severity = "combined"
#             message = "High pollution levels and low forest cover detected."
#             action = "Immediate environmental action, plantation programs, and emission control measures are strongly recommended."
#             needs_email = True
#         elif aqi_num > 200:
#             title = "High Pollution Alert"
#             severity = "critical"
#             message = "Air quality has crossed the safe limit."
#             action = "Reduce vehicle emissions, control industrial pollution, and improve air monitoring."
#             needs_email = True
#         elif forest_num < 15:
#             title = "Forest Improvement Alert"
#             severity = "forest"
#             message = "Forest cover is below the recommended level."
#             action = "Increase tree plantation and develop green zones."
#             needs_email = True
#     elif aqi_num is not None and aqi_num > 200:
#         title = "High Pollution Alert"
#         severity = "critical"
#         message = "Air quality has crossed the safe limit."
#         action = "Reduce vehicle and industrial pollution immediately."
#         needs_email = True

#     return {
#         "title": title,
#         "severity": severity,
#         "message": message,
#         "action": action,
#         "needs_email": needs_email
#     }


# def build_alert_email_message(state_name, year, aqi, forest_cover, co2, risk_score, alert_name, status_message, action_message):
#     return f"""
# EcoVision India - Environmental Alert Notification

# State: {state_name}
# Year: {year}
# AQI: {aqi}
# Forest Cover %: {forest_cover}
# CO2 Emissions: {co2}
# Risk Score: {risk_score}

# Alert Type: {alert_name}

# Status:
# {status_message}

# Recommended Action:
# {action_message}

# This alert was generated automatically by the EcoVision India Environmental Analytics Platform.

# Regards,
# EcoVision India
# """.strip()


# # ---------------------------------------------------
# # EMAIL FUNCTION
# # ---------------------------------------------------
# def send_email(subject, message):
#     if not SENDER_EMAIL or not SENDER_APP_PASSWORD:
#         print("Email configuration missing.")
#         return False, "Email configuration is missing."

#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)

#         msg = MIMEMultipart()
#         msg["From"] = SENDER_EMAIL
#         msg["To"] = ", ".join(RECEIVER_EMAILS)
#         msg["Subject"] = subject
#         msg.attach(MIMEText(message, "plain"))

#         server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
#         server.quit()

#         print("Email sent successfully")
#         return True, "Email sent successfully."

#     except Exception as e:
#         print("Email Error:", e)
#         return False, str(e)


# # ---------------------------------------------------
# # SUMMARY COUNTS
# # ---------------------------------------------------
# def get_alert_summary():
#     summary = {
#         "critical": 0,
#         "warning": 0,
#         "safe": 0
#     }

#     if df.empty or "state_name" not in df.columns:
#         return summary

#     temp_df = df.copy()
#     temp_df["state_name"] = temp_df["state_name"].astype(str).str.strip()

#     if "year" in temp_df.columns:
#         temp_df = temp_df.sort_values("year").groupby("state_name", as_index=False).tail(1)
#     else:
#         temp_df = temp_df.drop_duplicates(subset=["state_name"], keep="last")

#     for _, row in temp_df.iterrows():
#         aqi = get_col(row, ["aqi", "air_quality_index"], "N/A")
#         forest_cover = get_col(
#             row,
#             ["forest_cover", "forest_cover_percentage", "forest_cover_%"],
#             "N/A"
#         )

#         alert = get_alert_details(aqi, forest_cover)

#         if alert["severity"] in ["critical", "combined", "forest"]:
#             if alert["severity"] == "forest":
#                 summary["warning"] += 1
#             else:
#                 summary["critical"] += 1
#         else:
#             summary["safe"] += 1

#     return summary


# # ---------------------------------------------------
# # ROUTES
# # ---------------------------------------------------
# @app.route("/")
# def home():
#     return render_template("home.html")


# # ---------------------------------------------------
# # LOGIN
# # ---------------------------------------------------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email", "").strip().lower()
#         password = request.form.get("password", "").strip()

#         if not email or not password:
#             flash("Please enter both email and password.", "error")
#             return redirect(url_for("login"))

#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)

#             cursor.execute(
#                 "SELECT * FROM users WHERE email = %s AND password = %s",
#                 (email, password)
#             )
#             user = cursor.fetchone()

#             cursor.close()
#             conn.close()

#             if not user:
#                 flash("Invalid email or password.", "error")
#                 return redirect(url_for("login"))

#             flash("Login successful!", "success")
#             return redirect(url_for("states"))

#         except Exception as e:
#             print("Login DB Error:", e)
#             flash("Database connection error. Please check MySQL settings.", "error")
#             return redirect(url_for("login"))

#     return render_template("user_login.html")


# # ---------------------------------------------------
# # SIGNUP
# # ---------------------------------------------------
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         name = request.form.get("name", "").strip()
#         email = request.form.get("email", "").strip().lower()
#         password = request.form.get("password", "").strip()
#         confirm_password = request.form.get("confirm_password", "").strip()

#         if not name or not email or not password or not confirm_password:
#             flash("Please fill all fields.", "error")
#             return redirect(url_for("signup"))

#         if password != confirm_password:
#             flash("Passwords do not match.", "error")
#             return redirect(url_for("signup"))

#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)

#             cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#             existing_user = cursor.fetchone()

#             if existing_user:
#                 cursor.close()
#                 conn.close()
#                 flash("Account already exists. Please login.", "error")
#                 return redirect(url_for("signup"))

#             cursor.execute(
#                 "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
#                 (name, email, password)
#             )
#             conn.commit()

#             cursor.close()
#             conn.close()

#             flash("Signup successful! Please login.", "success")
#             return redirect(url_for("login"))

#         except Exception as e:
#             print("Signup DB Error:", e)
#             flash("Database connection error. Please check MySQL settings.", "error")
#             return redirect(url_for("signup"))

#     return render_template("signup.html")


# # ---------------------------------------------------
# # DASHBOARDS
# # ---------------------------------------------------
# @app.route("/pollution-dashboard")
# def pollution_dashboard():
#     state_name = request.args.get("state_name")
#     return render_template("pollution_dashboard.html", state_name=state_name)


# @app.route("/forest-dashboard")
# def forest_dashboard():
#     state_name = request.args.get("state_name")
#     return render_template("forest_dashboard.html", state_name=state_name)


# @app.route("/environmental-dashboard")
# def environmental_dashboard():
#     state_name = request.args.get("state_name")
#     return render_template("environmental_dashboard.html", state_name=state_name)


# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")


# @app.route("/dashboard-details")
# def dashboard_details():
#     return render_template("Dashboard_deatls.html")


# # ---------------------------------------------------
# # STATES OVERVIEW
# # ---------------------------------------------------
# @app.route("/states")
# def states():
#     states_list = []
#     state_cards = []

#     if not df.empty and "state_name" in df.columns:
#         states_list = sorted(
#             df["state_name"].dropna().astype(str).str.strip().unique().tolist()
#         )

#         for state_name in states_list:
#             clean_name = str(state_name).strip().title()
#             state_cards.append({
#                 "name": clean_name,
#                 "url_name": normalize_state_name_for_url(clean_name),
#                 "image": f"/static/images/{get_state_image_filename(clean_name)}"
#             })

#     return render_template(
#         "state_overview.html",
#         states=states_list,
#         state_cards=state_cards
#     )


# # ---------------------------------------------------
# # STATE DETAILS
# # ---------------------------------------------------
# @app.route("/state/<state_name>")
# def state_details(state_name):
#     if df.empty or "state_name" not in df.columns:
#         return render_template("state_details.html", state=None)

#     matched_name = normalize_state_name_for_match(state_name)

#     temp_df = df.copy()
#     temp_df["state_name"] = temp_df["state_name"].astype(str).str.strip().str.lower()
#     matched_rows = temp_df[temp_df["state_name"] == matched_name]

#     if matched_rows.empty:
#         return render_template("state_details.html", state=None)

#     if "year" in matched_rows.columns:
#         row = matched_rows.sort_values(by="year", ascending=False).iloc[0]
#     else:
#         row = matched_rows.iloc[0]

#     real_state_name = str(get_col(row, ["state_name"], "N/A")).title()

#     state = {
#         "state_name": real_state_name,
#         "image_file": get_state_image_filename(real_state_name),
#         "latest_year": to_json_safe(get_col(row, ["year", "latest_year"], "N/A")),
#         "forest_cover_percentage": to_json_safe(
#             get_col(row, ["forest_cover_percentage", "forest_cover_%", "forest_cover"], "N/A")
#         ),
#         "air_quality_index": to_json_safe(
#             get_col(row, ["air_quality_index", "aqi"], "N/A")
#         ),
#         "environmental_risk_score": to_json_safe(
#             get_col(row, ["environmental_risk_score", "risk_score"], "N/A")
#         ),
#         "region_category": str(get_col(row, ["region_category"], "N/A")),
#         "population": to_json_safe(get_col(row, ["population"], "N/A")),
#         "forest_category": str(get_col(row, ["forest_category"], "N/A")),
#         "pollution_level": str(get_col(row, ["pollution_level"], "N/A")),
#         "industrial_index": to_json_safe(get_col(row, ["industrial_index"], "N/A")),
#         "population_density": to_json_safe(get_col(row, ["population_density"], "N/A")),
#         "required_forest_increase_sqkm": to_json_safe(
#             get_col(row, ["required_forest_increase_sqkm"], "N/A")
#         ),
#         "paragraph_1": f"{real_state_name} shows important environmental indicators such as forest cover, AQI, and ecological risk levels based on the latest available dataset.",
#         "paragraph_2": "This page provides a professional state-level overview to support environmental monitoring, comparison, and decision-making."
#     }

#     return render_template("state_details.html", state=state)


# # ---------------------------------------------------
# # ALERTS PAGE
# # ---------------------------------------------------
# @app.route("/alerts")
# def alerts():
#     states_list = []

#     if not df.empty and "state_name" in df.columns:
#         states_list = sorted(
#             df["state_name"].dropna().astype(str).str.strip().unique().tolist()
#         )

#     summary = get_alert_summary()

#     return render_template("alerts.html", states=states_list, summary=summary)


# # ---------------------------------------------------
# # API: CHECK ALERT
# # ---------------------------------------------------
# @app.route("/api/check-alert", methods=["GET"])
# def check_alert():
#     try:
#         state_name = request.args.get("state_name", "").strip()

#         if not state_name:
#             return jsonify({
#                 "success": False,
#                 "severity": "neutral",
#                 "title": "No State Entered",
#                 "message": "Please enter a state name."
#             }), 200

#         if df.empty:
#             return jsonify({
#                 "success": False,
#                 "severity": "neutral",
#                 "title": "Dataset Error",
#                 "message": "Dataset not loaded."
#             }), 200

#         if "state_name" not in df.columns:
#             return jsonify({
#                 "success": False,
#                 "severity": "neutral",
#                 "title": "Dataset Error",
#                 "message": "state_name column not found in dataset."
#             }), 200

#         temp_df = df.copy()
#         temp_df["state_name"] = temp_df["state_name"].astype(str).str.strip()

#         state_rows = temp_df[temp_df["state_name"].str.lower() == state_name.lower()]

#         if state_rows.empty:
#             return jsonify({
#                 "success": False,
#                 "severity": "neutral",
#                 "title": "State Not Found",
#                 "message": f"No data found for {state_name}.",
#                 "state_name": state_name
#             }), 200

#         if "year" in state_rows.columns:
#             row = state_rows.sort_values(by="year", ascending=False).iloc[0]
#         else:
#             row = state_rows.iloc[0]

#         aqi = get_col(row, ["aqi", "air_quality_index"], "N/A")
#         forest_cover = get_col(
#             row,
#             ["forest_cover", "forest_cover_percentage", "forest_cover_%"],
#             "N/A"
#         )
#         co2 = get_co2_value(row)
#         risk_score = get_col(row, ["environmental_risk_score", "risk_score"], "N/A")
#         year = get_col(row, ["year"], "N/A")
#         real_state_name = get_col(row, ["state_name"], state_name)

#         alert = get_alert_details(aqi, forest_cover)

#         return jsonify({
#             "success": True,
#             "severity": alert["severity"],
#             "title": alert["title"],
#             "state_name": str(real_state_name).title(),
#             "year": to_json_safe(year),
#             "aqi": format_decimal_or_na(aqi, 2),
#             "forest_cover": format_decimal_or_na(forest_cover, 2),
#             "co2": format_decimal_or_na(co2, 2),
#             "risk_score": format_decimal_or_na(risk_score, 2),
#             "message": str(alert["message"]),
#             "action": str(alert["action"]),
#             "needs_email": alert["needs_email"]
#         }), 200

#     except Exception as e:
#         print("API Error in /api/check-alert:", e)
#         return jsonify({
#             "success": False,
#             "severity": "neutral",
#             "title": "Server Error",
#             "message": f"Something went wrong: {str(e)}"
#         }), 500


# # ---------------------------------------------------
# # API: SEND ALERT EMAIL
# # ---------------------------------------------------
# @app.route("/send-alert-email", methods=["POST"])
# def send_alert_email():
#     try:
#         data = request.get_json()

#         state_name = data.get("state_name", "Unknown State")
#         year = data.get("year", "N/A")
#         aqi = data.get("aqi", "N/A")
#         forest_cover = data.get("forest_cover", "N/A")
#         co2 = data.get("co2", "N/A")
#         risk_score = data.get("risk_score", "N/A")
#         alert_name = data.get("alert_name", "Environmental Alert")
#         status_message = data.get("message", "Environmental status detected.")
#         action_message = data.get("action", "Please review the environmental condition.")

#         if alert_name == "Safe Environmental Status":
#             return jsonify({
#                 "status": "info",
#                 "message": "No email required for safe environmental status."
#             }), 200

#         subject = f"{alert_name} - {state_name}"
#         email_message = build_alert_email_message(
#             state_name=state_name,
#             year=year,
#             aqi=aqi,
#             forest_cover=forest_cover,
#             co2=co2,
#             risk_score=risk_score,
#             alert_name=alert_name,
#             status_message=status_message,
#             action_message=action_message
#         )

#         success, response_message = send_email(subject, email_message)

#         if success:
#             return jsonify({
#                 "status": "success",
#                 "message": "Email sent successfully."
#             }), 200
#         else:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Failed to send email: {response_message}"
#             }), 500

#     except Exception as e:
#         print("Route Error:", e)
#         return jsonify({
#             "status": "error",
#             "message": "Something went wrong while sending email."
#         }), 500


# # ---------------------------------------------------
# # RUN
# # ---------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pandas as pd
import os
import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy as np

app = Flask(__name__)
app.secret_key = "ecovision_secret_key"

# ---------------------------------------------------
# MYSQL DATABASE CONFIG
# ---------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Santhi@73966",   # <-- update this
    "database": "userverification"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------------------------------------------
# EMAIL CONFIG
# ---------------------------------------------------
SENDER_EMAIL = "forestsurveyindia@gmail.com"
SENDER_APP_PASSWORD ="ascwbjpjdymskpkh"   # <-- new Gmail App Password here
RECEIVER_EMAILS = [
    "forestsurveyindia@gmail.com"
]

# ---------------------------------------------------
# DATASET LOAD
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "final_cleaned_dataset122.csv")

print("Checking dataset path:", DATASET_PATH)

try:
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        df.columns = df.columns.str.strip().str.lower()

        if "state_name" in df.columns:
            df["state_name"] = df["state_name"].astype(str).str.strip()

        print("Dataset loaded successfully")
        print("Columns:", df.columns.tolist())
        print("Total rows:", len(df))
    else:
        print("Dataset file not found:", DATASET_PATH)
        df = pd.DataFrame()
except Exception as e:
    print("Dataset loading error:", e)
    df = pd.DataFrame()

# ---------------------------------------------------
# STATE IMAGE MAP
# ---------------------------------------------------
STATE_IMAGE_MAP = {
    "Andhra Pradesh": "AP1.jpg",
    "Arunachal Pradesh": "Arunachal Pradesh.jpg",
    "Assam": "Assam.jpg",
    "Bihar": "Bihar.jpg",
    "Chhattisgarh": "Chhattisgarh.jpg",
    "Goa": "Goa.jpg",
    "Gujarat": "Gujarat.jpg",
    "Haryana": "Haryana.jpg",
    "Himachal Pradesh": "Himachal Pradesh.jpg",
    "Jharkhand": "Jharkhand.jpg",
    "Karnataka": "Karnataka.jpg",
    "Kerala": "Kerala.jpg",
    "Madhya Pradesh": "Madhya Pradesh.jpg",
    "Maharashtra": "Maharashtra.jpg",
    "Manipur": "Manipur.jpg",
    "Meghalaya": "Meghalaya.jpg",
    "Mizoram": "Mizoram.jpg",
    "Nagaland": "Nagaland.jpg",
    "Odisha": "Odisha.jpg",
    "Punjab": "Punjab.jpg",
    "Rajasthan": "Rajasthan.jpg",
    "Sikkim": "Sikkim.jpg",
    "Tamil Nadu": "Tamil Nadu.jpg",
    "Telangana": "Telangana.jpg",
    "Tripura": "Tripura.jpg",
    "Uttar Pradesh": "Uttar Pradesh.jpg",
    "Uttarakhand": "Uttarakhand.jpg",
    "West Bengal": "West Bengal.jpg"
}

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def get_col(row, possible_names, default="N/A"):
    for name in possible_names:
        if name in row.index:
            value = row[name]
            if pd.isna(value):
                return default
            return value
    return default


def find_matching_column(columns, keywords):
    for col in columns:
        col_clean = str(col).strip().lower()
        for keyword in keywords:
            if keyword in col_clean:
                return col
    return None


def get_co2_value(row):
    co2 = get_col(
        row,
        [
            "co2_emissions",
            "co2",
            "carbon_emissions",
            "co2 emission",
            "co2_emission",
            "co2_emission_tons",
            "carbon_emission",
            "co₂_emissions",
            "co2 levels",
            "co2_level"
        ],
        None
    )

    if co2 is not None and not pd.isna(co2):
        return co2

    co2_col = find_matching_column(row.index, ["co2", "carbon"])
    if co2_col and not pd.isna(row[co2_col]):
        return row[co2_col]

    return "N/A"


def normalize_state_name_for_url(state_name):
    return str(state_name).strip().lower().replace(" ", "-")


def normalize_state_name_for_match(state_name):
    return str(state_name).strip().lower().replace("-", " ")


def to_json_safe(value):
    if pd.isna(value):
        return "N/A"

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        return float(value)

    if isinstance(value, (np.bool_,)):
        return bool(value)

    return value


def format_decimal_or_na(value, decimals=2):
    if value == "N/A" or value is None:
        return "N/A"

    if isinstance(value, (int, float, np.integer, np.floating)):
        return round(float(value), decimals)

    try:
        return round(float(value), decimals)
    except Exception:
        return value


def format_number_for_email(value):
    if value == "N/A" or value is None:
        return "N/A"
    try:
        return f"{float(value):,.2f}"
    except Exception:
        return str(value)


def get_state_image_filename(state_name):
    clean_name = str(state_name).strip().title()

    if clean_name in STATE_IMAGE_MAP:
        return STATE_IMAGE_MAP[clean_name]

    candidate = f"{clean_name}.jpg"
    image_path = os.path.join(BASE_DIR, "static", "images", candidate)

    if os.path.exists(image_path):
        return candidate

    return "logo.jpg"


# ---------------------------------------------------
# ALERT ENGINE
# ---------------------------------------------------
def get_alerts_for_values(row):
    """
    Returns ALL matching alerts using full row data.

    Updated logic:
    - High Pollution Alert => AQI > 200
    - Forest Improvement Alert => Forest Cover < 60
    - Environmental Risk Alert => AQI > 200 and Forest Cover < 60

    Forest increase recommendation should NOT be shown
    for states where forest cover is already high (>= 60).
    """
    alerts = []

    aqi = get_col(row, ["aqi", "air_quality_index"], "N/A")
    forest_cover = get_col(
        row,
        ["forest_cover", "forest_cover_percentage", "forest_cover_%"],
        "N/A"
    )
    required_forest = get_col(row, ["required_forest_increase_sqkm"], "N/A")

    try:
        aqi_num = float(aqi)
    except Exception:
        aqi_num = None

    try:
        forest_num = float(forest_cover)
    except Exception:
        forest_num = None

    required_forest_text = format_number_for_email(required_forest)

    # 1) High Pollution Alert
    if aqi_num is not None and aqi_num > 200:
        if forest_num is not None and forest_num < 60:
            high_pollution_action = (
                f"Reduce vehicle emissions, control industrial pollution, improve air monitoring, "
                f"and increase forest area by approximately {required_forest_text} sq.km through "
                f"tree plantation and green zone development."
            )
        else:
            high_pollution_action = (
                "Reduce vehicle emissions, control industrial pollution, and improve air monitoring."
            )

        alerts.append({
            "title": "High Pollution Alert",
            "severity": "critical",
            "message": "Air quality has crossed the safe limit.",
            "action": high_pollution_action,
            "needs_email": True
        })

    # 2) Forest Improvement Alert
    if forest_num is not None and forest_num < 60:
        alerts.append({
            "title": "Forest Improvement Alert",
            "severity": "forest",
            "message": "Forest cover is below the recommended level.",
            "action": (
                f"Increase forest area by approximately {required_forest_text} sq.km, "
                f"restore degraded forest areas, and develop green zones."
            ),
            "needs_email": True
        })

    # 3) Environmental Risk Alert
    if aqi_num is not None and forest_num is not None and aqi_num > 200 and forest_num < 60:
        alerts.append({
            "title": "Environmental Risk Alert",
            "severity": "combined",
            "message": "High pollution levels and low forest cover detected.",
            "action": (
                f"Immediate environmental action is required: control emissions, strengthen monitoring, "
                f"and increase forest area by approximately {required_forest_text} sq.km through "
                f"plantation and ecological restoration."
            ),
            "needs_email": True
        })

    # Safe status if no alerts
    if not alerts:
        alerts.append({
            "title": "Safe Environmental Status",
            "severity": "safe",
            "message": "Environmental indicators are within manageable range.",
            "action": "Continue monitoring and maintain current environmental practices.",
            "needs_email": False
        })

    return alerts


def get_primary_alert(alerts):
    """
    Used for showing main card in UI.
    Priority:
    combined > critical > forest > safe
    """
    priority_order = ["combined", "critical", "forest", "safe"]

    for severity in priority_order:
        for alert in alerts:
            if alert["severity"] == severity:
                return alert

    return alerts[0]


def build_combined_alert_email_message(state_name, year, aqi, forest_cover, co2, risk_score, alerts):
    alert_titles = "\n".join([f"{i+1}. {alert['title']}" for i, alert in enumerate(alerts)])

    status_block = "\n\n".join(
        [f"{i+1}. {alert['title']}\nStatus: {alert['message']}\nRecommended Action: {alert['action']}"
         for i, alert in enumerate(alerts)]
    )

    return f"""
EcoVision India - Environmental Alert Notification

State: {state_name}
Year: {year}
AQI: {format_number_for_email(aqi)}
Forest Cover %: {format_number_for_email(forest_cover)}
CO2 Emissions: {format_number_for_email(co2)}
Risk Score: {format_number_for_email(risk_score)}

Triggered Alerts:
{alert_titles}

Alert Details:
{status_block}

This alert was generated automatically by the EcoVision India Environmental Analytics Platform.

Regards,
EcoVision India
""".strip()


def get_latest_state_row(state_name):
    """
    Finds latest row for given state.
    """
    if df.empty or "state_name" not in df.columns:
        return None

    temp_df = df.copy()
    temp_df["state_name"] = temp_df["state_name"].astype(str).str.strip()

    state_rows = temp_df[temp_df["state_name"].str.lower() == str(state_name).strip().lower()]

    if state_rows.empty:
        return None

    if "year" in state_rows.columns:
        state_rows = state_rows.sort_values(by="year", ascending=False)

    return state_rows.iloc[0]


# ---------------------------------------------------
# EMAIL FUNCTION
# ---------------------------------------------------
def send_email(subject, message):
    if not SENDER_EMAIL or not SENDER_APP_PASSWORD:
        print("Email configuration missing.")
        return False, "Email configuration is missing."

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(RECEIVER_EMAILS)
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
        server.quit()

        print("Email sent successfully")
        return True, "Email sent successfully."

    except Exception as e:
        print("Email Error:", e)
        return False, str(e)


# ---------------------------------------------------
# SUMMARY COUNTS
# ---------------------------------------------------
def get_alert_summary():
    summary = {
        "critical": 0,
        "warning": 0,
        "safe": 0
    }

    if df.empty or "state_name" not in df.columns:
        return summary

    temp_df = df.copy()
    temp_df["state_name"] = temp_df["state_name"].astype(str).str.strip()

    if "year" in temp_df.columns:
        temp_df = temp_df.sort_values("year").groupby("state_name", as_index=False).tail(1)
    else:
        temp_df = temp_df.drop_duplicates(subset=["state_name"], keep="last")

    for _, row in temp_df.iterrows():
        alerts = get_alerts_for_values(row)

        if any(a["severity"] in ["critical", "combined"] for a in alerts):
            summary["critical"] += 1
        elif any(a["severity"] == "forest" for a in alerts):
            summary["warning"] += 1
        else:
            summary["safe"] += 1

    return summary


# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return redirect(url_for("login"))

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password)
            )
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if not user:
                flash("Invalid email or password.", "error")
                return redirect(url_for("login"))

            flash("Login successful!", "success")
            return redirect(url_for("states"))

        except Exception as e:
            print("Login DB Error:", e)
            flash("Database connection error. Please check MySQL settings.", "error")
            return redirect(url_for("login"))

    return render_template("user_login.html")


# ---------------------------------------------------
# SIGNUP
# ---------------------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not name or not email or not password or not confirm_password:
            flash("Please fill all fields.", "error")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("signup"))

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                conn.close()
                flash("Account already exists. Please login.", "error")
                return redirect(url_for("signup"))

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()

            cursor.close()
            conn.close()

            flash("Signup successful! Please login.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            print("Signup DB Error:", e)
            flash("Database connection error. Please check MySQL settings.", "error")
            return redirect(url_for("signup"))

    return render_template("signup.html")


# ---------------------------------------------------
# DASHBOARDS
# ---------------------------------------------------
@app.route("/pollution-dashboard")
def pollution_dashboard():
    state_name = request.args.get("state_name")
    return render_template("pollution_dashboard.html", state_name=state_name)


@app.route("/forest-dashboard")
def forest_dashboard():
    state_name = request.args.get("state_name")
    return render_template("forest_dashboard.html", state_name=state_name)


@app.route("/environmental-dashboard")
def environmental_dashboard():
    state_name = request.args.get("state_name")
    return render_template("environmental_dashboard.html", state_name=state_name)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard-details")
def dashboard_details():
    return render_template("Dashboard_deatls.html")


# ---------------------------------------------------
# STATES OVERVIEW
# ---------------------------------------------------
@app.route("/states")
def states():
    states_list = []
    state_cards = []

    if not df.empty and "state_name" in df.columns:
        states_list = sorted(
            df["state_name"].dropna().astype(str).str.strip().unique().tolist()
        )

        for state_name in states_list:
            clean_name = str(state_name).strip().title()
            state_cards.append({
                "name": clean_name,
                "url_name": normalize_state_name_for_url(clean_name),
                "image": f"/static/images/{get_state_image_filename(clean_name)}"
            })

    return render_template(
        "state_overview.html",
        states=states_list,
        state_cards=state_cards
    )


# ---------------------------------------------------
# STATE DETAILS
# ---------------------------------------------------
@app.route("/state/<state_name>")
def state_details(state_name):
    if df.empty or "state_name" not in df.columns:
        return render_template("state_details.html", state=None)

    matched_name = normalize_state_name_for_match(state_name)

    temp_df = df.copy()
    temp_df["state_name"] = temp_df["state_name"].astype(str).str.strip().str.lower()
    matched_rows = temp_df[temp_df["state_name"] == matched_name]

    if matched_rows.empty:
        return render_template("state_details.html", state=None)

    if "year" in matched_rows.columns:
        row = matched_rows.sort_values(by="year", ascending=False).iloc[0]
    else:
        row = matched_rows.iloc[0]

    real_state_name = str(get_col(row, ["state_name"], "N/A")).title()

    state = {
        "state_name": real_state_name,
        "image_file": get_state_image_filename(real_state_name),
        "latest_year": to_json_safe(get_col(row, ["year", "latest_year"], "N/A")),
        "forest_cover_percentage": to_json_safe(
            get_col(row, ["forest_cover_percentage", "forest_cover_%", "forest_cover"], "N/A")
        ),
        "air_quality_index": to_json_safe(
            get_col(row, ["air_quality_index", "aqi"], "N/A")
        ),
        "environmental_risk_score": to_json_safe(
            get_col(row, ["environmental_risk_score", "risk_score"], "N/A")
        ),
        "region_category": str(get_col(row, ["region_category"], "N/A")),
        "population": to_json_safe(get_col(row, ["population"], "N/A")),
        "forest_category": str(get_col(row, ["forest_category"], "N/A")),
        "pollution_level": str(get_col(row, ["pollution_level"], "N/A")),
        "industrial_index": to_json_safe(get_col(row, ["industrial_index"], "N/A")),
        "population_density": to_json_safe(get_col(row, ["population_density"], "N/A")),
        "required_forest_increase_sqkm": to_json_safe(
            get_col(row, ["required_forest_increase_sqkm"], "N/A")
        ),
        "paragraph_1": f"{real_state_name} shows important environmental indicators such as forest cover, AQI, and ecological risk levels based on the latest available dataset.",
        "paragraph_2": "This page provides a professional state-level overview to support environmental monitoring, comparison, and decision-making."
    }

    return render_template("state_details.html", state=state)


# ---------------------------------------------------
# ALERTS PAGE
# ---------------------------------------------------
@app.route("/alerts")
def alerts():
    states_list = []

    if not df.empty and "state_name" in df.columns:
        states_list = sorted(
            df["state_name"].dropna().astype(str).str.strip().unique().tolist()
        )

    summary = get_alert_summary()

    return render_template("alerts.html", states=states_list, summary=summary)


# ---------------------------------------------------
# API: CHECK ALERT
# ---------------------------------------------------
@app.route("/api/check-alert", methods=["GET"])
def check_alert():
    try:
        state_name = request.args.get("state_name", "").strip()

        if not state_name:
            return jsonify({
                "success": False,
                "severity": "neutral",
                "title": "No State Entered",
                "message": "Please enter a state name."
            }), 200

        if df.empty:
            return jsonify({
                "success": False,
                "severity": "neutral",
                "title": "Dataset Error",
                "message": "Dataset not loaded."
            }), 200

        if "state_name" not in df.columns:
            return jsonify({
                "success": False,
                "severity": "neutral",
                "title": "Dataset Error",
                "message": "state_name column not found in dataset."
            }), 200

        row = get_latest_state_row(state_name)

        if row is None:
            return jsonify({
                "success": False,
                "severity": "neutral",
                "title": "State Not Found",
                "message": f"No data found for {state_name}.",
                "state_name": state_name
            }), 200

        aqi = get_col(row, ["aqi", "air_quality_index"], "N/A")
        forest_cover = get_col(
            row,
            ["forest_cover", "forest_cover_percentage", "forest_cover_%"],
            "N/A"
        )
        co2 = get_co2_value(row)
        risk_score = get_col(row, ["environmental_risk_score", "risk_score"], "N/A")
        year = get_col(row, ["year"], "N/A")
        real_state_name = get_col(row, ["state_name"], state_name)

        alerts = get_alerts_for_values(row)
        primary_alert = get_primary_alert(alerts)

        return jsonify({
            "success": True,
            "severity": primary_alert["severity"],
            "title": primary_alert["title"],
            "state_name": str(real_state_name).title(),
            "year": to_json_safe(year),
            "aqi": format_decimal_or_na(aqi, 2),
            "forest_cover": format_decimal_or_na(forest_cover, 2),
            "co2": format_decimal_or_na(co2, 2),
            "risk_score": format_decimal_or_na(risk_score, 2),
            "message": str(primary_alert["message"]),
            "action": str(primary_alert["action"]),
            "needs_email": any(alert["needs_email"] for alert in alerts),
            "all_alerts": [
                {
                    "title": alert["title"],
                    "severity": alert["severity"],
                    "message": alert["message"],
                    "action": alert["action"],
                    "needs_email": alert["needs_email"]
                }
                for alert in alerts
            ]
        }), 200

    except Exception as e:
        print("API Error in /api/check-alert:", e)
        return jsonify({
            "success": False,
            "severity": "neutral",
            "title": "Server Error",
            "message": f"Something went wrong: {str(e)}"
        }), 500


# ---------------------------------------------------
# API: SEND ALERT EMAIL
# ---------------------------------------------------
@app.route("/send-alert-email", methods=["POST"])
def send_alert_email():
    try:
        data = request.get_json() or {}
        state_name = data.get("state_name", "").strip()

        if not state_name:
            return jsonify({
                "status": "error",
                "message": "State name is required."
            }), 400

        row = get_latest_state_row(state_name)

        if row is None:
            return jsonify({
                "status": "error",
                "message": f"No data found for state: {state_name}"
            }), 404

        real_state_name = str(get_col(row, ["state_name"], state_name)).title()
        year = get_col(row, ["year"], "N/A")
        aqi = get_col(row, ["aqi", "air_quality_index"], "N/A")
        forest_cover = get_col(
            row,
            ["forest_cover", "forest_cover_percentage", "forest_cover_%"],
            "N/A"
        )
        co2 = get_co2_value(row)
        risk_score = get_col(row, ["environmental_risk_score", "risk_score"], "N/A")

        alerts = get_alerts_for_values(row)
        email_alerts = [alert for alert in alerts if alert["needs_email"]]

        if not email_alerts:
            return jsonify({
                "status": "info",
                "message": "No alert email required for safe environmental status."
            }), 200

        subject = f"Environmental Alerts - {real_state_name}"

        email_message = build_combined_alert_email_message(
            state_name=real_state_name,
            year=year,
            aqi=aqi,
            forest_cover=forest_cover,
            co2=co2,
            risk_score=risk_score,
            alerts=email_alerts
        )

        success, response_message = send_email(subject, email_message)

        if success:
            return jsonify({
                "status": "success",
                "message": f"Email sent successfully with {len(email_alerts)} alert(s).",
                "alerts_sent": [alert["title"] for alert in email_alerts]
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Failed to send email: {response_message}"
            }), 500

    except Exception as e:
        print("Route Error:", e)
        return jsonify({
            "status": "error",
            "message": f"Something went wrong while sending email: {str(e)}"
        }), 500


# ---------------------------------------------------
# RUN
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)