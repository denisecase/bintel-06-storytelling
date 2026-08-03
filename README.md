# bintel-06-storytelling

[![Workflow Guide](https://img.shields.io/badge/Pro--Guide-pro--analytics--02-green)](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project: BI storytelling with smart sales data.

## Project Description

This project focuses on addressing one specific business goal
end to end and telling a story with data.

We learn to:

- define a clear business question and KPI (key performance indicator)
- use reporting-ready data to answer the business question
- summarize and analyze the relevant data
- create connected charts that support the findings
- identify meaningful business insights
- write a clear, actionable business recommendation
- tell a story with data

## Working Files

You'll work with these areas:

- **data/reporting** - reporting-ready data generated earlier
- **docs/** - project narrative and documentation
- **src/bizintel/** - the app is an example; run only (copy to a new file for your work)
- **pyproject.toml** - update authorship & links
- **zensical.toml** - update authorship & links

## Instructions (pro-analytics-02)

Follow the
[step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**
4. Phase 4. **Modify**
5. Phase 5. **Apply**

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.
When issues occur, share screenshots, error messages, and details about what you tried.
Working through issues is part of implementing professional projects.

## Success

After completing Phase 1. **Start & Run**,
you'll have your own GitHub project,
and running the example module will print out:

```shell
========================
Executed successfully!
========================
```

A new file `project.log` will appear in the root project folder.

## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/username/bintel-06-storytelling

cd bintel-06-storytelling
code .
```

### In a VS Code terminal

These are listed for convenience.
For best results, follow the detailed instructions in
[pro-analytics-02 guide](https://denisecase.github.io/pro-analytics-02/).

```shell
uv self update
uv python pin 3.14
uv lock --upgrade
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
uvx pre-commit autoupdate

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
uvx pre-commit run --all-files

# OPTIONAL: run the example module
uv run python -m bizintel.app_case

# TASK 1: run the example storytelling module for an example problem
uv run python -m bizintel.storytelling_case

# TASK 2: run your own storytelling module that looks at a different problem
# add your command in the line below


# run common chores
uv run ruff format .
uv run ruff check . --fix
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
- You do not need to add to or modify `tests/`. They are provided for example only.
- Many files are silent helpers. Explore as you like, but nothing is required.
- You do NOT need to understand everything; understanding builds naturally over time.

## Troubleshooting >>>

If you see something like this in your terminal: `>>>` or `...`
You accidentally started Python interactive mode.
It happens.
Press `Ctrl+c` (both keys together) or `Ctrl+Z` then `Enter` on Windows.

## Example Output (Remove or replace this Section after You Verify)

```shell
| BI | Loading reporting-ready data
| BI |   Loaded 2392 reporting rows
| BI |   Verified 14 reporting columns
| BI | CALL a function to summarize sales by category........
| BI | Summarizing category sales for Region = 'East'
| BI |   Categories summarized: 4
| BI | CALL a function to select the leading category........
| BI |   Selected leading category for deeper analysis: Office
| BI | CALL a function to summarize monthly sales........
| BI | Summarizing monthly sales for Region = 'East'
| BI | Summarizing monthly sales for Category = 'Office'
| BI |   Months summarized: 12
| BI | CALL a function to plot category sales........
| BI | Creating chart: Sales by Category in East
| BI | Saved category chart: = docs\images\storytelling_category_sales_case.png
| BI | CALL a function to plot monthly sales........
| BI | Creating chart: Monthly Office Sales in East
| BI | Saved monthly chart: = docs\images\storytelling_monthly_sales_case.png
| BI | CALL a function to identify key results........
| BI | Identifying key results
| BI |   Selected region: East
| BI |   Leading category: Office
| BI |   Leading category sales: $456,342.94
| BI |   Strongest month: 2025-05
| BI |   Strongest month sales: $61,229.06
| BI | CALL a function to show charts........
| BI | App workflow complete
| BI | CLOSE chart windows to continue.
| BI | Terminate this process with CTRL+c as needed.
| BI | ========================
| BI | Executed successfully!
| BI | ========================
```

## Findings and Visuals

Take screenshots of your charts and provide them here with a discussion.
In Markdown, display a figure using:
an exclamation mark immediately followed by square brackets containing a useful caption
immediately followed by parentheses containing the relative path to your figure.

In your custom project:

- your figures and narrative should reflect your work
- this `README.md` should include your commands, process, and visuals
- `docs/index.md` should include your narrative

Replace these placeholders with screenshots from your own project run:

![Total Sales by Region](./docs/images/Figure_1.png)

![Total Sales by Product Category](./docs/images/Figure_2.png)

## Project Documentation

Additional project instructions, terms, and notes:

[docs/index.md](docs/index.md)

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)
