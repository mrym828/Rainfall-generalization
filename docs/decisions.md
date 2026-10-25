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

**Decision:** A station-month must contain at least 28 valid daily precipitation observations for its monthly rainfall total to be considered a valid target.

Station-months that do not meet this requirement will have their monthly precipitation targets set to NaN, rather than zero. The station-month records will be preserved, and other meteorological features may still be used if they satisfy their respective quality requirements.

The 28-day threshold remains the provisional primary criterion until further sensitivity experiments are completed.


**Reason:** Missing daily precipitation observations may cause the recorded monthly precipitation total to underestimate the actual rainfall amount, particularly when rainfall is concentrated in a small number of days.

The 28-day threshold was selected as an initial quality-control criterion to reduce the risk of unreliable rainfall targets. However, meeting this threshold does not guarantee that the monthly precipitation total is accurate.

**Evidence:** Daily precipitation completeness was assessed across six UAE weather stations from January 1996 to December 2023, representing 2,016 expected station-month combinations.

The analysis was conducted after replacing NOAA precipitation missing-value codes with NaN and reconstructing the complete station-month calendar.

The following results were obtained:

| Completeness criterion | Accepted months | Rejected months | Retention |
|--------------|--------| --------- | -------- | 
| ≥25 valid days | 1,992 | 24 | 98.81% |
|≥28 valid days | 1,889 | 127 | 93.70% |
| ≥30 valid days | 1,579 | 437 | 78.32% |
| ≥90% monthly completeness | 1,941 |75 | 96.28% |

Under the primary 28-day criterion, 127 station-months (6.30%) did not satisfy the completeness requirement.

The complete calendar also identified January 2006 at Ras Al Khaimah as an entirely missing station-month, which was absent from the original monthly grouping.

**Notes:**
- The number of calendar days varies across months.

- February contains 28 days in a regular year and 29 days in a leap year.

- Under the fixed 28-day threshold, a regular February requires all 28 observations, whereas a leap-year February may have one missing observation.

- A month with insufficient precipitation observations must not automatically be interpreted as having zero rainfall.

- The complete station-month calendar must be preserved to ensure correct chronological alignment when constructing next-month rainfall targets.

- Missing precipitation targets do not automatically require the removal of other valid meteorological predictors.

**Applied in:** 

The completeness criteria have been investigated and validated in notebooks/01_data_inspection. ipynb.

Application of the selected threshold to monthly precipitation totals is planned for the monthly aggregation implementation.

### D3 — Completeness Threshold Sensitivity Assessment

**Alternative Criterion:**

A relative completeness threshold of at least 90% was investigated to account for differences in calendar-month lengths.

Relative monthly precipitation completeness was calculated as:


$$ Completeness (\%) = valid PRCP days/calendar days in month*100$$

**Results:**

The 90% criterion accepted 1,941 station-months (96.28%), compared with 1,889 station-months (93.70%) under the fixed 28-day criterion.

Therefore, the relative criterion accepted 52 additional station-months, increasing retention by approximately 2.58 percentage points.

Validation confirmed that no station-month accepted by the 28-day criterion was rejected by the 90% criterion.

**Interpretation:**

The percentage-based criterion accounts for differences in month lengths and may provide a more consistent measure of relative completeness.

For example, February 1996 contained 27 valid precipitation observations out of 29 calendar days, giving a completeness rate of approximately 93.10%. This month is rejected by the fixed 28-day criterion but accepted by the 90% criterion.

However, retaining additional station-months does not necessarily improve rainfall target reliability. Missing daily observations may include rainfall events, causing monthly precipitation totals to be underestimated.

**Research Decision:**

The fixed 28-day criterion will remain the provisional primary threshold.

The 90% relative completeness criterion will be retained as an alternative for sensitivity analysis.

Both criteria will be evaluated using Leave-One-Station-Out (LOSO) cross-validation, with consistent model configurations and comparable, reliable evaluation targets.

The final threshold will be selected based on data quality considerations and cross-station prediction performance, rather than data retention alone.

## D6: Sea-level pressure (SLP) as a predictor

**Decision:** Retain SLP in cleaned data for documentation, but omit it from the main forecasting features. 

**Evidence (daily NOAA GSOD, 1996–2023):**
- Overall missing SLP: 17.147%.
- Fujairah: 44.631% missing; 100% missing in 1996–2003 and 2022 (nine full years).
- Al Ain: 22.557% missing; 100% missing in 2001–2003.
- Dubai: 12.852%; RAK: 8.198%; Sharjah: 8.123%; Abu Dhabi: 6.605%.

**Rationale:** SLP is meteorologically relevant, but long and uneven station-specific gaps would require extensive imputation and could distort the cross-station generalization comparison. Exclusion is a data-quality decision, not a claim that pressure is unimportant for rainfall.

## D7 : Precipitation Quality Control

