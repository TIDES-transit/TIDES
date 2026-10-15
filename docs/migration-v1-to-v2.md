# Migrating from TIDES v1.0 to v2.0

!!! note "Pre-release"

    This guide covers the changes in the v2.0-alpha.1 pre-release. Everything described here has been approved through the change management process. One area targeted for v2.0, vehicles and consists, is still in review and is not part of alpha.1; see the placeholder section below. That area will be added to this guide when it lands in v2.0 final.

TIDES v2.0 is a major release containing backwards-incompatible changes. This guide summarizes every change from v1.0 and what producers and consumers of TIDES data need to do to migrate.

## Summary of changes

| Change | Type | Affected tables |
|---|---|---|
| `passenger_events` renamed to `device_events` with expanded scope | Breaking | `passenger_events` → `device_events` |
| Enumeration values renamed to `snake_case` across TIDES-defined vocabularies | Breaking | `device_events`, `devices`, `fare_transactions`, `stop_visits`, `train_cars`, `trips_performed`, `vehicle_locations` |
| `ntd_mode` values switched to NTD's two-character mode codes | Breaking | `trips_performed` |
| `stop_visits.door_status` renamed to `door_action`, with shorter values | Breaking | `stop_visits` |
| `route_type` switched to GTFS numeric codes (integer field) | Breaking | `trips_performed` |
| Duration fields renamed with explicit `_duration` suffix | Breaking | `stop_visits` |
| `minimum: 0` constraint removed from `departure_load` | Normative (constraint relaxed) | `stop_visits` |
| `operators` table restructured into `crew` | Breaking | `operators` → `crew`; `trips_performed`, `vehicle_train_cars` |
| `vehicle_label` field added | New optional field | `vehicles` |
| `vehicle_crew` supporting table added | New optional table | `vehicle_crew` |
| Vehicles and consists restructure | In review for v2.0 final; not in alpha.1 | `vehicles`, `train_cars`, `vehicle_train_cars` (unchanged in alpha.1) |
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
- `employee_id` is a free identifier in alpha.1 and is not linked to the new `crew` table; how it relates to `crew.crew_id` is subject to change in v2.0 final.
- New `event_type` values `passenger_entry` and `passenger_exit` support station fare-gate and turnstile events.

### Enumeration values are now `snake_case`

Descriptive-sentence enumeration values in every TIDES-defined vocabulary are replaced with `snake_case` identifiers, for code compatibility. The rule agreed by the Contributors Group: vocabularies that TIDES defines itself convert; values inherited from externally maintained vocabularies keep their source form. `trips_performed.route_type` (GTFS) moves to the numeric codes GTFS itself uses (mapping below), and `direction_id` is numeric and untouched. `trips_performed.ntd_mode` (NTD) also stays in NTD's own form, but moves from NTD's mode names to its official two-character codes (mapping below).

Thirteen fields across seven tables are affected. Producers must map values as follows. Consumers matching on any of these strings must update the same way.

#### `device_events.event_type`

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

The new values `passenger_entry` and `passenger_exit` (station fare gates and turnstiles) have no v1.0 equivalent.

#### `devices.device_type`

| v1.0 value | v2.0 value |
|---|---|
| `Farebox` | `farebox` |
| `Fare gate` | `fare_gate` |
| `Fare vending machine` | `fare_vending_machine` |
| `Passenger counter` | `passenger_counter` |
| `Vehicle location` | `vehicle_location` |
| `Other` | `other` |

#### `fare_transactions.fare_action`

| v1.0 value | v2.0 value |
|---|---|
| `Unknown action type` | `unknown_action_type` |
| `Purchase` | `purchase` |
| `Enter` | `enter` |
| `Exit` | `exit` |
| `Transfer entrance` | `transfer_entrance` |
| `Transfer exit` | `transfer_exit` |
| `Add` | `add` |
| `New` | `new` |
| `Capture` | `capture` |
| `Extend` | `extend` |
| `Combine` | `combine` |
| `Void` | `void` |
| `Activate` | `activate` |
| `Adjust` | `adjust` |
| `Other` | `other` |

#### `fare_transactions.fare_media_id`

| v1.0 value | v2.0 value |
|---|---|
| `Cash or coins` | `cash_or_coins` |
| `Smart card or ticket` | `smart_card_or_ticket` |
| `Magnetic-stripe card or ticket` | `magnetic_stripe_card_or_ticket` |
| `Bank card` | `bank_card` |
| `Mobile NFC` | `mobile_nfc` |
| `Optical scan` | `optical_scan` |
| `Button pressed by driver or operator to indicate a boarding or alighting passenger.` | `operator_button_press` |
| `Other type` | `other_type` |

The sentence-long fare media value is the one editorial rename in the set; its meaning is unchanged.

#### `stop_visits.door_status` is now `door_action`

