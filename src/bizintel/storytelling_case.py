"""storytelling_case.py - example.

An example of telling a story with data.

It is the final module for presenting a complete end-to-end BI workflow.

An overall BI project often flows like this:

prepared data
    ↓
data warehouse
    ↓
reporting-ready dataset from the dw
    ↓
analysis and OLAP (slice, dice, roll-up, drill-down)
    ↓
insight
    ↓
story and recommended action <--- this is our final addition

Author: Denise Case
Date: 2026-08

Storytelling process:

1. Define one clear business question.
2. Use the reporting-ready CSV created earlier.
3. Gather only the data needed to answer the question.
4. Create connected charts.
5. Identify the key results supported by the charts.
6. Write the story and recommendation in docs/index.md.

Business Question:
- Which product category contributes the most sales in the East region,
  and when are its sales strongest?

Data Source:
- data/reporting/sales_reporting_case.csv

Output:
- docs/images/storytelling_category_sales_case.png
- docs/images/storytelling_monthly_sales_case.png

Terminal command to run this file from the root project folder:

uv run python -m bizintel.storytelling_case

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it with your alias, and modify your copy.
  If you do, include your command to run it in the docstring above and in README.md.
"""

# === Section 1. Import dependencies and set up constants ===

# === IMPORTS ===

from numbers import Real
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import matplotlib.pyplot as plt
import pandas as pd

from bizintel.utils_logger import LOG, log_header
from bizintel.utils_viz import plot_bar, plot_line

# === DECLARE CONSTANTS ===

# Storytelling input folder.
DATA_REPORTING: Final[Path] = Path("data/reporting")

# Storytelling input file (created earlier).
REPORTING_FILE: Final[Path] = DATA_REPORTING / "sales_reporting_case.csv"

# Storytelling charts output folder so they can appear in our narrative.
CHARTS_OUTPUT: Final[Path] = Path("docs/images")

# Chart files shown in docs/index.md.
STORYTELLING_CHART_FILE_1: Final[Path] = (
    CHARTS_OUTPUT / "storytelling_category_sales_case.png"
)
STORYTELLING_CHART_FILE_2: Final[Path] = (
    CHARTS_OUTPUT / "storytelling_monthly_sales_case.png"
)

# The selected region defines the focus of this example story.
# Your category and selection will depend on the question you have selected.
SELECTED_REGION: Final[str] = "East"


# === Section 2. Define Reusable Functions ===

# === Section 2.1 DEFINE A LOAD REPORTING DATA FUNCTION ===


def load_reporting_data(file_path: Path) -> pd.DataFrame:
    """Load and verify the reporting-ready data.

    WHY: Storytelling begins with trusted, reporting-ready data.
    The earlier modules created this file from the data warehouse.
    We do not repeat the preparation, warehouse, or ETL work here.

    Args:
        file_path: Path to the reporting-ready CSV file.

    Returns:
        Reporting-ready pandas DataFrame.
    """
    LOG.info("Loading reporting-ready data")

    if not file_path.exists():
        raise FileNotFoundError(
            f"Reporting-ready data file not found: {file_path}. "
            "Run the earlier workflow first."
        )

    df_reporting: pd.DataFrame = pd.read_csv(file_path)

    # Define the set of columns
    # required for this analysis.
    required_columns: set[str] = {
        "YearMonth",  # categorical dimension
        "Region",  # categorical dimension
        "Category",  # categorical dimension
        "SaleAmount",  # numeric measure
    }

    # COLUMN QUALITY CHECKS.
    # The required columns minus the actual columns
    # in the DataFrame gives us any missing columns.
    missing_columns: set[str] = required_columns - set(df_reporting.columns)

    # If any of the columns we need
    # for this analysis are missing, raise an error,
    # and show provide a sorted list of the missing columns.
    if missing_columns:
        raise ValueError(
            f"Reporting data is missing required columns: {sorted(missing_columns)}"
        )

    # If the DataFrame is empty, raise an error.
    if df_reporting.empty:
        raise ValueError("The reporting data contains no rows.")

    # NUMERIC COLUMN QUALITY CHECKS.
    # Do this for all numeric columns that are required for the analysis.
    # Our only numeric column for this analysis is `SaleAmount`.
    # The column SHOULD be numeric, but for safety,
    # we check and convert it to numeric if needed
    # so it can be summarized reliably.
    # Use the built-in pandas function to_numeric() and pass in
    # our dataframe's numeric column, and
    # set the errors parameter to "coerce"
    # so that any non-numeric values are converted to NaN.

    df_reporting["SaleAmount"] = pd.to_numeric(
        df_reporting["SaleAmount"],
        errors="coerce",
    )

    # DATA QUALITY CHECK.
    # If any of the values in the SaleAmount column are NaN,
    # raise an error to indicate that the data is not clean.
    # Start with our df numeric column,
    # then call the isna() method to check for NaN values,
    # and then call the any() method
    # to check if any of the values are True (that is, are Not-a-Number).
    # if so, raise a ValueError with a message
    # indicating that the numeric column contains missing or non-numeric values.
    if df_reporting["SaleAmount"].isna().any():
        raise ValueError("SaleAmount contains missing or nonnumeric values.")

    # GOOD PRACTICE.
    # Log critical information about the reporting data for verification.
    # Every df has a built in .shape attribute
    # that returns a tuple of (rows, columns).
    # Use index [0] for the first value (rows)
    # and index [1] for the second value (columns).
    LOG.info(f"  Loaded {df_reporting.shape[0]} reporting rows")
    LOG.info(f"  Verified {df_reporting.shape[1]} reporting columns")
    return df_reporting


