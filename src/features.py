import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats.mstats import gmean
from numpy import log as ln

from iso3166 import countries, countries_by_name  # ISO data for countries
import datetime

from src.get_data import CORONA_DATA, CONTINENTS_DATA, POPULATION_DATA

##################################
# Constants
##################################
OFFICIAL_COUNTRY_NAMES = [
    'Bolivia, Plurinational State of',  # Bolivia
    'Brunei Darussalam',  # Brunei
    'Myanmar',  # Burma
    'Congo',  # Congo (Brazzaville)
    'Congo, Democratic Republic of the',  # Congo (Kinshasa)
    "Côte d'Ivoire",  # Cote d'Ivoire
    'Iran, Islamic Republic of',  # Iran
    'Korea, Republic of',  # Korea, South
    "Lao People's Democratic Republic",  # Laos
    'Moldova, Republic of',  # Moldova
    'Russian Federation',  # Russia
    'Syrian Arab Republic',  # Syria
    'Taiwan, Province of China',  # Taiwan*
    'Tanzania, United Republic of',  # Tanzania
    'United Kingdom of Great Britain and Northern Ireland',  # United Kingdom
    'Venezuela, Bolivarian Republic of',  # Venezuela
    'Viet Nam',  # Vietnam
    'Palestine, State of',  # West Bank and Gaza
    'Virgin Islands, British',  # British Virgin Islands
    'Guernsey',  # Channel Islands: Estimated by coordinates as Saint Peter Port on Guernsey
    'Curaçao',  # Curacao
    'Réunion',  # Reunion
    'Saint Barthélemy',  # Saint Barthelemy
    'Sint Maarten (Dutch part)',  # Sint Maarten
    'Saint Martin (French part)'  # St Martin
]

DISPLAY_NAMES_DICT = {
    'Bolivia': 'Bolivia, Plurinational State of',
    'Brunei': 'Brunei Darussalam',
    'Congo': 'Congo',
    'DR Congo': 'Congo, Democratic Republic of the',
    'Iran': 'Iran, Islamic Republic of',
    'South Korea': 'Korea, Republic of',
    'Laos': "Lao People's Democratic Republic",
    'Moldova': 'Moldova, Republic of',
    'Russia': 'Russian Federation',
    'Syria': 'Syrian Arab Republic',
    'Taiwan': 'Taiwan, Province of China',
    'Tanzania': 'Tanzania, United Republic of',
    'United Kingdom': 'United Kingdom of Great Britain and Northern Ireland',
    'United States': 'US',
    'Venezuela': 'Venezuela, Bolivarian Republic of',
    'Vietnam': 'Viet Nam',
    'Palestine': 'Palestine, State of',
    'British Virgin Islands': 'Virgin Islands, British',
    'Channel Islands': 'Guernsey',
    'Sint Maarten': 'Sint Maarten (Dutch part)',
    'St Martin': 'Saint Martin (French part)'
}

# ========================================
#              PRE-PROCESSING
# ========================================

# ------------ Remove Cruise ships from Dataset ------------


def remove_ships(df):
    # Cruise ships
    ships = ['Diamond Princess', 'MS Zaandam', 'Grand Princess']

    # Remove cruise ship data from dataset
    for ship in ships:
        # Create list of index labels
        index_names = df[(df['Province.State'] == ship) |
                         (df['Country.Region'] == ship)].index
        # Delete rows with labels
        df.drop(index_names, inplace=True)

    return df


covid_data_no_ships = remove_ships(CORONA_DATA)

# ------------ Clean up Province.State ------------


def cleanup_provinces(df):
    # Create temporary data frame: Select all row where 'Province.State' != NaN
    temp_df_notna = df[pd.notna(df['Province.State'])]

    # Provinces: Sum up data in Provinces of China and Australia
    temp_df_province = temp_df_notna[(temp_df_notna['Country.Region'] == 'China') | (
        temp_df_notna['Country.Region'] == 'Australia')]

    # Group data by Country.Region, data and type - this removes Province.State column
    # Sum cases within groups
    # Ungroup to reset index
    temp_df_province = temp_df_province.groupby(['Country.Region', 'date', 'type']) \
        .sum() \
        .reset_index()

    # Rename former Colonies: Select all data where Country is not China, Australia or Canada. Delete original Country name column and replace it with Province names.
    # Select all rows where Country is neither China, nor Australia or Canada
    # Delete column 'Country.Region' and rename 'Province.State' column to 'Country.Region'
    temp_df_colonies = temp_df_notna[(temp_df_notna['Country.Region'] != 'China')
                                     & (temp_df_notna['Country.Region'] != 'Australia')
                                     & (temp_df_notna['Country.Region'] != 'Canada')] \
        .drop('Country.Region', axis=1) \
        .rename(columns={'Province.State': 'Country.Region'})

    # Province == NaN: Remove Province.State column from all rows where Country is not Canada
    # Select all rows where Country != Canada
    temp_df_not_canada = df[df['Country.Region'] != 'Canada']

    # Select all rows where Province is NaN
    temp_df_not_canada = temp_df_not_canada[temp_df_not_canada['Province.State'].isna(
    )]

    # Delete Province column
    temp_df_not_canada = temp_df_not_canada.drop('Province.State', axis=1)

    # Canada: Select all rows where Country.Region is Canada
    temp_df_canada = df[df['Country.Region'] == 'Canada']

    # Group data by Country.Region, data and type - this removes Province.State column
    # Sum cases within groups
    # Ungroup to reset index
    temp_df_canada = temp_df_canada.groupby(['Country.Region', 'date', 'type']) \
        .sum() \
        .reset_index()

    # Join temp dataframes together
    df = pd.concat([temp_df_not_canada, temp_df_province,
                    temp_df_colonies, temp_df_canada], axis=0, sort=True)

    return df