The field is renamed from `door_status` to `door_action`, and its values are shortened rather than mechanically converted. The field description lists what each value means.

| v1.0 value | v2.0 value |
|---|---|
| `Doors did not open` | `none` |
| `Front door opened and back doors remain closed` | `front_only` |
| `Back doors opened and front door remained closed` | `back_only` |
| `All doors opened` | `all` |
| `Other configuration` | `other` |

#### `stop_visits.schedule_relationship` and `vehicle_locations.schedule_relationship`

| v1.0 value | v2.0 value |
|---|---|
| `Scheduled` | `scheduled` |
| `Skipped` | `skipped` |
| `Added` | `added` |
| `Missing` | `missing` |

#### `trips_performed.schedule_relationship`

| v1.0 value | v2.0 value |
|---|---|
| `Scheduled` | `scheduled` |
| `Added` | `added` |
| `Unscheduled` | `unscheduled` |
| `Canceled` | `canceled` |
| `Duplicated` | `duplicated` |

#### `trips_performed.trip_type` and `vehicle_locations.trip_type`

| v1.0 value | v2.0 value |
|---|---|
| `In service` | `in_service` |
| `Deadhead` | `deadhead` |
| `Layover` | `layover` |
| `Pullout` | `pullout` |
| `Pullin` | `pullin` |
| `Extra Pullout` | `extra_pullout` |
| `Extra Pullin` | `extra_pullin` |
| `Deadhead To Layover` | `deadhead_to_layover` |
| `Deadhead From Layover` | `deadhead_from_layover` |
| `Other not in service` | `other_not_in_service` |

#### `train_cars.train_car_type`

| v1.0 value | v2.0 value |
|---|---|
| `Train car` | `train_car` |
| `Trolley` | `trolley` |
| `Other` | `other` |

#### `vehicle_locations.current_status`

| v1.0 value | v2.0 value |
|---|---|
| `Incoming at` | `incoming_at` |
| `Stopped at` | `stopped_at` |
| `In transit to` | `in_transit_to` |

#### `vehicle_locations.gps_quality`

| v1.0 value | v2.0 value |
|---|---|
| `Excellent` | `excellent` |
| `Good` | `good` |
| `Poor` | `poor` |

### `trips_performed.ntd_mode` uses NTD's two-character mode codes

