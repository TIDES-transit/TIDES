# Changelog

All notable changes to the TIDES specification will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **BREAKING:** `stop_visits` duration fields renamed from `_time` to `_duration` suffix to distinguish from timestamp fields: `ramp_deployed_time` → `ramp_deployed_duration`, `kneel_deployed_time` → `kneel_deployed_duration`, `lift_deployed_time` → `lift_deployed_duration` ([#237](https://github.com/TIDES-transit/TIDES/issues/237))
- `passenger_events.event_count` description clarified to specify when values > 1 are appropriate, direct aggregated APC data to stop_visits, and clarify that 0 is distinct from null ([#236](https://github.com/TIDES-transit/TIDES/issues/236))
- Removed `minimum: 0` constraint from `stop_visits.departure_load`. This field is often derived from observations of boardings and alightings that are subject to observation error and those errors may result in negative values ([#270](https://github.com/TIDES-transit/TIDES/issues/270))
- **BREAKING:** Renamed `passenger_events` table to `device_events` to support station-based and mobile device events alongside vehicle-mounted APC events ([#241](https://github.com/TIDES-transit/TIDES/issues/241))
    - Primary key renamed: `passenger_event_id` → `device_event_id`
    - `device_id` is now **required** (was optional)
    - `vehicle_id` is now **optional** (was required)
    - `trip_stop_sequence` is now **optional** (was required)
- **BREAKING:** `device_events.event_type` enum values converted from Title Case to snake_case and two new types added ([#241](https://github.com/TIDES-transit/TIDES/issues/241), incorporates [#235](https://github.com/TIDES-transit/TIDES/issues/235))
- **BREAKING:** Enum values changed from 'Sentence case' to snake_case for improved code compatibility across all TIDES-defined vocabularies: `devices.device_type`, `fare_transactions.fare_action`, `fare_transactions.fare_media_id`, `stop_visits.schedule_relationship`, `train_cars.train_car_type`, `trips_performed.trip_type`, `trips_performed.schedule_relationship`, `vehicle_locations.current_status`, `vehicle_locations.gps_quality`, `vehicle_locations.trip_type`, `vehicle_locations.schedule_relationship` (`device_events.event_type` is converted as part of the `device_events` change, [#241](https://github.com/TIDES-transit/TIDES/issues/241)). `stop_visits.door_status` is renamed `stop_visits.door_action`, and its values become `none`, `front_only`, `back_only`, `all`, and `other`. `trips_performed.route_type` becomes an integer field using the GTFS numeric route type codes, including Google's Extended Route Types (for example `Bus` becomes `3` and `Express Bus Service` becomes `702`). `trips_performed.ntd_mode` changes from NTD mode names to the two-character NTD mode codes from the NTD Policy Manual (for example `Bus` becomes `MB`, `Commuter Rail` becomes `CR`, `Público` becomes `PB`); the `Demand Taxi` and `Other` values, which have no NTD code, are removed and the field is left empty when a trip has no NTD mode. One value is renamed rather than mechanically converted: fare media "Button pressed by driver or operator to indicate a boarding or alighting passenger." becomes `operator_button_press`. ([#235](https://github.com/TIDES-transit/TIDES/issues/235))

### Added

- `vehicles.vehicle_label` optional field for user-visible vehicle numbers displayed on exterior, distinguishing from internal `vehicle_id`. Aligns with GTFS-realtime VehicleDescriptor.label ([#240](https://github.com/TIDES-transit/TIDES/issues/240))
- `device_events.latitude` and `device_events.longitude` fields for mobile device events not at fixed locations ([#241](https://github.com/TIDES-transit/TIDES/issues/241))
- `device_events.employee_id` field for handheld validator events operated by fare inspectors or conductors ([#241](https://github.com/TIDES-transit/TIDES/issues/241))
- `passenger_entry` and `passenger_exit` event types for station-based events like fare gate passages ([#241](https://github.com/TIDES-transit/TIDES/issues/241))

## [1.0] - 2025-12-23

### Changed

- Promoted to stable release (no normative changes from v1.0-beta.1)

### Added

- CHANGELOG.md to track specification changes

## [1.0-beta.1] - 2024-01-06

### Added

- Initial pre-release of the TIDES data specification
- **Core Tables:**
    - `vehicle_locations` - Timestamped vehicle locations and speeds.
    - `passenger_events` - Timestamped passenger-related events, including boardings and alightings.
    - `fare_transactions` - Timestamped fare transaction, associated with devices.
    - `stop_visits` - Summarized boarding, alighting, arrival, departure, and other events (kneel engaged, ramp deployed, etc.) by trip and stop for each service date.
    - `trips_performed` - Trips performed for each service date.
    - `station_activities` - Summarized transactions, entries, and exits by stop or station and time period for each service date (for events not associated with a trip).
    - `devices` - Measurement devices, such as AVL, APC, and AFC devices, associated with vehicles or stops or stations.
    - `train_cars` - Assets that comprise vehicles, such as train cars, with descriptive information.
    - `vehicle_train_cars` - Relationships between assets and vehicles.
    - `vehicles` - Vehicles, including buses and train consists, with descriptive information.
    - `operators` - Personnel who operate vehicles.
- TIDES Data Package Profile for data packaging
- Sample template data package structure
- Validation tools and test scripts
- Documentation site with governance policies
- Change management policy with semantic versioning

[Unreleased]: https://github.com/TIDES-transit/TIDES/compare/v1.0...HEAD
[1.0]: https://github.com/TIDES-transit/TIDES/compare/v1.0-beta.1...v1.0
[1.0-beta.1]: https://github.com/TIDES-transit/TIDES/releases/tag/v1.0-beta.1
