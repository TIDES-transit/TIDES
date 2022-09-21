# Create samples of raw CAD/AVL data
# - limit to 100 rows per file
library(data.table)
library(odbc)

## Setup ####
RAW_PATH = file.path('samples', '50027-MetroTransitMN', 'data-raw')

## Event data ####
tmdl = dbConnect(odbc(), "TMDailyLog")
odbcSetTransactionIsolationLevel(tmdl, 'read_uncommitted')

## vehicle locations
# result = data.table(dbGetQuery(tmdl, "SELECT logged_message_id location_ping_id, calendar_id - 1e8 date, MESSAGE_TIMESTAMP timestamp, source_host vehicle_id, latitude * 1e-7 latitude, longitude * 1e-7 longitude, validity & 15 FOM, heading bearing, speed * 0.44704 speed, CAST(odometer * 16.09344 AS INTEGER) odometer, adherence schedule_deviation FROM logged_message_short WHERE message_type_id = 12 AND calendar_id BETWEEN ? AND ?", params = as.integer(strftime(c(start_date, end_date), '1%Y%m%d'))))
vehicle_locations = data.table(dbGetQuery(tmdl, "SELECT TOP 1000 logged_message_short_id, calendar_id, message_timestamp, source_host, latitude, longitude, validity, heading, speed, odometer, adherence_seconds FROM logged_message_short WHERE message_type_id = 12 AND calendar_id = ?", params = as.integer(strftime(Sys.Date(), '1%Y%m%d'))), key = 'logged_message_short_id')
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
