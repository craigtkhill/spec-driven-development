import importlib.util
from pathlib import Path

SKILLS = Path("skills")
WORKFLOW = SKILLS / "spec-test-driven-development" / "workflow.py"
DIAGRAM = Path("workflow.svg")

spec = importlib.util.spec_from_file_location("create_diagram", WORKFLOW.parent / "create_diagram.py")
create_diagram = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_diagram)

diagram = create_diagram.build(WORKFLOW)
in_diagram = {node.label for node in diagram.nodes if not node.diamond and not node.terminal}
existing = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
skills = existing - {WORKFLOW.parent.name}

failed = False
for name in sorted(skills - in_diagram):
    print(f"FAIL {name}: skill is not in the workflow diagram")
    failed = True
for name in sorted(in_diagram - existing):
    print(f"FAIL {name}: workflow calls a skill that does not exist")
    failed = True
if DIAGRAM.read_text() != diagram.svg():
    print(f"FAIL {DIAGRAM}: out of date, run create_diagram.py on {WORKFLOW} {DIAGRAM}")
    failed = True

raise SystemExit(failed)
