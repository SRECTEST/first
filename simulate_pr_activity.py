import random
import subprocess
import time

REPO_PATH = "D:/final year/PTest/first"

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
    subprocess.run(cmd, cwd=REPO_PATH)

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

                subprocess.run([
                    "gh",
                    "pr",
                    "create",
                    "--title",
                    random.choice(titles),
                    "--body",
                    f"PR by {emp}"
                ], cwd=REPO_PATH)

                time.sleep(1)

print("Simulation complete")