# === Section 2.2 DEFINE A SUMMARIZE FUNCTION THAT ANSWERS THIS BUSINESS QUESTION ===


def summarize_category_sales(
    df_reporting: pd.DataFrame,
    selected_region: str,
) -> pd.DataFrame:
    """Summarize total sales by category for the selected region.

    WHY: The first chart establishes the important comparison.
    In this case, we want to see which category contributes the most sales.

    Args:
        df_reporting: Complete reporting-ready sales data.
        selected_region: Region to investigate.

    Returns:
        DataFrame with Category and TotalSales columns.
    """
    LOG.info(f"Summarizing category sales for Region = {selected_region!r}")

    # A slice focuses the analysis on one selected Region value.
    # Create a new DataFrame with only the rows for the selected region.
    # Start with the complete reporting DataFrame, then use the .loc[] method
    # to filter the rows where the "Region" column matches the selected region.
    # Call the .copy() method to create a new DataFrame
    # that is independent of the original.
    df_region: pd.DataFrame = df_reporting.loc[
        df_reporting["Region"] == selected_region
    ].copy()

    # If the slice is empty, raise an error to indicate that the selected region
    # we are interested in does not exist in the reporting data.
    # Note: This error message uses an f-string with the
    # !r conversion flag to show the selected region in quotes.
    # You can remove it if you prefer, and/or ask your favorite AI for
    # more information.
    if df_region.empty:
        raise ValueError(
            f"No sales were found for region {selected_region!r}. "
            "Update SELECTED_REGION to a region present in the data."
        )

    # After filtering to the slice we want to study,
    # summarize the data by a meaningful business dimension.
    #
    # General BI pattern:
    # group by a dimension, aggregate a measure, and sort the result.
    #
    # In this example:
    # - Category is the dimension we want to compare.
    # - SaleAmount is the numeric measure we want to summarize.
    #
    # Create a new DataFrame named df_category_sales.
    #
    # Put the right-hand side inside parentheses so Python allows us
    # to write one long expression across several readable lines.
    # Note: These parentheses do not create a tuple because there is no comma.
    #
    # Chain several DataFrame operations together.
    # Each method returns a DataFrame that the next method can use.
    #
    # CHAIN FUNCTION 1. GROUPBY
    # Start with df_region and call the df groupby() method by passing in:
    #   1. "Category" - the dimension used to create the groups.
    #   2. set the named `as_index` parameter to False to keep
    #      Category a regular DataFrame column.
    #
    # CHAIN FUNCTION 2. AGGREGATE (code like the pros!)
    # Next call the df agg() method on the grouped data by passing in a named aggregation.
    # For the named aggregation, we pass in a keyword argument whose value is a tuple.
    # The keyword sets the name of the new result column and is NOT in quotes,
    # it is a Python identifier.
    # The value is a tuple that holds:
    #   1. "SaleAmount" - the numeric column (in quotes) to summarize.
    #   2. "sum" - the aggregation operation (in quotes) to apply to each group.
    #
    # CHAIN FUNCTION 3. SORT (descending)
    # Next, call the df sort_values() method on the aggregated df by passing in:
    #   1. "TotalSales" - the column used to sort the rows.
    #   2. set the named `ascending` parameter to False so the highest come first.

    # IMPORTANT: It is good to know this pattern, but not that useful anymore
    # to be able to write it from scratch.
    # Most analysts have access to both the pandas API and
    # free or low-cost generative AI tools that can
    # help write the code
    # if we can describe the business question and
    # the data we have available.

    # FOCUS ON THE HUMAN LEVEL SKILLS and
    # use tools to help with the implementation.
    df_category_sales: pd.DataFrame = (
        df_region.groupby("Category", as_index=False)
        .agg(TotalSales=("SaleAmount", "sum"))
        .sort_values("TotalSales", ascending=False)
    )

    # MAKE PRESENTABLE.
    # Round the TotalSales column to two decimal places for better readability.
    # How many digits depends on your data.
    df_category_sales["TotalSales"] = df_category_sales["TotalSales"].round(2)

    # FINALLY, log key information before exiting the function.
    # In this case, log the number of categories summarized in the result
    # by calling the built in df method shape
    # and using index [0] to get the number of rows.
    LOG.info(f"  Categories summarized: {df_category_sales.shape[0]}")
    return df_category_sales


