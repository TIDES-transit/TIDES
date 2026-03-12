# Changelog

All notable changes to the TIDES specification will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **BREAKING:** `stop_visits` duration fields renamed from `_time` to `_duration` suffix to distinguish from timestamp fields: `ramp_deployed_time` → `ramp_deployed_duration`, `kneel_deployed_time` → `kneel_deployed_duration`, `lift_deployed_time` → `lift_deployed_duration` ([#237](https://github.com/TIDES-transit/TIDES/issues/237))

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
