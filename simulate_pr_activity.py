import random
import subprocess
import requests
import time

REPO_PATH = r"D:\final year\PTest\first"

SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

employees = [f"emp_{i}" for i in range(1,11)]

managers = {
    "manager_1": employees[:5],
    "manager_2": employees[5:]
}

titles = [
"Fix bug",
"Improve logging",
"Refactor service",
"Add validation",
"Optimize query"
]

def run(cmd):
    return subprocess.run(cmd, cwd=REPO_PATH, capture_output=True, text=True)


def send_slack(message):
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK, json=payload)


for day in range(1,11):

    print(f"DAY {day}")

    for manager in managers:

        for emp in managers[manager]:

            prs_today = random.randint(2,3)

            for pr in range(prs_today):

                branch = f"{emp}_day{day}_{pr}"

                run(["git","checkout","main"])
                run(["git","pull"])

                run(["git","checkout","-b",branch])

                with open(f"{REPO_PATH}/worklog.txt","a") as f:
                    f.write(f"{emp} update day {day}\n")

                run(["git","add","."])

                run([
                    "git",
                    "commit",
                    f'--author={emp} <{emp}@company.com>',
                    "-m",
                    random.choice(titles)
                ])

                run(["git","push","origin",branch])

                # CREATE PR AND CAPTURE URL
                result = run([
                    "gh",
                    "pr",
                    "create",
                    "--title",
                    random.choice(titles),
                    "--body",
                    f"PR by {emp}",
                    "--json",
                    "url",
                    "--jq",
                    ".url"
                ])

                pr_url = result.stdout.strip()

                print("PR:", pr_url)

                # SEND TO SLACK
                slack_message = f"""
Daily Update

Employee: {emp}
Manager: {manager}
Day: {day}

PR Created:
{pr_url}
"""

                send_slack(slack_message)

                time.sleep(2)

print("Simulation complete")