covid_data_no_provinces = cleanup_provinces(covid_data_no_ships)

#  ------------ Update Country Names to Official Names ------------


def update_country_names(df):

    # Function returns error at missing country name as string
    # The error equals the name of the object in the search
    def check_country_names(country):
        try:
            countries.get(country)
        except KeyError as error:
            return eval(str(error))

    # Create list of all countries that cannot be found by their names
    countries_not_found = [check_country_names(
        country) for country in df['Country.Region'].unique()]
    # Remove all None values (countries whee no error occured) from list
    countries_not_found = list(filter(None, countries_not_found))

    # Create a zip object from two lists
    # Create a dictionary from zip object
    missing_countries_dict = dict(
        zip(countries_not_found, OFFICIAL_COUNTRY_NAMES))

    # Replace country names with official names from dictionary
    for key, value in missing_countries_dict.items():
        df.loc[(df['Country.Region'] == key), 'Country.Region'] = value

    return df


covid_data_w_official_names = update_country_names(covid_data_no_provinces)

#  ------------ Add Column 'DisplayName' for Shorter Names in Figures ------------


def add_display_names(df):
    # Add column from Country.Region, but for countries not found use keys in missing_countries_dict
    df['DisplayName'] = df['Country.Region']

    for key, value in DISPLAY_NAMES_DICT.items():
        df.loc[(df['Country.Region'] == value), 'DisplayName'] = key

    return df


covid_data_w_display_names = add_display_names(covid_data_w_official_names)

#  ------------ Add ISO Codes to Countries ------------


def add_iso_codes(df):
    # Get 2-digit country codes
    df['iso2Code'] = [countries.get(
        row).alpha2 for row in df['Country.Region']]

    # Get 3-digit country codes
    df['iso3Code'] = [countries.get(
        row).alpha3 for row in df['Country.Region']]

    # Get numeric country codes
    # For usage with UN dtataset
    df['isoNumCode'] = [countries.get(
        row).numeric for row in df['Country.Region']]

    # Convert ISO numeric code to number
    df['isoNumCode'] = pd.to_numeric(df['isoNumCode'])

    return df


covid_data_w_iso_codes = add_iso_codes(covid_data_w_display_names)

#  ------------ Add Continents to Countries ------------


def add_continents(df):
    # Create dict from continents dataframe
    codes = CONTINENTS_DATA['Three_Letter_Country_Code']
    continents = CONTINENTS_DATA['Continent_Name']

    continents_dict = dict(zip(codes, continents))

    # Map continents dictionary to data frame
    df['Continent'] = df['iso3Code'].map(continents_dict)

    # Add 'Europe' as continent for Kosovo
    df.loc[(df['Country.Region'] == 'Kosovo'), 'Continent'] = 'Europe'

    return df


covid_data_w_continents = add_continents(covid_data_w_iso_codes)

#  ------------ Add Population Data ------------


def cleanup_population_data(df):
    # Get current year
    now = datetime.datetime.now()
    current_year = int(now.strftime('%Y'))

    # population-by-country-2020
    df = df[df['Time'] == 2018].groupby(
        ['LocID', 'Location', 'Time', 'PopTotal']).sum().reset_index()
    df.drop(['Location', 'Time', 'VarID', 'MidPeriod',
             'PopMale', 'PopFemale', 'PopDensity'], axis=1, inplace=True)
    # PopTotal in 1000s
    # Update value to single units
    df['PopTotal'] = df['PopTotal'] * 1000

    return df


