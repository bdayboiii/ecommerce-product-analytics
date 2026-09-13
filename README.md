# E-commerce Product Analytics & Experimentation

## Overview

An end-to-end product analytics project focused on identifying
e-commerce conversion friction, developing a product hypothesis,
prototyping the proposed intervention, and evaluating it through A/B
testing.

The project follows a product-management workflow:

**User behavior → Funnel analysis → Problem identification → Product
hypothesis → Prototype → Experiment → Product recommendation**

------------------------------------------------------------------------

## Problem Statement

E-commerce platforms need to understand where users drop off during the
journey from discovering a product to completing a purchase.

This project investigates:

-   Where users drop off in the conversion funnel
-   Whether new and existing users behave differently
-   Whether product price is associated with conversion behavior
-   A potential product intervention for new users
-   Whether the proposed intervention improves view-to-cart conversion

------------------------------------------------------------------------

## Dataset

A **synthetic e-commerce dataset** was generated to simulate realistic
user behavior.

The database contains:

-   **1,003 users**
-   **203 products**
-   **10,000 sessions**
-   **27,939 events**
-   **4,887 orders**

### Main event types

-   `view`
-   `add_to_cart`
-   `checkout`
-   `purchase`

The synthetic data was generated using documented behavioral
assumptions, including lower conversion tendencies among new users and
for higher-priced products.

> **Note:** The dataset is synthetic and does not represent real
> customer or company data.

------------------------------------------------------------------------

## Tech Stack

-   PostgreSQL
-   SQL
-   Python
-   Pandas
-   Matplotlib
-   SciPy
-   Figma

------------------------------------------------------------------------

## Analysis

### 1. Conversion Funnel

The overall funnel was analyzed across four stages:

**View → Add to Cart → Checkout → Purchase**

This established the overall conversion baseline and provided a starting
point for identifying potential friction.

### 2. New vs Existing Users

Users were segmented based on time since signup.

The analysis showed a substantial difference in view-to-cart conversion:

  User Type     View-to-Cart Conversion
  ----------- -------------------------
  Existing                        \~73%
  New                             \~44%

This indicated that the primary friction was concentrated among new
users.

### 3. Price Segmentation

Products were grouped into:

-   **Low:** \< ₹2,000
-   **Medium:** ₹2,000--₹3,999
-   **High:** ₹4,000+

For high-priced products:

  User Type     View-to-Cart Conversion
  ----------- -------------------------
  Existing                       69.62%
  New                            38.27%

This represents a **31.35 percentage-point gap** between new and
existing users.

------------------------------------------------------------------------

## Product Hypothesis

### Problem

New users are substantially less likely to add a product to their cart
after viewing it. The difference is particularly large for higher-priced
products.

### Hypothesis

New users may lack sufficient confidence to commit to a product after
viewing it, particularly when considering higher-priced products.

### Proposed Intervention

Add concise purchase-confidence signals to the product page:

-   Ratings and review count
-   Easy-return information
-   Expected delivery information
-   Trusted-seller information

The intervention was designed as a lightweight product-page change
rather than a complete redesign.

------------------------------------------------------------------------

## Product Prototype

A low-fidelity product-page prototype was created with separate
**control** and **treatment** variants.

**[View Figma
Prototype](https://www.figma.com/design/jipFAdrKBgJhlzJQYyc9va/E-commerce-Product-Analytics---Experimentation)**

### Control

Standard product page containing product information, rating, price,
size selection, and add-to-bag functionality.

### Treatment

The same product page with additional purchase-confidence signals:

-   Review information
-   Easy-return information
-   Delivery information
-   Trusted-seller information

The prototype demonstrates how the analytical finding was translated
into a product hypothesis and a testable intervention.

------------------------------------------------------------------------

## A/B Experiment

### Target Population

New users viewing products priced at ₹4,000 or more.

### Experiment Groups

**Control:** Existing product-page experience.

**Treatment:** Existing product page with additional purchase-confidence
signals.

### Primary KPI

**View-to-cart conversion rate**

------------------------------------------------------------------------

## Experiment Results

  Group         Sessions   Cart Sessions   Conversion
  ----------- ---------- --------------- ------------
  Control            120              39       32.50%
  Treatment          123              54       43.90%

### Observed Impact

-   **Absolute lift:** +11.40 percentage points
-   **Relative lift:** +35.08%

A two-proportion z-test was used to evaluate statistical significance.

The experiment produced a p-value of approximately **0.0675**.

Since this is above the 5% significance threshold, the observed
improvement is **not statistically significant at α = 0.05**.

### Product Recommendation

The treatment shows a promising directional improvement, but the
evidence is not strong enough to recommend an immediate full rollout.

A larger experiment should be run to increase statistical power and
determine whether the observed effect persists. Checkout and purchase
conversion should also be monitored to ensure that improvements in
view-to-cart conversion translate into downstream business impact.

------------------------------------------------------------------------

## Limitations

-   The dataset is synthetic and does not represent real customer
    behavior.
-   The experiment was simulated using a predefined treatment-effect
    assumption.
-   The A/B test sample size is small, resulting in an inconclusive
    statistical result.
-   The proposed confidence signals are hypotheses and would require
    validation with real user research and production experimentation.
-   The analysis focuses primarily on view-to-cart conversion;
    downstream metrics should be evaluated before making a final product
    decision.

------------------------------------------------------------------------

## Project Structure

``` text
ecommerce-product-analytics/
│
├── analysis/
│   ├── funnel_analysis.sql
│   └── ab_test.sql
│
├── database/
│   └── schema.sql
│
├── notebook/
│   └── analysis.ipynb
│
├── scripts/
│   └── generate_data.py
│
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

## Key Takeaway

The analysis identified **new users viewing high-priced products** as a
high-friction segment. A lightweight product-page intervention focused
on purchase confidence produced a promising but statistically
inconclusive improvement in view-to-cart conversion.

The project demonstrates an end-to-end product analytics workflow:

**Identify friction → Form a hypothesis → Prototype a solution → Run an
experiment → Evaluate the evidence → Make a product recommendation**