# === Section 2.3 DEFINE A SELECT THE TOP CATEGORY FUNCTION ===


def select_top_category(df_category_sales: pd.DataFrame) -> str:
    """For this business problem, we need a function that
    takes a DataFrame of category sales sorted highest to lowest and
    selects the category with the greatest total sales.

    WHY: The second part of the story follows the first result.
    We investigate the leading category rather than creating
    an unrelated second chart.

    Args:
        df_category_sales: Category sales sorted highest to lowest.

    Returns:
        Category with the greatest total sales.
    """

    # SELECT THE TOP CATEGORY.
    # The provided DataFrame is already sorted from highest to lowest,
    # so the first row contains the category with the greatest total sales.
    #
    # Create a new string variable named top_category.
    #
    # Start with the provided df. It has a built in property named iloc
    # short for integer location that lets us select a row by its integer position.
    # Use iloc[0] to select the entire first row in the DataFrame.
    #
    # Next, use ["Category"] to select just the Category value from that row.
    #
    # Then, wrap the result in the built in Python method str()
    # to ensure the selected value is stored as a string.
    top_category: str = str(df_category_sales.iloc[0]["Category"])

    # FINALLY, log key information before exiting the function.
    # In this case, log the selected leading category.
    LOG.info(f"  Selected leading category for deeper analysis: {top_category}")

    # AND RETURN the leading category string to the caller
    return top_category


# === Section 2.4 DEFINE A SUMMARIZE MONTHLY SALES FUNCTION ===


def summarize_monthly_sales(
    df_reporting: pd.DataFrame,
    selected_region: str,
    selected_category: str,
) -> pd.DataFrame:
    """Summarize monthly sales for one region and category.

    WHY: The second chart provides detail behind the first result.
    It shows when the leading category performs most strongly.

    Args:
        df_reporting: Complete reporting-ready sales data.
        selected_region: Region to investigate.
        selected_category: Category selected from the first analysis.

    Returns:
        DataFrame with YearMonth and TotalSales columns.
    """
    LOG.info(f"Summarizing monthly sales for Region = {selected_region!r}")
    LOG.info(f"Summarizing monthly sales for Category = {selected_category!r}")

    # A dice focuses on the selected Region and Category values.
    df_selected: pd.DataFrame = df_reporting.loc[
        (df_reporting["Region"] == selected_region)
        & (df_reporting["Category"] == selected_category)
    ].copy()

    # If the dice is empty,
    # raise an error to indicate that the selected region and category
    # combination does not exist in the reporting data.
    if df_selected.empty:
        raise ValueError("No sales were found for the selected region and category.")

    # Group the selected sales by month to reveal the time pattern.
    # See comments above for more about chaining methods
    # together to group, aggregate, and sort the result.
    df_monthly_sales: pd.DataFrame = (
        df_selected.groupby("YearMonth", as_index=False)
        .agg(TotalSales=("SaleAmount", "sum"))
        .sort_values("YearMonth")
    )

    df_monthly_sales["TotalSales"] = df_monthly_sales["TotalSales"].round(2)

    # FINALLY, log key information before exiting the function.
    # In this case, log the number of months summarized in the result
    # by calling the built in df method shape
    # and using index [0] to get the number of rows.
    LOG.info(f"  Months summarized: {df_monthly_sales.shape[0]}")

    # AND RETURN the monthly sales DataFrame to the caller
    return df_monthly_sales


# === Section 2.5 DEFINE AN IDENTIFY KEY RESULTS FUNCTION ===


