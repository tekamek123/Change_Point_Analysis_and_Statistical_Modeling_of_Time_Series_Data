# Task 1: Analysis Workflow and Foundation Document

## Data Analysis Workflow

### Phase 1: Data Preparation and Exploration
1. **Data Loading and Initial Inspection**
   - Load Brent oil price data (1987-2022)
   - Check data quality, missing values, and format consistency
   - Convert date formats to standardized datetime objects

2. **Exploratory Data Analysis (EDA)**
   - Visualize price trends over time
   - Calculate basic statistics (mean, variance, min/max)
   - Identify obvious outliers and data anomalies

3. **Time Series Properties Analysis**
   - **Trend Analysis**: Decompose time series into trend, seasonal, and residual components
   - **Stationarity Testing**: Apply ADF test, KPSS test to determine stationarity
   - **Volatility Patterns**: Analyze price volatility clusters and heteroscedasticity
   - **Autocorrelation Analysis**: Examine ACF/PACF plots to understand temporal dependencies

### Phase 2: Event Data Compilation and Integration
1. **Historical Event Research**
   - Compile major geopolitical events affecting oil markets
   - Document OPEC decisions and production changes
   - Identify economic sanctions and conflicts in oil-producing regions
   - Record financial crises and economic shocks

2. **Event Dataset Creation**
   - Structure event data with dates, descriptions, and event types
   - Categorize events (political, economic, supply/demand, etc.)
   - Assign severity scores where possible

3. **Data Integration**
   - Merge event data with price data
   - Create binary indicators for event periods
   - Align temporal scales for analysis

### Phase 3: Bayesian Change Point Modeling
1. **Model Selection and Design**
   - Choose appropriate Bayesian change point model structure
   - Define prior distributions for model parameters
   - Specify likelihood functions based on data properties

2. **Model Implementation**
   - Implement Bayesian change point detection using PyMC
   - Set up MCMC sampling with appropriate parameters
   - Conduct model convergence diagnostics

3. **Change Point Detection**
   - Run Bayesian inference to identify structural breaks
   - Extract posterior distributions of change point locations
   - Quantify uncertainty in change point estimates

### Phase 4: Analysis and Interpretation
1. **Event-Change Point Correlation**
   - Map detected change points to historical events
   - Calculate temporal proximity metrics
   - Assess statistical significance of correlations

2. **Impact Quantification**
   - Estimate magnitude of price changes around change points
   - Compare pre/post event price dynamics
   - Analyze duration of effects

3. **Validation and Sensitivity**
   - Perform robustness checks with different model specifications
   - Test sensitivity to prior choices
   - Validate findings against historical records

### Phase 5: Communication and Visualization
1. **Dashboard Development**
   - Create interactive visualizations of price trends
   - Display change points with event annotations
   - Provide filters for time periods and event types

2. **Report Generation**
   - Summarize key findings and insights
   - Provide actionable recommendations for stakeholders
   - Document methodology and limitations

## Understanding the Model and Data

### Time Series Properties and Modeling Implications

#### Trend Analysis
- **Expected Pattern**: Long-term upward trend with cyclical fluctuations
- **Modeling Impact**: Need to detrend data or include trend components in the model
- **Approach**: Use decomposition methods to separate trend from cyclical components

#### Stationarity Testing
- **Hypothesis**: Brent oil prices likely non-stationary (unit root present)
- **Implications**: 
  - Non-stationary series require differencing or trend modeling
  - Change point models can handle non-stationarity by identifying regime shifts
- **Testing Methods**: Augmented Dickey-Fuller (ADF), KPSS tests

#### Volatility Patterns
- **Expected Characteristics**: 
  - Volatility clustering during crisis periods
  - Heteroscedastic variance over time
- **Modeling Considerations**:
  - May need GARCH-type models for volatility
  - Bayesian models can incorporate changing variance parameters

### Change Point Models in Oil Price Analysis

#### Purpose and Benefits
1. **Structural Break Detection**: Identify sudden changes in price dynamics
2. **Regime Identification**: Separate different market regimes (crisis vs. stable periods)
3. **Event Attribution**: Link statistical changes to real-world events
4. **Risk Management**: Help identify periods of increased uncertainty

#### Model Structure
- **Bayesian Approach**: Provides uncertainty quantification for change point locations
- **Flexible Framework**: Can model changes in mean, variance, and trend parameters
- **Prior Information**: Incorporate knowledge about likely event periods

#### Expected Outputs
1. **Change Point Dates**: Probabilistic estimates of when structural changes occurred
2. **Parameter Estimates**: Pre and post-change point model parameters
3. **Uncertainty Measures**: Credible intervals for change point locations
4. **Event Probabilities**: Likelihood of specific events causing detected changes

#### Limitations
1. **Correlation vs. Causation**: Statistical association doesn't prove causation
2. **Temporal Ambiguity**: Difficulty determining exact timing of effects
3. **Confounding Events**: Multiple simultaneous events complicate attribution
4. **Model Dependence**: Results sensitive to model specification and priors

## Assumptions and Limitations

### Key Assumptions
1. **Data Quality**: Historical price data is accurate and representative
2. **Event Coverage**: Major events affecting oil prices are identified and documented
3. **Temporal Alignment**: Event dates correspond to market impact periods
4. **Model Appropriateness**: Bayesian change point models are suitable for this analysis
5. **Market Efficiency**: Price changes reflect available information about events

### Critical Limitations
1. **Correlation-Causation Gap**:
   - Statistical correlation in time doesn't prove causal impact
   - Multiple factors may simultaneously influence prices
   - Lag effects may create temporal misalignment

2. **Data Limitations**:
   - Daily data may miss intraday volatility patterns
   - Historical event data may be incomplete or biased
   - Quality of early data (1980s) may be lower than recent data

3. **Model Constraints**:
   - Change point models assume discrete regime shifts
   - May miss gradual transitions or continuous changes
   - Sensitive to prior specifications and hyperparameters

4. **Event Attribution Challenges**:
   - Global events have complex, interconnected effects
   - OPEC decisions may be responses to market conditions rather than causes
   - Sanctions and conflicts may have delayed or prolonged effects

### Communication Strategy

#### Stakeholder Channels
1. **Executive Leadership**: Quarterly briefings with key insights and strategic implications
2. **Investment Teams**: Monthly detailed analysis reports with specific recommendations
3. **Policy Advisors**: Policy impact assessments and regulatory implications
4. **Technical Teams**: Methodology documentation and model validation reports

#### Communication Formats
1. **Interactive Dashboard**: Real-time visualization of trends and change points
2. **Executive Summary**: 1-page briefings with key findings and action items
3. **Technical Reports**: Detailed methodology and statistical analysis
4. **Alert System**: Real-time notifications of significant market changes

#### Success Metrics
1. **Decision Support**: Analysis directly influences investment or policy decisions
2. **Timeliness**: Insights delivered within actionable timeframes
3. **Accuracy**: Change point predictions align with historical events
4. **Comprehensibility**: Non-technical stakeholders can understand key insights

---

**Document Version**: 1.0  
**Date**: February 2026  
**Author**: Data Science Team, Birhan Energies
