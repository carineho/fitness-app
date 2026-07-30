# Database Schema
### Activity
The schema uses a shared Activity table for common fields across all sports, with sports-specific details linked via foreign key.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| date | date | when the activity happened |
| sport_type | str | one of: climbing, running, yoga, diving, strength |
| notes | str, optional | free text remarks |


### ClimbSession
One row per climbing session, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| gym | str | gym / location name |


### Climb
One row per individual climb attempted within a session.
| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| climb_session_id | int, foreign key -> ClimbSession.id | links back to the parent session |
| grade_raw | str | grade as reported by the gym |
| grade_normalized | float, optional | grade converted to a shared numeric scale |
| attempts | int, optional | number of tries on this climb |
| sent | whether climb was successfully completed |


### RunDetail
One row per run, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| distance_km | float | distance covered |
| pace_min_per_km | float | average pace |


### YogaDetail
One row per yoga session, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| yoga_type | str | e.g., aerial, vinyasa |
| duration_minutes | int | session length |


### DiveDetail
One row per dive, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| dive_site | str | dive site name |
| duration_minutes | int | dive time |
| max_depth_m | float | maximum depth reached |


### StrengthSession
One row per strength / general workout session, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| body_area | str | e.g., arms, core, legs |


### Exercise
One row per individual exercise performed within a session

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| strength_session_id | int, foreign key -> StrengthSession.id | links back to parent session |
| exercise_name | str | e,g., bench press, plank |
| exercise_type | str | "reps" or "time" |
| sets | int, optional | number of sets |
| reps | int, optional | reps per set (for rep-based exercises) |
| weight_kg | float, optional | weight used (for rep-based exercises) |
| duration_seconds | int, optional | duration held / performed (for time-based exercises) |


### GradingSystem
Lookup table for converting each gym's raw grade into a shared normalize scale, so climbing progress is comparable across gyms with different grading systems.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| gym | str | gym / location name |
| raw_grade | str | grade as the gym labels it |
| normalized_value | float | corresponding value on shared internal scale |