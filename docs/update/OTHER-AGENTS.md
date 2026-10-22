# Update Spec-Driven Development - Other Agent Harnesses

Run these commands from your **project root**.

Replace `<harness-name>` with your agent harness's config directory name (e.g., `claude`, `cursor`, `codex`).

```bash
cd .<harness-name>
git pull origin main
cd ..
git add .<harness-name>
git commit -m "chore: update spec-driven-development submodule"
```
