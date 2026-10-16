# Migrating from TIDES v1.0 to v2.0

!!! warning "Draft"

    This guide is a working draft. It reflects the changes staged for the v2.0 release and will be finalized when v2.0 is released. Field names and details below may change during review.

TIDES v2.0 is a major release containing backwards-incompatible changes. This guide summarizes every change from v1.0 and what producers and consumers of TIDES data need to do to migrate.

## Summary of changes

| Change | Type | Affected tables |
|---|---|---|
| `passenger_events` renamed to `device_events` with expanded scope | Breaking | `passenger_events` → `device_events` |
| `event_type` enumeration values renamed to `snake_case` | Breaking | `device_events` |
| Duration fields renamed with explicit `_duration` suffix | Breaking | `stop_visits` |
| `minimum: 0` constraint removed from `departure_load` | Normative (constraint relaxed) | `stop_visits` |
| Vehicle attributes normalized into `vehicle_groups`; `train_cars` and `vehicle_train_cars` removed; `vehicle_assignments` and `consist_vehicles` added | Breaking | `vehicles`, `train_cars`, `vehicle_train_cars`, and new tables |
| `vehicle_direction` field added to operational tables | New optional field | `vehicle_locations`, `stop_visits`, `trips_performed`, `fare_transactions`, `device_events` |
| `vehicle_label` field added | New optional field | `vehicles` |
| `vehicle_crew` supporting table added | New optional table | `vehicle_crew` |
| `event_count` usage and APC data guidance clarified | Non-normative | `device_events` |

## Breaking changes

### `passenger_events` is now `device_events`

The `passenger_events` table is renamed to `device_events` and generalized from a vehicle-centered to a device-centered model. The table now covers three kinds of measurement devices:

1. **Vehicle-mounted devices** (the existing APC use case)
2. **Station-based devices** (fare gates, turnstiles)
3. **Mobile devices** (handheld validators used by fare inspectors and conductors)

To migrate:

- Rename the file `passenger_events.csv` to `device_events.csv` and update the resource entry in `datapackage.json`.
- Rename the primary key column `passenger_event_id` to `device_event_id`.
- Populate `device_id` for every record; it is now **required** (it was optional in v1.0). Every event must be traceable to a device in the `devices` table.
- `vehicle_id` and `trip_stop_sequence` are now **optional** (they were required in v1.0). Existing vehicle-based records can keep them populated; station-based and mobile device events may leave them empty.
- New optional fields are available: `employee_id` (for mobile/handheld devices), `latitude`, and `longitude` (for mobile device events not at a fixed location).
- New `event_type` values `passenger_entry` and `passenger_exit` support station fare-gate and turnstile events.

### `event_type` values are now `snake_case`

Descriptive-sentence enumeration values in `event_type` are replaced with `snake_case` identifiers. Producers must map values as follows:

| v1.0 value | v2.0 value |
|---|---|
| `Vehicle arrived at stop` | `vehicle_arrived` |
| `Vehicle departed stop` | `vehicle_departed` |
| `Door opened` | `door_opened` |
| `Door closed` | `door_closed` |
| `Passenger boarded` | `passenger_boarded` |
| `Passenger alighted` | `passenger_alighted` |
| `Kneel was engaged` | `kneel_engaged` |
| `Kneel was disengaged` | `kneel_disengaged` |
| `Ramp was deployed` | `ramp_deployed` |
| `Ramp was raised` | `ramp_raised` |
| `Ramp deployment failed` | `ramp_failed` |
| `Lift was deployed` | `lift_deployed` |
| `Lift was raised` | `lift_raised` |
| `Individual bike boarded` | `bike_boarded` |
| `Individual bike alighted` | `bike_alighted` |
| `Bike rack deployed` | `bike_rack_deployed` |

### Duration fields renamed in `stop_visits`

Three fields holding durations are renamed with an explicit `_duration` suffix to distinguish them from timestamps:

| v1.0 field | v2.0 field |
|---|---|
| `kneel_deployed_time` | `kneel_deployed_duration` |
| `ramp_deployed_time` | `ramp_deployed_duration` |
| `lift_deployed_time` | `lift_deployed_duration` |

Field semantics are unchanged; only the names change.

### Vehicles, vehicle groups, assignments, and consists

Vehicle representation is restructured to normalize attributes and properly support rail consists:

