import requests
import csv
import os
from datetime import datetime
from twilio.rest import Client

# Twilio Credentials

account_sid = "********"
auth_token = "*********"
client = Client(account_sid, auth_token)

# Student preferences

students = [
    {
        "name": "Alwina",
        "number": "whatsapp:+919791242322",
        "skills": ["python", "java", "engineer"]
    }
]

# File paths

csv_file = "matched_jobs.csv"
sent_jobs_file = "sent_jobs.txt"
log_file = "job_log.txt"

# -----------------------------
# Load previously sent job URLs
# -----------------------------
sent_jobs = set()
if os.path.exists(sent_jobs_file):
    with open(sent_jobs_file, "r") as f:
        sent_jobs = set(line.strip() for line in f.readlines())

# -----------------------------
# Fetch jobs
# -----------------------------
url = "https://remoteok.com/api"

try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    jobs = response.json()

    matched_jobs = []

    for job in jobs:
        if isinstance(job, dict):
            title = job.get("position", "")
            company = job.get("company", "N/A")
            location = job.get("location", "Remote")
            link = job.get("url", "")

            if not link or link in sent_jobs:
                continue

            if any(keyword in title.lower() for keyword in ["python", "engineer", "java"]):
                matched_jobs.append({
                    "company": company,
                    "role": title,
                    "location": location,
                    "link": link
                })

            if len(matched_jobs) == 3:
                break

    # -----------------------------
    # Save jobs to CSV
    # -----------------------------
    if matched_jobs:
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["company", "role", "location", "link"])
            writer.writeheader()
            writer.writerows(matched_jobs)

        # -----------------------------
        # Send personalized messages
        # -----------------------------
        for student in students:
            personalized_jobs = []

            for job in matched_jobs:
                if any(skill in job["role"].lower() for skill in student["skills"]):
                    personalized_jobs.append(job)

            if personalized_jobs:
                message = f"Hi {student['name']}! 🚀\n\nHere are your latest job matches:\n\n"

                for idx, job in enumerate(personalized_jobs, start=1):
                    message += (
                        f"{idx}. {job['company']}\n"
                        f"Role: {job['role']}\n"
                        f"Location: {job['location']}\n"
                        f"Link: {job['link']}\n\n"
                    )

                message += f"📅 Alert Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"

                client.messages.create(
                    from_="whatsapp:+14155238886",
                    body=message,
                    to=student["number"]
                )

                print(f"✅ Message sent to {student['name']}")

        # -----------------------------
        # Store sent jobs to avoid duplicates
       
        with open(sent_jobs_file, "a") as f:
            for job in matched_jobs:
                f.write(job["link"] + "\n")

        # -----------------------------
        # Write logs
        # -----------------------------
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now()}] Sent {len(matched_jobs)} jobs successfully\n")

    else:
        print("❌ No new matching jobs found.")

except Exception as e:
    print(f"Error: {e}")
