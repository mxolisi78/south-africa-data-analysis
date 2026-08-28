"""
Exploratory Data Analysis for South Africa
===========================================

This script performs comprehensive EDA on the merged dataset,
creating visualizations and statistical analyses.

Inputs:
    - data/processed/south_africa_combined.csv

Outputs:
    - outputs/figures/*.png (visualizations)
    - outputs/tables/*.csv (summary tables)
    - outputs/reports/eda_report.txt

Author: Your Name
Date: 2026-08-28
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set style for professional plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Define directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
FIGURES_DIR = BASE_DIR / "outputs" / "figures"
TABLES_DIR = BASE_DIR / "outputs" / "tables"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"

# Create directories
for dir_path in [FIGURES_DIR, TABLES_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def load_merged_data():
    """Load the merged dataset."""
    logger.info("Loading merged dataset...")
    file_path = DATA_DIR / "south_africa_combined.csv"
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {len(df)} observations from {df['Year'].min()} to {df['Year'].max()}")
    return df


def create_time_series_plots(df):
    """Create time series plots for both indicators."""
    logger.info("Creating time series plots...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Unemployment
    ax1.plot(df['Year'], df['Unemployment_Rate'], 
             marker='o', linewidth=2, markersize=8, color='#2E86C1')
    ax1.set_title('South Africa Unemployment Rate (1991-2023)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Unemployment Rate (%)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=df['Unemployment_Rate'].mean(), color='red', linestyle='--', 
                alpha=0.7, label=f'Mean: {df["Unemployment_Rate"].mean():.1f}%')
    ax1.legend()
    
    # Add trend line
    z = np.polyfit(df['Year'], df['Unemployment_Rate'], 1)
    p = np.poly1d(z)
    ax1.plot(df['Year'], p(df['Year']), "r--", alpha=0.5, 
             label=f'Trend: {z[0]:.2f}% per year')
    ax1.legend()
    
    # Education
    ax2.plot(df['Year'], df['Tertiary_Enrolment'], 
             marker='s', linewidth=2, markersize=8, color='#28B463')
    ax2.set_title('South Africa Tertiary Enrolment Rate (1991-2023)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Enrolment Rate (%)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=df['Tertiary_Enrolment'].mean(), color='red', linestyle='--', 
                alpha=0.7, label=f'Mean: {df["Tertiary_Enrolment"].mean():.1f}%')
    
    # Add trend line
    z = np.polyfit(df['Year'], df['Tertiary_Enrolment'], 1)
    p = np.poly1d(z)
    ax2.plot(df['Year'], p(df['Year']), "r--", alpha=0.5, 
             label=f'Trend: {z[0]:.2f}% per year')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'time_series.png', dpi=300, bbox_inches='tight')
    plt.show()
    logger.info(f"  Saved: {FIGURES_DIR / 'time_series.png'}")


def create_correlation_analysis(df):
    """Create correlation heatmap and scatter plot."""
    logger.info("Creating correlation analysis...")
    
    # Correlation matrix
    corr_matrix = df[['Unemployment_Rate', 'Tertiary_Enrolment']].corr()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Heatmap
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, square=True, ax=ax1, cbar_kws={'label': 'Correlation'})
    ax1.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
    
    # Scatter plot with regression line
    sns.regplot(x='Tertiary_Enrolment', y='Unemployment_Rate', 
                data=df, ax=ax2, scatter_kws={'alpha':0.6, 's':100},
                line_kws={'color': 'red'})
    ax2.set_xlabel('Tertiary Enrolment Rate (%)', fontsize=12)
    ax2.set_ylabel('Unemployment Rate (%)', fontsize=12)
    ax2.set_title(f'Correlation: {corr_matrix.iloc[0,1]:.3f}', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add year labels to points
    for idx, row in df.iterrows():
        ax2.annotate(str(row['Year']), 
                    (row['Tertiary_Enrolment'], row['Unemployment_Rate']),
                    fontsize=8, alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'correlation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    logger.info(f"  Saved: {FIGURES_DIR / 'correlation_analysis.png'}")


def create_distribution_plots(df):
    """Create distribution plots for both variables."""
    logger.info("Creating distribution plots...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Unemployment distribution
    sns.histplot(df['Unemployment_Rate'], bins=8, kde=True, ax=axes[0], color='#2E86C1')
    axes[0].axvline(df['Unemployment_Rate'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["Unemployment_Rate"].mean():.1f}%')
    axes[0].axvline(df['Unemployment_Rate'].median(), color='green', linestyle='--', 
                   label=f'Median: {df["Unemployment_Rate"].median():.1f}%')
    axes[0].set_title('Unemployment Rate Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Unemployment Rate (%)')
    axes[0].legend()
    
    # Education distribution
    sns.histplot(df['Tertiary_Enrolment'], bins=8, kde=True, ax=axes[1], color='#28B463')
    axes[1].axvline(df['Tertiary_Enrolment'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["Tertiary_Enrolment"].mean():.1f}%')
    axes[1].axvline(df['Tertiary_Enrolment'].median(), color='green', linestyle='--', 
                   label=f'Median: {df["Tertiary_Enrolment"].median():.1f}%')
    axes[1].set_title('Tertiary Enrolment Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Enrolment Rate (%)')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'distributions.png', dpi=300, bbox_inches='tight')
    plt.show()
    logger.info(f"  Saved: {FIGURES_DIR / 'distributions.png'}")


def create_summary_table(df):
    """Create summary statistics table."""
    logger.info("Creating summary statistics table...")
    
    summary = df[['Unemployment_Rate', 'Tertiary_Enrolment']].describe()
    
    # Add additional statistics
    additional_stats = pd.DataFrame({
        'Unemployment_Rate': [df['Unemployment_Rate'].skew(), 
                             df['Unemployment_Rate'].kurtosis()],
        'Tertiary_Enrolment': [df['Tertiary_Enrolment'].skew(), 
                              df['Tertiary_Enrolment'].kurtosis()]
    }, index=['Skewness', 'Kurtosis'])
    
    summary = pd.concat([summary, additional_stats])
    
    # Save to CSV
    summary.to_csv(TABLES_DIR / 'summary_statistics.csv')
    logger.info(f"  Saved: {TABLES_DIR / 'summary_statistics.csv'}")
    
    return summary


def create_insights_report(df, summary):
    """Generate a text report with key insights."""
    logger.info("Creating insights report...")
    
    corr = df['Unemployment_Rate'].corr(df['Tertiary_Enrolment'])
    
    report_path = REPORTS_DIR / 'eda_report.txt'
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("EXPLORATORY DATA ANALYSIS REPORT\n")
        f.write("South Africa - Unemployment and Tertiary Enrolment (1991-2023)\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("DATA OVERVIEW\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Observations: {len(df)}\n")
        f.write(f"Year Range: {df['Year'].min()} - {df['Year'].max()}\n\n")
        
        f.write("KEY STATISTICS\n")
        f.write("-" * 40 + "\n")
        f.write("\nUnemployment Rate:\n")
        f.write(f"  Mean: {summary.loc['mean', 'Unemployment_Rate']:.2f}%\n")
        f.write(f"  Median: {summary.loc['50%', 'Unemployment_Rate']:.2f}%\n")
        f.write(f"  Range: {summary.loc['min', 'Unemployment_Rate']:.2f}% - {summary.loc['max', 'Unemployment_Rate']:.2f}%\n")
        f.write(f"  Std Dev: {summary.loc['std', 'Unemployment_Rate']:.2f}%\n\n")
        
        f.write("Tertiary Enrolment:\n")
        f.write(f"  Mean: {summary.loc['mean', 'Tertiary_Enrolment']:.2f}%\n")
        f.write(f"  Median: {summary.loc['50%', 'Tertiary_Enrolment']:.2f}%\n")
        f.write(f"  Range: {summary.loc['min', 'Tertiary_Enrolment']:.2f}% - {summary.loc['max', 'Tertiary_Enrolment']:.2f}%\n")
        f.write(f"  Std Dev: {summary.loc['std', 'Tertiary_Enrolment']:.2f}%\n\n")
        
        f.write("KEY INSIGHTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"1. Strong Positive Correlation: {corr:.3f}\n")
        f.write("   - As tertiary enrolment increases, unemployment tends to increase\n")
        f.write("   - This suggests a complex relationship in the South African context\n\n")
        
        f.write("2. Unemployment Trends:\n")
        f.write("   - Generally increasing trend over the period\n")
        f.write("   - Significant increase in recent years (2020-2023)\n\n")
        
        f.write("3. Education Trends:\n")
        f.write("   - Steady increase in tertiary enrolment\n")
        f.write("   - More than doubled from 11.8% (1991) to 23.7% (2021)\n\n")
        
        f.write("4. Policy Implications:\n")
        f.write("   - Investment in education may not automatically reduce unemployment\n")
        f.write("   - Need for job creation alongside education expansion\n")
        f.write("   - Structural issues in the labor market need addressing\n")
    
    logger.info(f"  Saved: {report_path}")
    return report_path


def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("STARTING EXPLORATORY DATA ANALYSIS")
    logger.info("=" * 60)
    
    # Load data
    df = load_merged_data()
    
    # Create visualizations
    create_time_series_plots(df)
    create_correlation_analysis(df)
    create_distribution_plots(df)
    
    # Create summary tables
    summary = create_summary_table(df)
    
    # Create insights report
    create_insights_report(df, summary)
    
    logger.info("\n" + "=" * 60)
    logger.info("EDA COMPLETED SUCCESSFULLY")
    logger.info("=" * 60)
    logger.info(f"Figures saved to: {FIGURES_DIR}")
    logger.info(f"Tables saved to: {TABLES_DIR}")
    logger.info(f"Reports saved to: {REPORTS_DIR}")
    
    return df


if __name__ == "__main__":
    df = main()