"""
Data Cleaning Script for South Africa - World Bank Indicators
============================================================

This script loads raw unemployment and tertiary education data
from the World Bank, cleans it, and creates a merged dataset
for analysis.

Inputs:
    - data/raw/south_africa_unemployment.csv
    - data/raw/south_africa_tertiary_education.csv

Outputs:
    - data/processed/south_africa_combined.csv
    - data/processed/data_summary.txt

Author: Your Name
Date: 2026-08-28
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Create processed directory if it doesn't exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """
    Load raw data from CSV files.
    """
    logger.info("Loading raw data...")
    
    unemployment_path = RAW_DIR / "south_africa_unemployment.csv"
    education_path = RAW_DIR / "south_africa_tertiary_education.csv"
    
    unemployment = pd.read_csv(unemployment_path)
    education = pd.read_csv(education_path)
    
    logger.info(f"Loaded unemployment: {unemployment.shape[0]} rows")
    logger.info(f"Loaded education: {education.shape[0]} rows")
    
    return unemployment, education


def inspect_data(unemployment, education):
    """
    Print summary information about the datasets.
    """
    logger.info("=" * 60)
    logger.info("DATA INSPECTION SUMMARY")
    logger.info("=" * 60)
    
    # Unemployment
    logger.info("\nUNEMPLOYMENT:")
    logger.info(f"  Shape: {unemployment.shape}")
    logger.info(f"  Years: {unemployment['Year'].min()} - {unemployment['Year'].max()}")
    logger.info(f"  Missing values: {unemployment['Value'].isna().sum()}")
    logger.info(f"  Valid observations: {unemployment['Value'].notna().sum()}")
    
    # Education
    logger.info("\nEDUCATION:")
    logger.info(f"  Shape: {education.shape}")
    logger.info(f"  Years: {education['Year'].min()} - {education['Year'].max()}")
    logger.info(f"  Missing values: {education['Value'].isna().sum()}")
    logger.info(f"  Valid observations: {education['Value'].notna().sum()}")
    
    return None


def clean_data(unemployment, education):
    """
    Clean the datasets and prepare for merging.
    
    Steps:
    1. Remove rows with missing values
    2. Rename columns for clarity
    3. Keep only essential columns
    """
    logger.info("\nCleaning data...")
    
    # Remove missing values
    unemployment_clean = unemployment.dropna(subset=['Value']).copy()
    education_clean = education.dropna(subset=['Value']).copy()
    
    logger.info(f"  Unemployment: {len(unemployment_clean)} valid observations")
    logger.info(f"  Education: {len(education_clean)} valid observations")
    
    # Rename columns
    unemployment_clean = unemployment_clean.rename(columns={
        'Value': 'Unemployment_Rate'
    })
    
    education_clean = education_clean.rename(columns={
        'Value': 'Tertiary_Enrolment'
    })
    
    # Keep only Year and indicator columns
    unemployment_clean = unemployment_clean[['Year', 'Unemployment_Rate']]
    education_clean = education_clean[['Year', 'Tertiary_Enrolment']]
    
    return unemployment_clean, education_clean


def merge_data(unemployment_clean, education_clean):
    """
    Merge the two datasets on Year.
    """
    logger.info("\nMerging datasets...")
    
    # Inner join keeps only years present in both datasets
    merged = pd.merge(
        unemployment_clean,
        education_clean,
        on='Year',
        how='inner'
    )
    
    # Sort by year
    merged = merged.sort_values('Year').reset_index(drop=True)
    
    logger.info(f"  Merged shape: {merged.shape}")
    logger.info(f"  Year range: {merged['Year'].min()} - {merged['Year'].max()}")
    logger.info(f"  Number of years: {len(merged)}")
    
    return merged


def save_processed_data(merged):
    """
    Save the processed dataset and summary statistics.
    """
    logger.info("\nSaving processed data...")
    
    # Save main dataset
    output_path = PROCESSED_DIR / "south_africa_combined.csv"
    merged.to_csv(output_path, index=False)
    logger.info(f"  Saved dataset: {output_path}")
    
    # Save summary statistics
    summary_path = PROCESSED_DIR / "data_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("SOUTH AFRICA DATA ANALYSIS - SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("DATASET OVERVIEW:\n")
        f.write(f"  - Years: {merged['Year'].min()} - {merged['Year'].max()}\n")
        f.write(f"  - Observations: {len(merged)}\n\n")
        
        f.write("UNEMPLOYMENT RATE:\n")
        f.write(f"  - Mean: {merged['Unemployment_Rate'].mean():.2f}%\n")
        f.write(f"  - Median: {merged['Unemployment_Rate'].median():.2f}%\n")
        f.write(f"  - Min: {merged['Unemployment_Rate'].min():.2f}%\n")
        f.write(f"  - Max: {merged['Unemployment_Rate'].max():.2f}%\n")
        f.write(f"  - Std Dev: {merged['Unemployment_Rate'].std():.2f}%\n\n")
        
        f.write("TERTIARY ENROLMENT:\n")
        f.write(f"  - Mean: {merged['Tertiary_Enrolment'].mean():.2f}%\n")
        f.write(f"  - Median: {merged['Tertiary_Enrolment'].median():.2f}%\n")
        f.write(f"  - Min: {merged['Tertiary_Enrolment'].min():.2f}%\n")
        f.write(f"  - Max: {merged['Tertiary_Enrolment'].max():.2f}%\n")
        f.write(f"  - Std Dev: {merged['Tertiary_Enrolment'].std():.2f}%\n\n")
        
        f.write("CORRELATION:\n")
        corr = merged['Unemployment_Rate'].corr(merged['Tertiary_Enrolment'])
        f.write(f"  - Unemployment vs Tertiary Enrolment: {corr:.3f}\n")
    
    logger.info(f"  Saved summary: {summary_path}")
    
    return None


def main():
    """
    Main execution function.
    """
    logger.info("=" * 60)
    logger.info("STARTING DATA CLEANING PIPELINE")
    logger.info("=" * 60)
    
    # Step 1: Load data
    unemployment, education = load_data()
    
    # Step 2: Inspect data
    inspect_data(unemployment, education)
    
    # Step 3: Clean data
    unemployment_clean, education_clean = clean_data(unemployment, education)
    
    # Step 4: Merge data
    merged = merge_data(unemployment_clean, education_clean)
    
    # Step 5: Save processed data
    save_processed_data(merged)
    
    logger.info("\n" + "=" * 60)
    logger.info("DATA CLEANING PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 60)
    
    return merged


if __name__ == "__main__":
    # Run the pipeline
    merged_data = main()
    
    # Print sample of the final dataset
    print("\n" + "=" * 60)
    print("FINAL DATASET - SAMPLE")
    print("=" * 60)
    print(merged_data.head(10))