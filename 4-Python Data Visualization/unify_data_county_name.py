"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

CodeSkulptor: https://py3.codeskulptor.org/#save3_SZvw6JCsNu.py
"""

import csv
import math
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    countrycode_to_countryname = {}
    countrycode_not_found = []

    for keys, values in plot_countries.items():
        if values in gdp_countries:
            countrycode_to_countryname[keys] = values
        else:
            countrycode_not_found.append(keys)

    return countrycode_to_countryname, set(countrycode_not_found)


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """

    country_gdp = {}
    gdpdata_without_data_year = []

    filename = gdpinfo["gdpfile"]
    keyfield = gdpinfo["country_name"]
    separator = gdpinfo["separator"]
    quote = gdpinfo["quote"]

    gdp_data = read_csv_as_nested_dict(filename, keyfield, separator, quote)

    country_name, country_not_found = reconcile_countries_by_name(plot_countries, gdp_data)

    for keys, values in country_name.items():
        if str(year) in gdp_data[values]:
            try:
                year_gdp = int(gdp_data[values][str(year)])
                country_gdp[keys] = math.log10(year_gdp)
            except ValueError:
                gdpdata_without_data_year.append(keys)

    return country_gdp, set(country_not_found), set(gdpdata_without_data_year)


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """

    country_gdp, missing_data, no_gdp = build_map_dict_by_name(gdpinfo, plot_countries, year)

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = "GDP by country for {} (log scale), " \
                           "unified by common country NAME".format(year)
    worldmap_chart.add("GDP for {}".format(year), country_gdp)
    worldmap_chart.add("Missing from World Bank Data", missing_data)
    worldmap_chart.add("No GDP data", no_gdp)
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# test_render_world_map()