def add_population_size(df):
    population_data = cleanup_population_data(POPULATION_DATA)
    # Create dictionary of LocID and PopTotal
    # Use set_index to set ID columns as the dataframe index.
    population_dict = population_data.set_index('LocID').to_dict()

    # Map continents dictionary to data frame
    df['TotalPopulation'] = df['isoNumCode'].map(population_dict['PopTotal'])

    # Kosovo: 1.907.592 (Source: https://de.wikipedia.org/wiki/Kosovo referencing CIA - The World Factbook July 2018)
    df.loc[df['Country.Region'] == 'Kosovo', 'TotalPopulation'] = 1907592

    # Channel Islands: 166.000 (Source: https://de.wikipedia.org/wiki/Kanalinseln)
    df.loc[df['Country.Region'] == 'Guernsey', 'TotalPopulation'] = 166000

    return df


covid_data_pop_size = add_population_size(covid_data_w_continents)


#  ============ STATISTICS ============

#  ------------ Calculate Cumulative Sums ------------
# Function to calculate cases per 100K
def calculate_per_100K(n, popTotal):
    return (n / popTotal) * 100000

#  ------------ Calculate Doubling Time ------------


def calculate_doubling_time(geom_mean):
    return ln(2)/ln(geom_mean)

#  ------------ Add Stats ------------


def add_stats(df):
    # Create list of unique type values
    types = list(df['type'].unique())

    # Create empty dictionary for dataframes
    d = {}

    # Create list with grouping variables for cumsum
    group_vars = ['Country.Region', 'Lat', 'Long', 'iso2Code',
                  'iso3Code', 'isoNumCode', 'TotalPopulation']

    # Loop through types
    for case_type in types:
        # Select rows where 'type' == case_type
        df_new = df[df['type'] == case_type]
        # Rename column 'cases' to 'daily_reported_cases'
        df_new = df_new.rename(columns={'cases': 'daily_reported_cases'})
        # Reset index (drop current index)
        df_new = df_new.reset_index(drop=True)
        # Add column & apply function to calculate cumsum
        df_new['cumulative_cases'] = df_new.groupby(
            group_vars)['daily_reported_cases'].apply(lambda x: x.cumsum())
        # Add df to dict
        d['df_{}'.format(case_type)] = df_new

    # Calculate Cumulative Cases per 100K
    # Iterate over all data frames in dictionary
    for df in d.values():
        # Calculate daily reported cases per 100K
        df['daily_per_100K'] = df.apply(lambda x: calculate_per_100K(
            x['daily_reported_cases'], x['TotalPopulation']), axis=1)
        # Calculate cumulative  cases per 100K
        df['cumulative_per_100K'] = df.apply(lambda x: calculate_per_100K(
            x['cumulative_cases'], x['TotalPopulation']), axis=1)

    # Rename Columns
    # Iterate over all data frames in dictionary
    for df in d.values():
        df.rename(columns={'Country.Region': 'Country', 'Lat': 'Latitude', 'Long': 'Longitude',
                           'daily_reported_cases': 'DailyReportedCases', 'date': 'Date', 'type': 'CaseType', 'iso2Code': 'ISO2Code',
                           'iso3Code': 'ISO3Code', 'isoNumCode': 'ISONumCode', 'cumulative_cases': 'CumulativeReportedCases',
                           'daily_per_100K': 'DailyReportedCasesPer100K', 'cumulative_per_100K': 'CumulativeReportedCasesPer100K'}, inplace=True)

    # Calculate Growth Factors
    group_vars = ['Country', 'DisplayName', 'Latitude', 'Longitude', 'ISO2Code',
                  'ISO3Code', 'ISONumCode', 'TotalPopulation']

    for df in d.values():
        df['GrowthFactor'] = df.groupby(group_vars)['CumulativeReportedCases'].apply(
            lambda x: x.pct_change() + 1)

    # Calculate Doubline Times in Rolling Window (7 days)
    group_vars = ['Country', 'DisplayName', 'Latitude', 'Longitude', 'ISO2Code',
                  'ISO3Code', 'ISONumCode', 'TotalPopulation', 'Continent', 'Date', 'CaseType',
                  'DailyReportedCases', 'CumulativeReportedCases',
                  'DailyReportedCasesPer100K', 'CumulativeReportedCasesPer100K']

    for key, value in d.items():
        grp = pd.DataFrame(value.groupby(group_vars)['GrowthFactor'].sum())
        grp['GF_RollingGeomMean'] = grp.rolling(7).apply(gmean, raw=True)
        grp.reset_index(inplace=True)
        d[key] = grp

    del grp

    for df in d.values():
        df['DoublingTime'] = df['GF_RollingGeomMean'].apply(
            lambda x: calculate_doubling_time(x))

    # Join data frames in d
    df = pd.concat(list(d.values()), ignore_index=True)

    return df


covid_data = add_stats(covid_data_pop_size)
#  ------------ Add Population Data ------------

#  ------------ Add Population Data ------------

# ========================================
#           PROCESSED DATAFRAMES
# ========================================
