"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

CodeSkulptor: https://py3.codeskulptor.org/#save3_nrlQvlS9uF.py
"""

import csv
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


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    min_year = gdpinfo["min_year"]
    max_year = gdpinfo["max_year"]

    data_points = []

    for keys, values in gdpdata.items():
        try:
            year = int(keys)
            if min_year <= year <= max_year:

                data = (year, float(values))
                data_points.append(data)
        except ValueError:
            continue

    return data_points


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    country_keyvalue = {}

    filename = gdpinfo["gdpfile"]
    country_name = gdpinfo["country_name"]
    separator = gdpinfo["separator"]
    quote = gdpinfo["quote"]

    country_gdpdata = read_csv_as_nested_dict(filename, country_name, separator, quote)

    country_keyname_gdpdata = []
    for keyname in country_gdpdata:
        country_keyname_gdpdata.append(keyname)

    for country in country_list:

        if country in country_keyname_gdpdata:
            country_list_data_points = build_plot_values(gdpinfo, country_gdpdata[country])
            country_keyvalue[country] = sorted(country_list_data_points)

        else:
            country_keyvalue[country] = []

    return country_keyvalue


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """

    min_year = str(gdpinfo["min_year"])
    max_year = str(gdpinfo["max_year"])

    title_name = "Plot of GDP for select countries spanning {} to {}".format(min_year, max_year)
    xy_chart = pygal.Line(title=title_name, x_title="Year", y_title="GDP in current US dollars")

    dict_plot = build_plot_dict(gdpinfo, country_list)

    for keys, values in dict_plot.items():
        xy_chart.add(keys, values)

    xy_chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# test_render_xy_plot()
