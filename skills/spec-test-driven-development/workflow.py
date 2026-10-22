from pathlib import Path


def load_skill(name: str) -> str:
    return Path(f"skills/{name}/SKILL.md").read_text()


def ask_user(question: str, aliases: dict[str, str] | None = None) -> str:
    if yolo:
        return agent.run(f"Do not ask the user. From this goal, answer, or reply done when nothing is left: {goal}\n\n{question}")

    reply = input(f"{question} ")
    return (aliases or {}).get(reply, reply)


def run_skill(name: str) -> None:
    agent.run(f"{load_skill(name)}\n\nRun the skill." + (" Do not ask the user. Decide yourself." if yolo else ""))


def check_if(statement: str) -> bool:
    reply = agent.run(f"Only check, change nothing. Is this true: {statement}? Reply true or false.")
    return reply.strip().lower() == "true"


work = ask_user("Is this development or a new skill? (d/s)", {"d": "development", "s": "skill"})

if work == "skill":
    run_skill("create-skill")
else:
    stage = ask_user("Is this a prototype or a full feature? (p/f)", {"p": "prototype", "f": "full"})

    kind = ask_user("Is this an engineering feature or a data feature? (e/d)", {"e": "engineering", "d": "data"})

    commit_type = ask_user("What type of change is this? (feat, fix, perf, refactor, or another type)")

    requirements = []

    while (requirement := ask_user("What do you want to build? Type done when finished.")) != "done":
        requirements.append(requirement)

    if not check_if("all dependencies are installed"):
        run_skill("install-dependencies")

    run_skill("update-dependencies")

    if check_if("any dependencies were updated"):
        run_skill("pre-commit-hooks")

        run_skill("write-commit-message")

    if stage == "prototype":
        run_skill("prototyping")

        run_skill("write-code")
    else:
        if kind == "data":
            run_skill("evaluation")
        else:
            run_skill("acceptance-test")

        for requirement in requirements:
            run_skill("specifying-requirements")

            run_skill("test-driven-development")

            run_skill("write-code")

            if check_if("the new code has a try/except or an edge-case branch"):
                run_skill("error-handling")

            run_skill("refactoring-code")

            run_skill("pre-commit-hooks")

            run_skill("write-commit-message")

        if kind == "data":
            run_skill("evaluation")
        else:
            run_skill("acceptance-test")
