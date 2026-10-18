from pathlib import Path


def load_skill(name: str) -> str:
    return Path(f"skills/{name}/SKILL.md").read_text()


def ask_user(question: str) -> str:
    return input(f"{question} ")


def run_skill(name: str) -> None:
    agent.run(f"{load_skill(name)}\n\nRun the skill.")


def check_if(statement: str) -> bool:
    reply = agent.run(f"Only check, change nothing. Is this true: {statement}? Reply true or false.")
    return reply.strip().lower() == "true"


work = ask_user("Is this development or a new skill?")

if work == "skill":
    run_skill("create-skill")
else:
    if not check_if("all dependencies are installed"):
        run_skill("install-dependencies")

    run_skill("update-dependencies")

    run_skill("acceptance-test")

    while requirement := ask_user("What requirement do you want to build?"):
        run_skill("specifying-requirements")

        run_skill("test-driven-development")

        run_skill("write-code")

        if check_if("the new code has a try/except or an edge-case branch"):
            run_skill("error-handling")

        run_skill("refactoring-code")

        run_skill("pre-commit-hooks")

        run_skill("write-commit-message")

    kind = ask_user("Is this an engineering feature or a data feature?")

    if kind == "data":
        run_skill("evaluation")
    else:
        run_skill("acceptance-test")
