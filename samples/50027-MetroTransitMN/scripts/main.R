#!/usr/bin/env Rscript

# Convert raw CAD/AVL data into TIDES spec
library(data.table)

## Setup ####
AGENCY_PATH = file.path('samples', '50027-MetroTransitMN')
RAW_PATH = file.path(AGENCY_PATH, 'data-raw')
TIDES_PATH = file.path(AGENCY_PATH, 'TIDES')

## Event tables ####

## vehicle_locations
vl_req = c('location_ping_id', 'date', 'timestamp', 'trip_id_performed', 'stop_sequence', 'vehicle_id')
vl_opt = c('device_id', 'stop_id', 'current_status', 'latitude', 'longitude', 'gps_quality', 'heading', 'speed', 'odometer', 'schedule_deviation', 'headway_deviation', 'in_service', 'schedule_relationship')
vl = fread(file.path(RAW_PATH, 'vehicle_locations.csv'), colClasses = list('character' = c('logged_message_short_id', 'calendar_id', 'source_host'), 'numeric' = c('longitude', 'latitude', 'heading', 'speed'), 'integer' = c('odometer', 'adherence_seconds')), integer64 = 'character')

# extract date/time
vl[, `:=`(date = as.IDate(calendar_id, format = '1%Y%m%d'))]

# convert integer lonlat to numeric
lonlat = c('longitude', 'latitude')
vl[, (lonlat) := lapply(.SD, `*`, 1e-7), .SDcols = lonlat]

# convert odometer from 100 feet to m and speed to mps
# FIXME: spec says odometer is integer, should probably be numeric
vl[, `:=`(speed = speed * 0.44704, odometer = as.integer(odometer * 16.09344))]

# convert validity to FOM to gps_quality enum
# FIXME: gps_quality enum doesn't allow for "unknown", issue #47
vl[, `:=`(FOM = bitwAnd(validity, 15L))]
vl[, gps_quality := fcase(FOM == 2L, 'Excellent', FOM %between% c(3L, 8L), 'Good', 8L < FOM, 'Poor', default = NA_character_)]

# update names
setnames(vl, c('logged_message_short_id', 'adherence_seconds', 'source_host', 'message_timestamp'), c('location_ping_id', 'schedule_deviation', 'vehicle_id', 'timestamp'))

# add NAs for required fields until I write code to merge in trip_id and stop_sequence
if (!hasName(vl, 'trip_id_performed')) vl[, `:=`(trip_id_performed = NA_character_)]
if (!hasName(vl, 'stop_sequence')) vl[, `:=`(stop_sequence = NA_integer_)]
fwrite(vl[, c(vl_req, intersect(names(vl), vl_opt)), with = FALSE], file.path(TIDES_PATH, 'vehicle_locations.csv'), quote = TRUE, logical01 = TRUE, scipen = 7L)
