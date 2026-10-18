# Decisions

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