- **`vehicle_groups` (new):** shared attributes (seated capacity, full capacity, wheelchair capacity, bike capacity) for a group of vehicles of the same type. Attribute fields move here from `vehicles` and `train_cars`.
- **`vehicles` (repurposed):** the static or slowly changing list of physical vehicles, buses and train cars alike, each referencing a `vehicle_group_id` for its attributes, plus identifying information (`vehicle_label`, `license_plate`, in-service `start_date` and `end_date`).
- **`vehicle_assignments` (new, optional):** the daily record of a single vehicle or a consist that operational data can be associated with.
- **`consist_vehicles` (new):** the individual cars that make up a consist, with order and orientation. Replaces `vehicle_train_cars`.
- **`train_cars` and `vehicle_train_cars` (removed):** train cars are now records in `vehicles`; consist membership lives in `consist_vehicles`.
- **`vehicle_direction` (new, optional):** added to `vehicle_locations`, `stop_visits`, `trips_performed`, `fare_transactions`, and `device_events` to represent the direction a train is moving during operation.

To migrate:

- Split vehicle attribute data out of `vehicles` and `train_cars` into `vehicle_groups` records, one per distinct vehicle type.
- Combine bus and train car records into a single `vehicles` table, each referencing its `vehicle_group_id`.
- Convert `vehicle_train_cars` records into `consist_vehicles` records with `car_order` and `car_orientation`.
- Remove `train_cars.csv` and `vehicle_train_cars.csv` from the data package and add the new tables to `datapackage.json`.

### `stop_visits.departure_load` may be negative

The `minimum: 0` constraint is removed. `departure_load` is typically derived from boardings and alightings rather than directly observed, and APC observation error can legitimately produce negative derived values, particularly at low loads.

**For producers:** negative values are valid and permitted. Document in your dataset metadata how negative values should be interpreted (for example, unadjusted derived values retained for aggregate accuracy). Nothing requires you to publish negative values; producers who adjust loads for internal consistency may continue to do so.

**For consumers:** do not assume `departure_load` is nonnegative. A negative value is a measurement artifact of the derived calculation, not a physical passenger count. For aggregate calculations (passenger miles, average loads), retaining negative values preserves statistical accuracy, since clamping them to zero introduces upward bias; for record-level display or operational reporting, treat interpretation per the producer's documentation.

## New optional capabilities

These additions are backwards-compatible; adopting them is optional.

- **`vehicle_crew` table:** supports multiple crew members per trip, including mid-trip reliefs, with `crew_role` and start/end times. `trips_performed.operator_id` remains for the single-operator case.
- **`vehicle_label` field:** separates the user-visible vehicle number from the internal `vehicle_id`. Aligns with GTFS-realtime `VehicleDescriptor.label`.

A `device_status` table for tracking device availability was considered during v2.0 development and deferred to a future minor release pending implementation experience (see #253).

## Non-normative clarifications

- `event_count` usage and APC data guidance are clarified in the `device_events` table documentation. No data changes are required.

## Migration checklist for producers

- [ ] Rename `passenger_events.csv` to `device_events.csv`; rename `passenger_event_id` to `device_event_id`.
- [ ] Populate `device_id` on all device events and register devices in the `devices` table.
- [ ] Map `event_type` values to their `snake_case` equivalents.
- [ ] Rename the three `stop_visits` duration fields.
- [ ] Restructure vehicle data into `vehicles` + `vehicle_groups` (+ `vehicle_assignments` / `consist_vehicles` for rail).
- [ ] Remove `train_cars.csv` and `vehicle_train_cars.csv`.
- [ ] Update `datapackage.json` resource entries and the profile reference to the v2.0 spec.
- [ ] Re-validate the data package against the v2.0 schemas.

## Migration checklist for consumers

- [ ] Update queries and joins from `passenger_events` to `device_events`; handle records where `vehicle_id` is empty (station and mobile device events).
- [ ] Update any `event_type` string matching to the `snake_case` values.
- [ ] Update references to the renamed `stop_visits` duration fields.
- [ ] Remove any assumption that `stop_visits.departure_load` is nonnegative; handle negative derived values per the producer's documented interpretation.
- [ ] Source vehicle attributes (capacities) from `vehicle_groups` via `vehicles.vehicle_group_id`.
- [ ] Replace `train_cars` / `vehicle_train_cars` joins with `vehicles` / `consist_vehicles`.
