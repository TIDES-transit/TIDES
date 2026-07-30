# Changelog

All notable changes to the TIDES specification will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **BREAKING:** Renamed `passenger_events` table to `device_events` to support station-based and mobile device events alongside vehicle-mounted APC events ([#241](https://github.com/TIDES-transit/TIDES/issues/241))
    - Primary key renamed: `passenger_event_id` → `device_event_id`
    - `device_id` is now **required** (was optional)
    - `vehicle_id` is now **optional** (was required)
    - `trip_stop_sequence` is now **optional** (was required)
- **BREAKING:** `device_events.event_type` enum values converted from Title Case to snake_case and two new types added ([#241](https://github.com/TIDES-transit/TIDES/issues/241), incorporates [#235](https://github.com/TIDES-transit/TIDES/issues/235))

### Added

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
