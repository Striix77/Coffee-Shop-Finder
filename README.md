## Overview

You have been hired by a company that builds a app for coffee addicts. You are
responsible for taking the user’s location and returning a list of the three closest coffee shops.

## Input

The coffee shop list is a comma separated file with rows of the following form:
`Name,Y Coordinate,X Coordinate`

The quality of data in this list of coffee shops may vary. Malformed entries should cause the
program to exit appropriately.

Your program will be executed directly from the command line and will be provided three
arguments in the following order:
`<user x coordinate> <user y coordinate> <shop data url>`

Notice that the data file will be read from an network location (ex: https://raw.githubusercontent.com/Agilefreaks/test_oop/master/coffee_shops.csv)

## Output

Write a program that takes the user’s coordinates encoded as listed above and prints out a
newline­separated list of the three closest coffee shops (including distance from the user) in
order of closest to farthest. These distances should be rounded to four decimal places.

Assume all coordinates lie on a plane.

The output should be very simple no UI is required.

## Example

Using the [coffee_shops.csv](coffee_shops.csv)

**Input**

`47.6 -122.4 coffee_shops.csv`

**Expected output**

```
Starbucks Seattle2,0.0645
Starbucks Seattle,0.0861
Starbucks SF,10.0793
```

## Setup

**Requirements**

- Python 3.12+
- Project uses only Python's standard library, no extra installs required:

`math, sys, urllib.request, csv, tkinter, ttk, filedialog, messagebox`

**Clone the repository**

```
git clone https://github.com/Striix77/Coffee-Shop-Finder.git
cd Coffee-Shop-Finder
```

## Usage

This program has two runnable versions:

**Command Line Version**

`python .\closest_coffee_shop_cli.py <user x coordinate> <user y coordinate> <shop data url>`

**UI Version**

`python .\closest_coffee_shop_ui.py`

## Troubleshooting

**Tkinter not found/UI crashes**

- Make sure you are running Python 3.12+ from python.org or Homebrew, not the system Python.

**Crashes regarding themes**

- Themes exclusive to Windows: `vista, winxpnative, and winnative`
- Themes exclusive to MacOS: `aqua`
- Themes available on **all platforms**: `alt, default, clam, classic`
