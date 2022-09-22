# Create samples of raw CAD/AVL data
# - limit to 100 rows per file
library(data.table)
library(odbc)

## Setup ####
RAW_PATH = file.path('samples', '50027-MetroTransitMN', 'data-raw')
DATE = as.Date('2022-09-20')
CALENDAR_ID = as.integer(strftime(DATE, format = '1%Y%m%d'))

## Event data ####
tmdl = dbConnect(odbc(), "TMDailyLog")
odbcSetTransactionIsolationLevel(tmdl, 'read_uncommitted')

## vehicle locations
vehicle_locations = data.table(dbGetQuery(tmdl, "SELECT TOP 1000 logged_message_short_id, calendar_id, message_timestamp, source_host, latitude, longitude, validity, heading, speed, odometer, adherence_seconds FROM logged_message_short WHERE message_type_id = 12 AND calendar_id = ?", params = CALENDAR_ID), key = 'logged_message_short_id')
fwrite(vehicle_locations, file.path(RAW_PATH, 'vehicle_locations.csv'))

## passenger events

dbDisconnect(tmdl)

## fare transactions

## Summary data ####

## stop visits

## trips performed

## station activities

## Supporting data ####

## devices

## train cars

## vehicle train cars

## vehicles

## operators