def identify_key_results(
    df_category_sales: pd.DataFrame,
    df_monthly_sales: pd.DataFrame,
    selected_region: str,
) -> None:
    """Identify and log the key factual results from the analysis.

    WHY: Results are values directly supported by the data.
    The complete analytical story is not written in the log.
    Students use the results and charts to write their narrative,
    limitation, and recommendation in docs/index.md.

    Args:
        df_category_sales: Total sales by category in the selected region.
        df_monthly_sales: Monthly sales for the selected leading category.
        selected_region: Region represented in the analysis.

    Returns:
        None
    """
    LOG.info("Identifying key results")

    # The category results are sorted from greatest to least total sales.
    top_category: str = str(df_category_sales.iloc[0]["Category"])
    top_category_sales: float = float(df_category_sales.iloc[0]["TotalSales"])

    # Find the month containing the greatest sales value.
    # Call the built-in pandas DataFrame method idxmax() on the TotalSales column
    # to get the index of the row with the maximum value.
    max_index: int = int(df_monthly_sales["TotalSales"].idxmax())

    # GET THE CORRESPONDING YearMonth from the index.
    strongest_month: str = str(df_monthly_sales.loc[max_index, "YearMonth"])

    # GET THE STRONGEST MONTH SALES VALUE from the index.
    # Start with df_monthly_sales and access the df loc property.
    # The loc property provides the pandas label-based indexer.
    #
    # Pass two labels inside the square brackets:
    #   1. max_index - the label of the row we want.
    #   2. "TotalSales" - the label of the column we want.
    #
    # Store the result in a variable before converting it.
    # Use the object type because pandas may return different scalar types.
    strongest_month_sales_value: object = df_monthly_sales.loc[
        max_index,
        "TotalSales",
    ]

    # VALIDATE THE VALUE.
    # First, verify that the selected TotalSales value is not missing.
    if pd.isna(strongest_month_sales_value):
        raise ValueError("The TotalSales value for the strongest month is missing.")
    # Next, verify that the selected value is a real number.
    # Real includes common numeric values such as integers and floating-point numbers.
    # It excludes nonnumeric values and complex numbers.
    if not isinstance(strongest_month_sales_value, Real):
        raise TypeError("The TotalSales value for the strongest month must be numeric.")

    # CONVERT THE VALIDATED VALUE.
    # Call float() only after verifying that the value is a real number.
    strongest_month_sales: float = float(strongest_month_sales_value)

    # FINALLY, Log factual results for verification.
    # Write the explanation and recommendation in docs/index.md.
    # Include the dollar sign where needed
    # and :, with 0.2f to format the float with two decimal places.
    LOG.info(f"  Selected region: {selected_region}")
    LOG.info(f"  Leading category: {top_category}")
    LOG.info(f"  Leading category sales: ${top_category_sales:,.2f}")
    LOG.info(f"  Strongest month: {strongest_month}")
    LOG.info(f"  Strongest month sales: ${strongest_month_sales:,.2f}")


# === MAIN FUNCTION ===


def main() -> None:
    """Main function to run the data storytelling example."""

    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "Input reporting data from:", REPORTING_FILE)

    # STEP 1: DEFINE ONE CLEAR BUSINESS QUESTION.
    #
    # EXAMPLE:
    # Which product category contributes the most sales in the East region,
    # and when are its sales the strongest?
    #
    # The constants and functions below gather only the evidence needed
    # to answer this question.

    LOG.info("CALL a function to load reporting-ready data........")
    df_reporting = load_reporting_data(REPORTING_FILE)

    # STEP 2: GATHER THE DATA FOR THE FIRST CHART.
    # Compare categories inside the selected region.
    LOG.info("CALL a function to summarize sales by category........")
    df_category_sales = summarize_category_sales(
        df_reporting,
        SELECTED_REGION,
    )

    # STEP 3: USE THE FIRST RESULT TO GUIDE THE NEXT ANALYSIS.
    # Select the leading category instead of choosing an unrelated
    # category before seeing the first result.
    LOG.info("CALL a function to select the leading category........")
    top_category = select_top_category(df_category_sales)

    # STEP 4: GATHER THE DATA FOR THE SECOND CHART.
    # Examine the monthly pattern for the leading category.
    LOG.info("CALL a function to summarize monthly sales........")
    df_monthly_sales = summarize_monthly_sales(
        df_reporting,
        SELECTED_REGION,
        top_category,
    )

    # STEP 5: CREATE AND SAVE THE CONNECTED CHARTS.
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
    plt.savefig(STORYTELLING_CHART_FILE_1, bbox_inches="tight")
    log_path(LOG, "Saved category chart:", STORYTELLING_CHART_FILE_1)

    LOG.info("CALL a function to plot monthly sales........")
    plot_line(
        df=df_monthly_sales,
        x="YearMonth",
        y="TotalSales",
        title=f"Monthly {top_category} Sales in {SELECTED_REGION}",
        xlabel="Month",
        ylabel="Total Sales ($)",
    )
    plt.savefig(STORYTELLING_CHART_FILE_2, bbox_inches="tight")
    log_path(LOG, "Saved monthly chart:", STORYTELLING_CHART_FILE_2)

    # STEP 6: IDENTIFY THE KEY FACTUAL RESULTS.
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

    LOG.info("Storytelling workflow complete")
    LOG.info("CLOSE chart windows to continue.")
    LOG.info("Terminate this process with CTRL+c as needed.")
    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
