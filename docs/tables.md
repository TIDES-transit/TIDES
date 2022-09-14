# Data Table Schemas

Data table schemas are specified in JSON and are compatible with the
[frictionless data](https://specs.frictionlessdata.io/table-schema/) table
schema standards.



## devices


|name|required|type|foreign_key|description|constraints enum|constraints unique|title|
|---|---|---|---|---|---|---|---|
|device_id|True|string|-|Identifies a device. If possible, this should match other internal agency device IDs.|-|True|-|
|stop_id|-|string|-|Identifies the stop at which the device is located. May be null if the device is on a vehicle. References GTFS|-|-|ID referencing GTFS stops.stop_id|
|vehicle_id|-|string|-|Identifies the vehicle on which the device is located. May be null if the device is at a stop or station.|-|-|ID referencing vehicles.vehicle_id|
|train_car_id|-|string|-|Identifies the train car or asset on which the device is located. May be null if the device is at a stop or station or if the Train_cars file is not used.|-|-|ID referencing train_car.train_car_id|
|device_type|-|string|-|Indicates the type of device.|Allowed Values: `APC,AFC,AVL,Other`|-|-|
|device_vendor|-|string|-|Vendor of the device.|-|-|-|
|device_model|-|string|-|Model of the device as specified by the vendor.|-|-|-|
|location|-|string|-|Indicates the location of a device on the vehicle or at a station. For example:
Front door.
Back door.
Entrance (not located on a vehicle).
Exit (not located on a vehicle).
Entrance/exit (not located on a vehicle).
Other.|-|-|-|


## vehicle_locations


|name|required|type|foreign_key|description|constraints enum|constraints maximum|constraints minimum|constraints unique|title|
|---|---|---|---|---|---|---|---|---|---|
|location_ping_id|True|string|-|Identifies the recorded vehicle location event.|-|-|-|True|-|
|date|True|date|-|Service date. References GTFS|-|-|-|-|-|
|timestamp|True|time|-|Recorded event time.|-|-|-|-|-|
|trip_id_performed|True|string|-|Identifies the trip performed.|-|-|-|-|ID referencing trips_performed.trip_id_performed|
|stop_sequence|True|string|-|Ordered stop the vehicle is approaching or serving on a particular trip. References GTFS|-|-|-|-|positive integer referencing GTFS stop_times.stop_sequence|
|vehicle_id|True|string|-|Identifies a vehicle.|-|-|-|-|ID referencing vehicles.vehicle_id|
|device_id|-|string|-|Identifies the device that recorded the vehicle location. May be null if only a single device is reporting vehicle location and the device_id is not distinct from vehicle_id.|-|-|-|-|ID references devices.device_id|
|stop_id|-|string|-|Identifies the stop the vehicle is approaching or serving currently. References GTFS|-|-|-|-|ID referencing GTFS stops.stop_id|
|current_status|-|string|-|Indicates the status of the vehicle in reference to a stop. References GTFS-Realtime|Allowed Values: `Incoming at,Stopped at,In transit to`|-|-|-|-|
|latitude|-|number|-|Degrees North, in the WGS-84 coordinate system. References GTFS-Realtime|-|90|-90|-|-|
|longitude|-|number|-|Degrees East, in the WGS-84 coordinate system. References GTFS-Realtime|-|180|-180|-|-|
|gps_quality|-|string|-|Indicates the quality of data and communication provided by the GPS.|Allowed Values: `Excellent,Good,Poor`|-|-|-|-|
|heading|-|number|-|Heading, in degrees, clockwise from true north, e.g., 0 would mean north and 90 would mean east. This can be the compass bearing, or the direction towards the next stop or intermediate location. This should not be deduced from the sequence of previous positions, which clients can compute from previous data. References GTFS-Realtime|-|360|0|-|-|
|speed|-|number|-|Momentary speed measured by the vehicle, in meters per second. References GTFS-Realtime|-|-|0|-|-|
|odometer|-|integer|-|Odometer value, in meters. References GTFS-Realtime|-|-|0|-|-|
|schedule_deviation|-|integer|-|Indicates schedule adherence in seconds. A negative value represents an early vehicle. (An unscheduled trip would not have a scheduled deviation.)|-|-|-|-|-|
|headway_deviation|-|integer|-|Indicates headway adherence in seconds. A negative value represents a shorter than scheduled headway.|-|-|-|-|-|
|in_service|-|string|-|Indicates status of travel with regard to service.|Allowed Values: `In passenger service,En-route to service,Traveling from a service trip,On a layover,Returning to a garage due to a suspension or breakdown,Travel for on-route replacement of breakdown,Other not in service`|-|-|-|-|
|schedule_relationship|-|string|-|Indicates the status of the stop. References GTFS-realtime VehiclePosition.trip.schedule_relationship|Allowed Values: `Scheduled,Skipped,No data,Unscheduled`|-|-|-|-|


## fare_transactions


|name|required|type|foreign_key|description|constraints enum|constraints minimum|constraints unique|rdfType|title|
|---|---|---|---|---|---|---|---|---|---|
|transaction_id|True|string|-|Identifies the fare transaction.|-|-|True|-|-|
|date|True|date|-|Service date. References GTFS|-|-|-|-|-|
|timestamp|True|time|-|Recorded event time, including for transactions that may be aggregated values associated with a trip or vehicle.|-|-|-|-|-|
|amount|True|number|-|Value of the transaction.|-|-|-|-|-|
|currency_type|True|string|-|Currency used for the transaction. References GTFS|-|-|-|https://schema.org/currency|-|
|fare_action|True|string|-|Indicates the type of action performed.|Allowed Values: `Unknown action type,Purchase,Enter,Exit,Transfer entrance,Transfer exit,Add,Activate,Adjust,Other`|-|-|-|-|
|trip_id_performed|-|string|-|Identifies the trip performed. May be null if the fare collection device is NOT located on a vehicle. May be null if on a vehicle but trip-level data is unavailable, in which case the data would be associated with the vehicle.|-|-|-|-|ID referencing trips_performed.trip_id_performed|
|stop_sequence|-|integer|-|Ordered stop the vehicle is serving on a particular trip. May be null if the fare collection device is NOT located on a vehicle. May be null if on a vehicle but stop-level data is unavailable, in which case the data would be associated with the vehicle and/or trip. References GTFS|-|0|-|-|positive integer referencing GTFS stop_times.stop_sequence|
|vehicle_id|-|string|-|Identifies the vehicle. May be null if collection device is NOT located on a vehicle. May be null if on a vehicle but vehicle data is unavailable, in which case the data would be associated with a trip and/or stop.|-|-|-|-|ID referencing vehicles.vehicle_id|
|device_id|-|string|-|Identifies the ITS device on which the fare transaction was performed. May be null if only a single device is reporting fare transactions on a vehicle and vehicle_id is provided. May be null if only a single device is reporting fare transactions at a stop and stop_id is provided.|-|-|-|-|ID referencing devices.device_id|
|fare_id|-|string|-|Identifies a fare class, as included in the GTFS Fare_attributes file. References GTFS|-|-|-|-|ID referencing GTFS fare_attributes.fare_id|
|stop_id|-|string|-|Identifies the stop. References GTFS|-|-|-|-|ID referencing GTFS stops.stop_id|
|group_size|-|integer|-|The number of customers included in the transaction.|-|0|-|-|-|
|media_type|-|string|-|Indicates the fare medium that was used for the transaction.|Allowed Values: `Cash or coins,Smart card or ticket,Magnetic-stripe card or ticket,Bank card,Mobile NFC,Optical scan,Button pressed by driver or operator to indicate a boarding or alighting passenger.,Other type`|-|-|-|-|
|rider_category|-|string|-|Indicates rider category (categories defined by transit agency). For example:
Adult
Youth
Student
Senior
Other reduced|-|-|-|-|-|
|fare_product|-|string|-|Indicates the fare group (fare groups defined by transit agency). For example:
Single ride
Pass
Employer sponsored
Other pass|-|-|-|-|-|
|fare_period|-|string|-|Indicates the fare period (fare periods defined by transit agency). For example:
All day
Peak
Off-peak
Summer
Other|-|-|-|-|-|
|fare_capped|True|boolean|-|Indicates if fare capping is in effect (fare capping options defined by transit agency).|-|-|-|-|-|
|fare_media_id|-|string|-|Identifies the individual fare medium used for the transaction. For example, the fare card ID.|-|-|-|-|-|
|fare_media_id_purchased|-|string|-|Identifies the individual fare medium purchased in the transaction. For example, the fare card ID.|-|-|-|-|-|
|balance|-|number|-|Stored value remaining on an account after the transaction is made.|-|-|-|-|-|


## train_cars


|name|required|type|foreign_key|description|constraints enum|constraints minimum|constraints unique|
|---|---|---|---|---|---|---|---|
|train_car_id|True|string|-|Identifies a train car or asset. If possible, this should match other internal agency asset IDs.|-|-|True|
|model_name|-|string|-|Describes the train car or asset's model.|-|-|-|
|facility_name|-|string|-|Name or internal agency ID for the facility where the train car or asset is generally held.|-|-|-|
|capacity_seated|-|integer|-|Number of seats on the train car or asset.|-|0|-|
|wheelchair_capacity|-|integer|-|Number of wheelchair spaces on the train car or asset.|-|0|-|
|bike_capacity|-|integer|-|Number of bike spaces on the train car or asset.|-|0|-|
|bike_rack|-|boolean|-|Indicates if the train car or asset has a usable bike rack.|-|-|-|
|capacity_standing|-|integer|-|Standing capacity of the train car or asset set by the manufacturer.|-|0|-|
|train_car_type|-|string|-|Indicates the type of train car or asset.|Allowed Values: `Train car,Trolley,Other`|-|-|


## operators


|name|required|type|foreign_key|description|constraints unique|
|---|---|---|---|---|---|
|operator_id|True|string|-|Identifies an operator. If possible, this should match other internal agency operator IDs.|True|


## stop_visits


|name|required|type|foreign_key|description|constraints enum|constraints minimum|title|
|---|---|---|---|---|---|---|---|
|date|True|date|-|Service date. References GTFS indirectly via calendars.txt and calendar_dates.txt|-|-|-|
|trip_id_performed|True|string|-|Identifies the trip performed References GTFS|-|-|ID referencing GTFS trips_performed.trip_id_performed|
|stop_sequence|True|integer|-|Ordered stop the vehicle is serving on a particular trip. References GTFS|-|0|positive integer referencing GTFS stop_times.stop_sequence|
|vehicle_id|True|string|-|Identifies the vehicle.|-|-|ID referencing vehicles.vehicle_id|
|dwell|-|integer|-|Indicates the amount of time a vehicle spent stopped at a stop in seconds.|-|0|-|
|stop_id|-|string|-|Identifies the stop. References GTFS|-|-|ID referencing GTFS stops.stop_id|
|checkpoint|-|boolean|-|Indicates if the stop should be used for evaluating schedule adherence, on-time performance, and other KPIs. This could be populated to match the GTFS “timepoint” field.|-|-|-|
|schedule_arrival_time|-|time|-|Scheduled time at which the vehicle arrives at a stop. References GTFS|-|-|-|
|schedule_departure_time|-|time|-|Scheduled time at which the vehicle departs from a stop. References GTFS|-|-|-|
|actual_arrival_time|-|time|-|Time at which the vehicle arrives at a stop.|-|-|-|
|actual_departure_time|-|time|-|Time at which the vehicle departs from a stop.|-|-|-|
|distance|-|integer|-|Observed distance in meters from the previous stop traveled by the vehicle.|-|0|-|
|boarding_1|-|integer|-|Number of riders that entered the front-most or right-most door of the vehicle|-|0|-|
|alighting_1|-|integer|-|Number of riders that exited the front-most or right-most door of the vehicle|-|0|-|
|boarding_2|-|integer|-|Number of riders that entered the rest of the vehicle’s doors.|-|0|-|
|alighting_2|-|integer|-|Number of riders that exited the rest of the vehicle’s doors.|-|0|-|
|load|-|integer|-|Number of riders on the vehicle when departing the stop.|-|0|-|
|door_open|-|time|-|Time at which the doors opened.|-|-|-|
|door_close|-|time|-|Time at which the doors closed.|-|-|-|
|door_status|-|string|-|Indicates actions of the doors during the stop visit.|Allowed Values: `Doors did not open,Front door opened and back doors remain closed,Back doors opened and front door remained closed,All doors opened,Other configuration`|-|-|
|ramp_deployed_time|-|number|-|Duration of time a ramp is deployed, in seconds.|-|0|-|
|ramp_failure|-|boolean|-|Indicates if the ramp deployment failed at a stop.|-|-|-|
|kneel_deployed_time|-|number|-|Duration of time a kneel is deployed in seconds.|-|0|-|
|lift_deployed_time|-|number|-|Duration of time in seconds of time a lift is deployed.|-|0|-|
|bike_rack_deployed|-|boolean|-|Indicates if the bike rack was deployed at a stop.|-|-|-|
|bike_load|-|integer|-|Number of bikes on the vehicle when departing the stop.|-|0|-|
|revenue|-|number|-|Amount of revenue collected at the stop.|-|-|-|
|number_of_transactions|-|integer|-|Number of fare transactions that occurred at a stop.|-|0|-|
|transaction_revenue_cash|-|number|-|Indicates the revenue from cash or coins.|-|-|-|
|transaction_revenue_smartcard|-|number|-|Indicates the revenue from smart card or ticket.|-|-|-|
|transaction_revenue_magcard|-|number|-|Indicates the revenue from magnetic-stripe card or ticket.|-|-|-|
|transaction_revenue_bankcard|-|number|-|Indicates the revenue from bank card (credit or debit card).|-|-|-|
|transaction_revenue_nfc|-|number|-|Indicates the revenue from mobile NFC (smartphone tap, etc.)|-|-|-|
|transaction_revenue_optical|-|number|-|Indicates the revenue from optical scan (of mobile app screen or paper ticket).|-|-|-|
|transaction_revenue_operator|-|number|-|Indicates the revenue from button pressed by driver or operator to indicate a boarding or alighting passenger.|-|-|-|
|transaction_revenue_other|-|number|-|Indicates the revenue from other fare media.|-|-|-|
|transaction_count_cash|-|number|-|Number of fare transactions made by cash or coins.|-|0|-|
|transaction_count_smartcard|-|number|-|Number of fare transactions made by smart card or ticket.|-|0|-|
|transaction_count_magcard|-|number|-|Number of fare transactions made by magnetic-stripe card or ticket.|-|0|-|
|transaction_count_bankcard|-|number|-|Number of fare transactions made by bank card (credit or debit card).|-|0|-|
|transaction_count_nfc|-|number|-|Number of fare transactions made by mobile NFC (smartphone tap, etc.)|-|0|-|
|transaction_count_optical|-|number|-|Number of fare transactions made by optical scan (of mobile app screen or paper ticket).|-|0|-|
|transaction_count_operator|-|number|-|Number of fare transactions made by button pressed by driver or operator to indicate a boarding or alighting passenger.|-|0|-|
|transaction_count_other|-|number|-|Number of fare transactions made by other fare media.|-|0|-|
|schedule_relationship|-|string|-|Indicates the status of stop’s service on the trip.(Note: schedule_arrival_time and schedule_departure_time may differ from GTFS in the case of a schedule modification). References GTFS-realtime TripUpdate|Allowed Values: `Scheduled,Skipped,Missing data,Unscheduled,Canceled,Duplicated,Schedule modified`|-|-|


## vehicle_train_cars


|name|required|type|foreign_key|description|constraints minimum|title|
|---|---|---|---|---|---|---|
|vehicle_id|True|string|-|Identifies a vehicle, such as a train consist. If possible, this should match other internal agency vehicle IDs.|-|ID referencing vehicles.vehicle_id|
|train_car_id|True|string|-|Identifies a train car or an asset that is a component of the vehicle.|-|ID referencing train_car.train_car_id|
|order|-|integer|-|The assigned order of the train car or asset within the vehicle.|0|-|
|operator_id|-|string|-|Identifies an operator (person). If possible, this should match other internal agency operator IDs.|-|-|


## vehicles


|name|required|type|foreign_key|description|constraints minimum|constraints unique|
|---|---|---|---|---|---|---|
|vehicle_id|True|string|-|Identifies a vehicle, such as a bus or a train consist. If possible, this should match other internal agency vehicle IDs and the GTFS-realtime VehicleDescriptor.|-|True|
|vehicle_start|-|time|-|The time at which the vehicle or train consist is first in operation (i.e., when the consist has been created). Required if Train_car is used.|-|-|
|vehicle_end|-|time|-|The time at which the vehicle or train consist no longer exists (i.e., the consist is separated or modified). Only used if Train_car is used.|-|-|
|model_name|-|string|-|Describes the vehicle's model.|-|-|
|facility_name|-|string|-|Name or internal agency ID for the facility where the vehicle is generally held.|-|-|
|capacity_seated|-|integer|-|Number of seats on the vehicle. Used if Train_car is not used.|0|-|
|wheelchair_capacity|-|integer|-|Number of wheelchair spaces on the vehicle. Used if Train_car is not used.|0|-|
|capacity_bike|-|integer|-|Number of bike spaces on the vehicle. Used if Train_car is not used.|0|-|
|bike_rack|-|boolean|-|Indicates if the vehicle has a useable bike rack. Used if Train_car is not used.|-|-|
|capacity_standing|-|integer|-|Standing capacity of the vehicle set by the manufacturer. Used if Train_car is not used.|0|-|


## trips_performed


|name|required|type|foreign_key|description|constraints enum|title|
|---|---|---|---|---|---|---|
|date|True|date|-|Service date. References GTFS|-|-|
|trip_id_performed|True|string|-|Identifies the trip performed.|-|-|
|vehicle_id|True|string|-|Identifies the vehicle.|-|ID referencing vehicles.vehicle_id|
|trip_id_scheduled|-|string|-|Identifies the scheduled trip associated with the trip performed. One scheduled trip may be associated with multiple operated trips, or an operated trip may not be associated with a scheduled trip. References GTFS|-|ID referencing GTFS trips.trip_id|
|route_id|-|string|-|Identifies the route. References GTFS|-|ID referencing GTFS routes.route_id|
|route_type|-|string|-|Indicates the type of transportation used on a route. References GTFS|Allowed Values: `Tram / Streetcar / Light rail,Subway / Metro,Rail,Bus,Ferry,Cable tram,Aerial lift,Funicular,Trolleybus,Monorail`|-|
|shape_id|-|string|-|Identifies a geospatial shape that describes the vehicle travel path for a trip. References GTFS|-|ID referencing shapes.shape_id|
|direction_id|-|integer|-|Indicates the direction of travel for a trip. References GTFS|Allowed Values: `0,1`|-|
|operator_id|-|string|-|Identifies the vehicle’s operator.|-|ID referencing operators.operator_id|
|block_id|-|string|-|Identifies the block to which the trip belongs. A block consists of a single trip, or many sequential trips made using the same vehicle, defined by shared service days and block_id. A block_id can have trips with different service days, making distinct blocks. See example in GTFS documentation. References GTFS|-|ID referencing trips.block_id|
|trip_start_stop_id|-|string|-|Origin stop_id. References GTFS|-|ID referencing GTFS stops.stop_id|
|trip_end_stop_id|-|string|-|Destination stop_id. References GTFS|-|ID referencing GTFS stops.stop_id|
|schedule_trip_start|-|time|-|Scheduled departure time from the trip’s origin.|-|-|
|schedule_trip_end|-|time|-|Scheduled end time at the trip’s destination.|-|-|
|actual_trip_start|-|time|-|Time at which the vehicle departed its origin.|-|-|
|actual_trip_end|-|time|-|Time at which the vehicle arrived at its destination.|-|-|
|in_service|-|string|-|Indicates status of travel with regard to service.|Allowed Values: `In passenger service,En-route to service,Traveling from a service trip,On a layover,Returning to a garage due to a suspension or breakdown,Travel for on-route replacement of breakdown,Other not in service`|-|
|schedule_relationship|-|string|-|Indicates the status of the trip. References GTFS-realtime TripUpdate.trip.schedule_relationship|Allowed Values: `Scheduled,Added,Unscheduled,Canceled,Duplicated`|-|


## station_activities


|name|required|type|foreign_key|description|constraints minimum|title|
|---|---|---|---|---|---|---|
|date|True|date|-|Service date|-|-|
|stop_id|True|string|-|Identifies stop. References GTFS|-|ID referencing GTFS stops.stop_id|
|time_period_start|True|datetime|-|Aggregation period start time.|-|-|
|time_period_end|True|datetime|-|Aggregation period end time.|-|-|
|time_period_category|-|string|-|Indicates a standard time period to aid further aggregation. For example:
All day
Peak
Off-peak
Summer
Other|-|-|
|total_entries|-|integer|-|Number of events at the stop considered entries, such as boardings or fare transactions.|0|-|
|total_exits|-|integer|-|Number of events at the stop considered exits, such as alightings.|0|-|
|number_of_transactions|-|integer|-|Number of fare transactions that occurred at a stop.|0|-|
|transaction_revenue_cash|-|number|-|Indicates the revenue from cash or coins.|-|-|
|transaction_revenue_smartcard|-|number|-|Indicates the revenue from smart card or ticket.|-|-|
|transaction_revenue_magcard|-|number|-|Indicates the revenue from magnetic-stripe card or ticket.|-|-|
|transaction_revenue_bankcard|-|number|-|Indicates the revenue from bank card (credit or debit card).|-|-|
|transaction_revenue_nfc|-|number|-|Indicates the revenue from mobile NFC (smartphone tap, etc.)|-|-|
|transaction_revenue_optical|-|number|-|Indicates the revenue from optical scan (of mobile app screen or paper ticket).|-|-|
|transaction_revenue_operator|-|number|-|Indicates the revenue from button pressed by driver or operator to indicate a boarding or alighting passenger.|-|-|
|transaction_revenue_other|-|number|-|Indicates the revenue from other fare media.|-|-|
|transaction_count_cash|-|number|-|Number of fare transactions made by cash or coins.|0|-|
|transaction_count_smartcard|-|number|-|Number of fare transactions made by smart card or ticket.|0|-|
|transaction_count_magcard|-|number|-|Number of fare transactions made by magnetic-stripe card or ticket.|0|-|
|transaction_count_bankcard|-|number|-|Number of fare transactions made by bank card (credit or debit card).|0|-|
|transaction_count_nfc|-|number|-|Number of fare transactions made by mobile NFC (smartphone tap, etc.)|0|-|
|transaction_count_optical|-|number|-|Number of fare transactions made by optical scan (of mobile app screen or paper ticket).|0|-|
|transaction_count_operator|-|number|-|Number of fare transactions made by button pressed by driver or operator to indicate a boarding or alighting passenger.|0|-|
|transaction_count_other|-|number|-|Number of fare transactions made by other fare media.|0|-|
|bike_entries|-|integer|-|Number of bikes that entered the stop.|0|-|
|bike_exits|-|integer|-|Number of bikes that exited the stop.|0|-|
|ramp_entries|-|integer|-|Number of entries that used a ramp or accessible entrance.|0|-|
|ramp_exits|-|integer|-|Number of exits that used a ramp or accessible exit.|0|-|


## passenger_events


|name|required|type|foreign_key|description|constraints enum|constraints minimum|constraints unique|title|
|---|---|---|---|---|---|---|---|---|
|passenger_event_id|True|string|-|Identifies the recorded passenger event.|-|-|True|-|
|date|True|date|-|Service date. References GTFS|-|-|-|-|
|timestamp|True|time|-|Recorded event time.|-|-|-|-|
|trip_id_performed|True|string|-|Identifies the trip performed.|-|-|-|ID referencing trips_performed.trip_id_performed|
|stop_sequence|True|integer|-|Ordered stop the vehicle is serving on a particular trip. References GTFS|-|0|-|positive integer referencing GTFS stop_times.stop_sequence|
|event_type|True|string|-|Indicates the type of event recorded.|Allowed Values: `Vehicle arrived at stop,Vehicle departed stop,Door opened,Door closed,Passenger boarded,Passenger alighted,Kneel was engaged,Kneel was disengaged,Ramp was deployed,Ramp was raised,Ramp deployment failed,Lift was deployed,Lift was raised,Individual bike boarded,Individual bike alighted,Bike rack deployed`|-|-|-|
|vehicle_id|True|string|-|Identifies a vehicle.|-|-|-|ID referencing vehicles.vehicle_id|
|device_id|-|string|-|Identifies the device that recorded the event. May be null if only a single device is reporting passenger events on a vehicle/ train car and the device_id is not distinct from vehicle_id/train_car_id.|-|-|-|ID referencing devices.device_id|
|train_car_id|-|string|-|Identifies the train car.|-|-|-|ID referencing train_car.train_car_id|
|stop_id|-|string|-|Identifies the stop the vehicle is serving. References GTFS|-|-|-|ID referencing GTFS stops.stop_id|
