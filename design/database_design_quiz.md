# Database Design Quiz - Option Pricing Application
*Based on Robert Bjork's Learning and Forgetting Lab Principles*

## Instructions
These questions are designed to deepen your understanding through active recall, desirable difficulties, and spaced retrieval practice. Take time to think through each question before looking at the answer.

---

**Question 1:** Why was PostgreSQL chosen over NoSQL for this option pricing application?
a) Better scalability for high-volume trading
b) Superior performance for real-time pricing
c) ACID compliance and structured financial data requirements
d) Lower licensing costs

**Answer:** c) ACID compliance and structured financial data requirements

---

**Question 2:** What is the primary key data type used across all tables in this schema?
a) SERIAL
b) INTEGER
c) UUID
d) VARCHAR

**Answer:** c) UUID


**Question 4:** How many daily requests does the system need to handle according to the load analysis?
a) 100 requests
b) 250 requests
c) 2,000 requests
d) 4,000 requests

**Answer:** c) 2,000 requests

---

**Question 5:** In the pricing_requests table, which fields store the calculated option prices?
a) volatility, time_to_expiry, tail_index_alpha
b) bsm_price, pareto_price, market_reference_price
c) anchor_strike, anchor_price
d) pareto_vs_bsm_diff, market_vs_bsm_diff

**Answer:** b) bsm_price, pareto_price, market_reference_price

---

**Question 6:** What ensures uniqueness in the option_contracts table?
a) contract_id only
b) symbol and strike_price only
c) symbol, strike_price, expiration_date, and option_type
d) expiration_date and option_type only

**Answer:** c) symbol, strike_price, expiration_date, and option_type

---

**Question 7:** Which index would be most critical for trader performance queries?
a) idx_market_data_symbol_date
b) idx_pricing_requests_trader_id
c) idx_option_contracts_symbol
d) idx_user_sessions_start

**Answer:** b) idx_pricing_requests_trader_id

---

**Question 8:** In the data retention policy, how long are pricing requests kept in the main table?
a) 6 months
b) 1 year
c) 2 years
d) Indefinitely

**Answer:** b) 1 year

---

**Question 9:** What decimal precision is used for strike_price in option_contracts?
a) DECIMAL(6,4)
b) DECIMAL(8,6)
c) DECIMAL(10,2)
d) DECIMAL(10,4)

**Answer:** c) DECIMAL(10,2)

---



---

**Question 11:** What is the expected peak load during market hours?
a) ~4 requests/minute
b) ~10 requests/minute
c) ~50 requests/minute
d) ~250 requests/minute

**Answer:** a) ~4 requests/minute

---

**Question 12:** In the NoSQL alternative, how would option details be stored?
a) As separate documents with references
b) As embedded subdocuments within pricing requests
c) In a denormalized flat structure
d) As binary encoded data

**Answer:** b) As embedded subdocuments within pricing requests



**Question 14:** What database feature is recommended for handling old pricing data?
a) Sharding
b) Replication
c) Partitioning by date
d) Indexing optimization

**Answer:** c) Partitioning by date


**Question 17:** How is time-based uniqueness handled in market_data?
a) Single timestamp field
b) Unique constraint on symbol and data_date
c) Separate version number field
d) Composite key with multiple time fields

**Answer:** b) Unique constraint on symbol and data_date
