# Summarizing the Momentum Model to Be used
- *Simple/Generic momentum:* calculate the **total return (including dividends)** of a stock over some particular **look-back period** (e.g., the past 12 months) (See Table 5.1 )
  - Get monthly Gross Returns by adding 1 to net return per month
  - Multiply all month sums (AKA Gross Return Series) by eachother and subtract 1
  - The result is the *cumulative 12-month return*
  - *Exclude the most recent month, for some reason...*
    - The reason is because it performs better this way, per the calculations of the authors. So... it's actually an 11-month return that we're calculating... From 1 year ago to 1 motnh ago
      - (Note that when calculating ID, below, we also use 11 months of data?)
    
- Although we can calculate short, long, and intermediate-term momentum, **the recommendation of the book is to use intermediate-term** (12 month look back)
  - The conclusion is that momentum performs in a 3-12  month time horizon
    - **Buy based on 12 months of performance and hold for 3 months**
    

- To improve generic formula -- *focus on the time-series characteristics* of a momentum stock
  - Smoother stocks peform better
    - Calculation:
      - Compute % of days with positive return relative to % of days with negative return
      - Smoother momentum = higher % of positive days, relatively

  - Limited attention
    - "if a stock gradually grinds along and achieves a 100 percent return (i.e., the water slowly heats up over time), investors will pay less attention to the gradual stock price movement and the security will likely be priced at less than fundamental value."
    - *A series of frequent gradual changes attracts less attention than infrequent dramatic changes. Investors therefore underreact to continuous information.*
      - So attempt to *optimize path-dependancy of momentum*
      -Since momentum anomaly is driven by an underreaction to marginally positive news.

  - ID (Information Discreteness) Calculation: ID = sign(Past Return) * [%negative - %positive]
    - Small ID --> continous information of small changes

- To combine momentum and ID one first calculates a list of top X momentum stocks and then from there sorts this list by ID and picks the top Y stocks in this ID-sorted list of high-momentum stocks


# Pseudocode
1. Get a list of S&P stocks? OR Russel 1000?
2. Generate a table of S&P/Russel1k Stocks sorted by 12-month GMS
   - GMS should be calculated for each by:
        1. Getting all monthly returns (as a coefficient between -1 and 1) and adding +1
        2. Multiplying all monthly returns from (2.1) together and subtracting 1
        3. The result is still a coefficient percentage between -1 and 1
3. Create a slice of this table with only the top 50 (??) momentum stocks
   1. Calculate ID for each in this list of 50 with the following formula: 
      - ID = sign(Past Return) * [%negative - %positive]

   2. Sort this slice by ID
4. Output a slice of the top 25 of these


 