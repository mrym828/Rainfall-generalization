# Decisions

## D1 : Use recent local rainfall as a feature?

**Decision:** Build two feature sets and compare them.
- Set A: no rainfall history (weather of month t, month-of-year, ..).
- Set B: Set A plus rainfall of recent months at the same station.

**Reason:** Set B tests "a station left out of training that still has a working rain gauge". Set A tests "a station without local rainfall history". They answer different questions, so both are reported separately.

**Rules:**
- Same held-out stations and same test months for both sets.
- Never use 0 to stand for "no measurement".
- Data of the held-out station is not used for training, tuning, or preprocessing.

**Location features (latitude, longitude, elevation):**
Excluded from the main comparison of Set A and Set B. With only 5 training
stations they can act as a station identifier, so the model may memorise
station-level rainfall instead of learning weather-rainfall relations.
They are kept in the stations table and used in the analysis of results.
If time allows, one extra experiment adds them, with the same models and test
months. If they enter the final model, the choice is made with an inner
leave-one-station-out evaluation on the training stations only, never using the
held-out station.

## D3: Minimum valid rainfall days per month

**Decision:** A station-month is kept only if it has at least 28 days with valid PRCP (non-NaN) value. Otherwise its monthly rainfall is set to NaN.

**Reason:** Missing days make the monthly rainfall total lower than the true value, so a month with many missing days would teach the models wrong targets. A month with 28 or more valid days is close enough to complete to trust.

**Evidence:** Counted valid PRCP days for every station-month (6 stations x 336 months = 2016).
- Threshold 28: 23 station-months lost (1.1%).
- Threshold 25: 9 lost. Threshold 20: 3 lost.
- The 23 lost at threshold 28 are 22 months with fewer than 28 valid days and 1 month with no rows at all (Ras Al Khaimah, January 2006).

**Notes:**
- February needs all of its days (28 or 29), because the limit is fixed at 28.
- Ras Al Khaimah has a gap of about 69 days from December 2005 to mid-February 2006, during the rainy season.
- The monthly table must contain every month for every station, with NaN where a month is missing, so that the "next month" shift works by calendar date.

**Applied in:** monthly aggregation, after replacing PRCP missing codes with NaN.


## D6: Sea-level pressure (SLP) as a predictor

**Decision:** Retain SLP in cleaned data for documentation, but omit it from the main forecasting features. 

**Evidence (daily NOAA GSOD, 1996–2023):**
- Overall missing SLP: 17.147%.
- Fujairah: 44.631% missing; 100% missing in 1996–2003 and 2022 (nine full years).
- Al Ain: 22.557% missing; 100% missing in 2001–2003.
- Dubai: 12.852%; RAK: 8.198%; Sharjah: 8.123%; Abu Dhabi: 6.605%.

**Rationale:** SLP is meteorologically relevant, but long and uneven station-specific gaps would require extensive imputation and could distort the cross-station generalization comparison. Exclusion is a data-quality decision, not a claim that pressure is unimportant for rainfall.