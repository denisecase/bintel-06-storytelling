"""app_case.py - example application entry point.

This module provides the standard entry point.

The application main() coordinates reusable functions
from project modules.

This application can import and call reusable functions
from the complete BI pipeline:

raw data
    ↓
prepared data
    ↓
data warehouse
    ↓
reporting and OLAP
    ↓
storytelling

This example currently calls only the
storytelling functions.

Author: Denise Case
Date: 2026-07

Terminal command to run this file from the root project folder:

uv run python -m bizintel.app_case

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it with your alias, and modify your copy.
  If you do, include your command to run it in the docstring above and in README.md.
"""

# === Section 1. Import dependencies and set up constants ===

# === DECLARE IMPORTS (bring in free code from elsewhere) ===

from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import matplotlib.pyplot as plt

# Import reusable functions.
# Additional reusable functions can be imported
# from earlier modules.
from bizintel.storytelling_case import (
    identify_key_results,
    load_reporting_data,
    select_top_category,
    summarize_category_sales,
    summarize_monthly_sales,
)
from bizintel.utils_logger import LOG, log_header
from bizintel.utils_viz import plot_bar, plot_line

# === DECLARE GLOBAL CONSTANTS AND CONFIGURATION ===

# Path to the DuckDB data warehouse created earlier in the BI pipeline.
DW_FILE: Final[Path] = Path("artifacts/smart_sales.duckdb")

# Folder for reporting-ready data.
DATA_REPORTING: Final[Path] = Path("data/reporting")

# Reporting-ready CSV file created by the earlier reporting workflow.
REPORTING_FILE: Final[Path] = DATA_REPORTING / "sales_reporting_case.csv"

# Folder for charts used in the project documentation.
CHARTS_OUTPUT: Final[Path] = Path("docs/images")

# Chart files shown in docs/index.md.
CATEGORY_CHART_FILE: Final[Path] = (
    CHARTS_OUTPUT / "storytelling_category_sales_case.png"
)
MONTHLY_CHART_FILE: Final[Path] = CHARTS_OUTPUT / "storytelling_monthly_sales_case.png"

# The selected region defines the focus of this example story.
# Change this value in your copied file to investigate another region.
SELECTED_REGION: Final[str] = "East"


# === DEFINE THE MAIN FUNCTION (WHERE THE MAGIC HAPPENS) ===


def main() -> None:
    """Main function to run the BI application workflow.

    This is where the application calls reusable functions
    in the order required by the workflow.
    """

    # First, log the header for the BI module to indicate the start of the workflow.
    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "Data warehouse:", DW_FILE)
    log_path(LOG, "Reporting data:", REPORTING_FILE)

    # This app can coordinate the complete BI pipeline.
    # For now, this app just reuses the Module 6 functions.

    # STORYTELLING STEP 1: DEFINE ONE CLEAR BUSINESS QUESTION.
    #
    # Which product category contributes the most sales in the East region,
    # and when are its sales strongest?
    #
    # The functions below gather only the evidence needed
    # to answer this question.

    LOG.info("CALL a function to load reporting-ready data........")
    df_reporting = load_reporting_data(REPORTING_FILE)

    # STORYTELLING STEP 2: GATHER THE DATA FOR THE FIRST CHART.
    # Compare categories inside the selected region.
    LOG.info("CALL a function to summarize sales by category........")
    df_category_sales = summarize_category_sales(
        df_reporting,
        SELECTED_REGION,
    )

    # STORYTELLING STEP 3: USE THE FIRST RESULT TO GUIDE THE NEXT ANALYSIS.
    # Select the leading category instead of choosing an unrelated
    # category before seeing the first result.
    LOG.info("CALL a function to select the leading category........")
    top_category = select_top_category(df_category_sales)

    # STORYTELLING STEP 4: GATHER THE DATA FOR THE SECOND CHART.
    # Examine the monthly pattern for the leading category.
    LOG.info("CALL a function to summarize monthly sales........")
    df_monthly_sales = summarize_monthly_sales(
        df_reporting,
        SELECTED_REGION,
        top_category,
    )

    # STORYTELLING STEP 5: CREATE AND SAVE THE CONNECTED CHARTS.
    CHARTS_OUTPUT.mkdir(parents=True, exist_ok=True)

    LOG.info("CALL a function to plot category sales........")
    plot_bar(
        df=df_category_sales,
        x="Category",
        y="TotalSales",
        title=f"Sales by Category in {SELECTED_REGION}",
        xlabel="Product Category",
        ylabel="Total Sales ($)",
        palette="Blues_d",
    )
    plt.savefig(CATEGORY_CHART_FILE, bbox_inches="tight")
    log_path(LOG, "Saved category chart:", CATEGORY_CHART_FILE)

    LOG.info("CALL a function to plot monthly sales........")
    plot_line(
        df=df_monthly_sales,
        x="YearMonth",
        y="TotalSales",
        title=f"Monthly {top_category} Sales in {SELECTED_REGION}",
        xlabel="Month",
        ylabel="Total Sales ($)",
    )
    plt.savefig(MONTHLY_CHART_FILE, bbox_inches="tight")
    log_path(LOG, "Saved monthly chart:", MONTHLY_CHART_FILE)

    # STORYTELLING STEP 6: IDENTIFY THE KEY FACTUAL RESULTS.
    # The log verifies the values found in the data.
    # The complete story belongs in docs/index.md with both charts.
    LOG.info("CALL a function to identify key results........")
    identify_key_results(
        df_category_sales,
        df_monthly_sales,
        SELECTED_REGION,
    )

    LOG.info("CALL a function to show charts........")
    plt.show()

    LOG.info("App workflow complete")
    LOG.info("CLOSE chart windows to continue.")
    LOG.info("Terminate this process with CTRL+c as needed.")
    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    # This conditional ensures that the main() function is only executed
    # when this script is run directly, not when it is imported as a module.
    main()