`ntd_mode` values change from NTD mode names to the official two-character mode codes listed in the Modes and Types of Service section of the [NTD Full Reporting Policy Manual](https://www.transit.dot.gov/ntd/manuals). The codes follow the 2026 edition of the manual; if NTD revises its list of modes, the `ntd_mode` values will be updated through the change management process. `Demand Taxi` and `Other` are removed because neither has a code in the 2026 manual. The field is optional; leave it empty for trips with no NTD mode.

| v1.0 value | v2.0 value |
|---|---|
| `Aerial Tramway` | `TR` |
| `Alaska Railroad` | `AR` |
| `Bus` | `MB` |
| `Bus Rapid Transit` | `RB` |
| `Cable Car` | `CC` |
| `Commuter Bus` | `CB` |
| `Commuter Rail` | `CR` |
| `Demand Response` | `DR` |
| `Demand Taxi` | removed |
| `Ferryboat` | `FB` |
| `Heavy Rail` | `HR` |
| `Hybrid Rail` | `YR` |
| `Inclined Plane` | `IP` |
| `Jitney` | `JT` |
| `Light Rail` | `LR` |
| `Monorail/Automated Guideway` | `MG` |
| `Other` | removed |
| `Público` | `PB` |
| `Streetcar` | `SR` |
| `Trolleybus` | `TB` |
| `Vanpool` | `VP` |

### `trips_performed.route_type` uses GTFS numeric codes

`route_type` changes from GTFS route type names to the numeric codes GTFS itself uses in `routes.txt`, and becomes an integer field. Google's [Extended Route Types](https://developers.google.com/transit/gtfs/reference/extended-route-types) stay available alongside the basic GTFS codes, so every value allowed in v1.0 has a code. Two codes that couldn't be listed by name in v1.0 are now available: `403`, which shares the name "Urban Railway Service" with `400`, and `405`, which shares the name "Monorail" with the basic code `12`.

| v1.0 value | v2.0 value |
|---|---|
| `Tram / Streetcar / Light rail` | `0` |
| `Subway / Metro` | `1` |
| `Rail` | `2` |
| `Bus` | `3` |
| `Ferry` | `4` |
| `Cable tram` | `5` |
| `Aerial lift` | `6` |
| `Funicular` | `7` |
| `Trolleybus` | `11` |
| `Monorail` | `12` |
| `Railway Service` | `100` |
| `High Speed Rail Service` | `101` |
| `Long Distance Trains` | `102` |
| `Inter Regional Rail Service` | `103` |
| `Car Transport Rail Service` | `104` |
| `Sleeper Rail Service` | `105` |
| `Regional Rail Service` | `106` |
| `Tourist Railway Service` | `107` |
| `Rail Shuttle (Within Complex)` | `108` |
| `Suburban Railway` | `109` |
| `Replacement Rail Service` | `110` |
| `Special Rail Service` | `111` |
| `Lorry Transport Rail Service` | `112` |
| `All Rail Services` | `113` |
| `Cross-Country Rail Service` | `114` |
| `Vehicle Transport Rail Service` | `115` |
| `Rack and Pinion Railway` | `116` |
| `Additional Rail Service` | `117` |
| `Coach Service` | `200` |
| `International Coach Service` | `201` |
| `National Coach Service` | `202` |
| `Shuttle Coach Service` | `203` |
| `Regional Coach Service` | `204` |
| `Special Coach Service` | `205` |
| `Sightseeing Coach Service` | `206` |
| `Tourist Coach Service` | `207` |
| `Commuter Coach Service` | `208` |
| `All Coach Services` | `209` |
| `Urban Railway Service` | `400` (or `403`, which Google's table also names "Urban Railway Service") |
| `Metro Service` | `401` |
| `Underground Service` | `402` |
| `All Urban Railway Services` | `404` |
| `Bus Service` | `700` |
| `Regional Bus Service` | `701` |
| `Express Bus Service` | `702` |
| `Stopping Bus Service` | `703` |
| `Local Bus Service` | `704` |
| `Night Bus Service` | `705` |
| `Post Bus Service` | `706` |
| `Special Needs Bus` | `707` |
| `Mobility Bus Service` | `708` |
| `Mobility Bus for Registered Disabled` | `709` |
| `Sightseeing Bus` | `710` |
| `Shuttle Bus` | `711` |
| `School Bus` | `712` |
| `School and Public Service Bus` | `713` |
| `Rail Replacement Bus Service` | `714` |
| `Demand and Response Bus Service` | `715` |
| `All Bus Services` | `716` |
| `Trolleybus Service` | `800` |
| `Tram Service` | `900` |
| `City Tram Service` | `901` |
| `Local Tram Service` | `902` |
| `Regional Tram Service` | `903` |
| `Sightseeing Tram Service` | `904` |
| `Shuttle Tram Service` | `905` |
| `All Tram Services` | `906` |
| `Water Transport Service` | `1000` |
| `Air Service` | `1100` |
| `Ferry Service` | `1200` |
| `Aerial Lift Service` | `1300` |
| `Telecabin Service` | `1301` |
| `Cable Car Service` | `1302` |
| `Elevator Service` | `1303` |
| `Chair Lift Service` | `1304` |
| `Drag Lift Service` | `1305` |
| `Small Telecabin Service` | `1306` |
| `All Telecabin Services` | `1307` |
| `Funicular Service` | `1400` |
| `Taxi Service` | `1500` |
| `Communal Taxi Service` | `1501` |
| `Water Taxi Service` | `1502` |
| `Rail Taxi Service` | `1503` |
| `Bike Taxi Service` | `1504` |
| `Licensed Taxi Service` | `1505` |
| `Private Hire Service Vehicle` | `1506` |
| `All Taxi Services` | `1507` |
| `Miscellaneous Service` | `1700` |
| `Horse-drawn Carriage` | `1702` |

### Duration fields renamed in `stop_visits`

Three fields holding durations are renamed with an explicit `_duration` suffix to distinguish them from timestamps:

| v1.0 field | v2.0 field |
|---|---|
| `kneel_deployed_time` | `kneel_deployed_duration` |
| `ramp_deployed_time` | `ramp_deployed_duration` |
| `lift_deployed_time` | `lift_deployed_duration` |

Field semantics are unchanged; only the names change.

### `operators` is now `crew`

The `operators` table is restructured into a `crew` table so that a crew member's role can change over time and so that the same person can be represented consistently across trips, vehicles, and train cars.

| v1.0 | v2.0 |
|---|---|
| `operators` table with a single `operator_id` field | `crew` table with `crew_id`, `crew_role`, `start_date`, and optional `end_date`; primary key `crew_id` + `start_date` |

The same `crew_id` may appear in more than one `crew` record when the role changes, with non-overlapping date ranges. `trips_performed`, `vehicle_train_cars`, and the new `vehicle_crew` table reference `crew.crew_id`.

To migrate:

- Rename `operators.csv` to `crew.csv` and update the resource entry in `datapackage.json`.
- Rename the `operator_id` column to `crew_id`, add `crew_role`, and add `start_date` (the earliest date the record applies; use the start of your dataset if unknown). Leave `end_date` empty for current records.
- Existing `trips_performed.operator_id` and `vehicle_train_cars.operator_id` values now resolve against `crew.crew_id`; the referring field names are unchanged.

### Vehicles and consists (in review, not part of v2.0-alpha.1)

A restructure of vehicle representation to support rail consists and mixed fleets (#272) is being worked through by the Standards Development Working Group with worked examples against real operational data. It is targeted for v2.0 final and is **not included in v2.0-alpha.1**. In alpha.1, the `vehicles`, `train_cars`, and `vehicle_train_cars` tables keep their v1.0 structure apart from the `vehicle_label` addition and the `crew` reference described above.

Producers implementing alpha.1 should expect the vehicles and consists area to change in v2.0 final; none of the changes in this guide depend on it beyond field references. This section will be replaced with migration steps when that work lands. Follow [#272](https://github.com/TIDES-transit/TIDES/pull/272) and the v2.0 map on [#271](https://github.com/TIDES-transit/TIDES/issues/271).

### `stop_visits.departure_load` may be negative

The `minimum: 0` constraint is removed. `departure_load` is typically derived from boardings and alightings rather than directly observed, and APC observation error can legitimately produce negative derived values, particularly at low loads.

**For producers:** negative values are valid and permitted. Document in your dataset metadata how negative values should be interpreted (for example, unadjusted derived values retained for aggregate accuracy). Nothing requires you to publish negative values; producers who adjust loads for internal consistency may continue to do so.

**For consumers:** do not assume `departure_load` is nonnegative. A negative value is a measurement artifact of the derived calculation, not a physical passenger count. For aggregate calculations (passenger miles, average loads), retaining negative values preserves statistical accuracy, since clamping them to zero introduces upward bias; for record-level display or operational reporting, treat interpretation per the producer's documentation.

## New optional capabilities

These additions are backwards-compatible; adopting them is optional.

- **`vehicle_crew` table:** supports multiple crew members per vehicle and trip, including mid-trip reliefs, with `crew_role` and start/end times. Records are keyed on `service_date`, `vehicle_id`, `crew_id`, and `start_time`; `trip_id_performed` is optional so that a single assignment can span consecutive trips (interlining), and is usually populated for easy joins. `trips_performed.operator_id` remains for the single-operator case.
- **`vehicle_label` field:** separates the user-visible vehicle number from the internal `vehicle_id`. Aligns with GTFS-realtime `VehicleDescriptor.label`.

A `device_status` table for tracking device availability was considered during v2.0 development and deferred to a future minor release pending implementation experience (see #253).

## Non-normative clarifications

- `event_count` usage and APC data guidance are clarified in the `device_events` table documentation. No data changes are required.

## Migration checklist for producers

- [ ] Rename `passenger_events.csv` to `device_events.csv`; rename `passenger_event_id` to `device_event_id`.
- [ ] Populate `device_id` on all device events and register devices in the `devices` table.
- [ ] Map enumeration values in the thirteen affected fields to their `snake_case` equivalents, and rename `stop_visits.door_status` to `door_action` with its shorter values.
- [ ] Write `trips_performed.route_type` as the GTFS numeric code (an integer) instead of the route type name.
- [ ] Switch `ntd_mode` to the two-character NTD mode codes; leave it empty for trips with no NTD mode.
- [ ] Rename the three `stop_visits` duration fields.
- [ ] Rename `operators.csv` to `crew.csv`; rename `operator_id` to `crew_id` and add `crew_role` and `start_date`.
- [ ] Leave `vehicles`, `train_cars`, and `vehicle_train_cars` as in v1.0 (plus optional `vehicle_label`); the vehicles and consists restructure follows in v2.0 final.
- [ ] Update `datapackage.json` resource entries and the profile reference to the v2.0 spec.
- [ ] Re-validate the data package against the v2.0 schemas.

## Migration checklist for consumers

- [ ] Update queries and joins from `passenger_events` to `device_events`; handle records where `vehicle_id` is empty (station and mobile device events).
- [ ] Update any string matching on the thirteen converted enumeration fields to the `snake_case` values, and read `stop_visits.door_action` in place of `door_status`.
- [ ] Expect `trips_performed.route_type` as an integer GTFS code rather than a route type name.
- [ ] Update any matching on `ntd_mode` to the two-character NTD mode codes, and expect it to be empty for trips with no NTD mode.
- [ ] Update references to the renamed `stop_visits` duration fields.
- [ ] Remove any assumption that `stop_visits.departure_load` is nonnegative; handle negative derived values per the producer's documented interpretation.
- [ ] Join `trips_performed.operator_id` and `vehicle_train_cars.operator_id` to `crew.crew_id` (with `start_date`/`end_date` if you need the role at the time); use `vehicle_crew` for full crew assignments.
- [ ] Expect the vehicles and consists tables to change in v2.0 final; no consumer change is needed for alpha.1.
