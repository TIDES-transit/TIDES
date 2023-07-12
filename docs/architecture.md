# TIDES Tables Schema

Schemas for TIDES suite.

## Files in Specification

TIDES consists of a package of files as defined in the following table.

**The following table is automatically generated from [`tides.spec.json`]( https://github.com/TIDES-transit/TIDES/blob/main/spec/tides.spec.json)**

{{ frictionless_spec('spec/tides.spec.json') }}

File components for TIDES are specified in [`tides.spec.json`](http://github.com/TIDES-transit/TIDES/blob/main/spec/tides.spec.json) in a format compatible with the
[frictionless data](https://specs.frictionlessdata.io/tabular-data-package/) data package standard.

## Relationships

Files in the TIDES suite are related to each other and other open standards as follows:

```mermaid
graph LR;
    avl(((AVL))) --> vehicle_locations[/vehicle_locations/]
    APC --> passenger_events[/passenger_events/]
    AFC --> fare_transactions[/fare_transactions/]
    vehicle_locations --> summary[Summary Process]
    fare_transactions --> summary
    passenger_events --> summary
    summary --> |stop_id,trip_id,vehicle_id|stop_visits[/stop_visits/]
    summary -->|stop_id| station_activities[/station_activities/]
    summary --> trips_performed[/trips_performed/]
    trips.txt[/trips.txt/] --> |trip_id| stop_times.txt[/stop_times.txt/]
    stops.txt[/stops.txt/] --> |stop_id|stop_times.txt
    calendar.txt[/calendar.txt/] --> |service_id|stop_times.txt
    vehicle_train_cars[/vehicle_train_cars/] -.vehicle_id.- vehicles[/vehicles/]
    vehicle_train_cars -.- |train_car_id| train_cars[/train_cars/]
    train_cars -.- |train_car_id| devices[/devices/]
    vehicles  --- |vehicle_id| devices
    vehicles --> |vehicle_id|trips_performed
    operators[/operators/] -.-> |operator_id| trips_performed
    stop_times.txt --> |"
        stop_times.txt: stop_id,stop_sequence
        stop_visits: stop_id,scheduled_stop_sequence
    "| stop_visits
    stop_times.txt --> |trips.txt| trips_performed
    stops.txt --> |stop_id|station_activities
    stop_times.txt --> |"
        stop_times.txt: stop_id,stop_sequence
        vehicle_locations: stop_id,scheduled_stop_sequence
    "| vehicle_locations
    stop_times.txt --> |"
        stop_times.txt: stop_id,stop_sequence
        passenger_events: stop_id,scheduled_stop_sequence
    "| passenger_events
    stop_times.txt --> |"
        stop_times.txt: stop_id,stop_sequence
        fare_transactions: stop_id,scheduled_stop_sequence
    "| fare_transactions
    subgraph eventf [Event Data]
        vehicle_locations
        passenger_events
        fare_transactions
    end
    subgraph summaryf [Summary Files]
        station_activities
        stop_visits
        trips_performed
    end
    subgraph gtfs [ GTFS ]
        stop_times.txt
        stops.txt
        trips.txt
        calendar.txt
    end
    subgraph proposedGTFS [ Proposed GTFS ]
        train_cars
        vehicle_train_cars
        vehicles
    end
    subgraph additional [ Additional Data ]
        devices
        operators
    end
    click stops.txt "https://gtfs.org/schedule/reference/#stopstxt"
    click stop_times.txt "https://gtfs.org/schedule/reference/#stop_timestxt"
    click calendar.txt "https://gtfs.org/schedule/reference/#calendartxt"
    click trips.txt "https://gtfs.org/schedule/reference/#tripstxt"
    click station_activities "../tables/#station-activities"
    click stop_visits "../tables/#stop-visits"
    click train_cars "../tables/#train-cars"
    click vehicle_train_cars "../tables/#vehicle-train-cars"
    click vehicles "../tables/#vehicles"
    click devices "../tables/#devices"
    click vehicle_locations "../tables/#vehicle-locations"
    click passenger_events "../tables/#passenger-events"
    click fare_transactions "../tables/#fare-transactions"
```
