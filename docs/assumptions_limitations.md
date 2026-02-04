# Assumptions and Limitations Document

## Critical Distinction: Correlation vs. Causation

### The Fundamental Challenge
The most critical limitation in this analysis is the distinction between **statistical correlation in time** and **proven causal impact**. While our Bayesian change point models can identify when structural changes occur in oil price dynamics, establishing definitive causation requires additional evidence beyond temporal correlation.

### Why Correlation ≠ Causation in Oil Markets

#### 1. **Multiple Concurrent Factors**
- Oil prices respond to numerous simultaneous influences
- Political events often coincide with economic changes
- Supply disruptions may trigger policy responses

#### 2. **Temporal Complexity**
- Effects may be immediate or delayed
- Some events have prolonged, gradual impacts
- Market anticipation can cause pre-emptive price movements

#### 3. **Bidirectional Relationships**
- Oil prices can influence political decisions
- Economic conditions affect both events and market responses
- Feedback loops create complex dynamics

### Establishing Causal Claims: Requirements
To move from correlation to causation, we would need:
1. **Temporal Precedence**: Clear evidence that event preceded price change
2. **Mechanistic Understanding**: Plausible economic/political mechanism
3. **Counterfactual Analysis**: What would have happened without the event
4. **Exclusion of Alternatives**: Ruling out other potential causes

## Core Assumptions

### Data Quality Assumptions
1. **Price Data Accuracy**
   - Historical Brent prices are accurate and reliable
   - Daily closing prices represent true market value
   - No significant data gaps or reporting errors

2. **Event Data Completeness**
   - Major oil-affecting events are identified and documented
   - Event dates are accurate and meaningful
   - Event descriptions capture the essential market impact

3. **Temporal Alignment**
   - Event dates correspond to actual market impact timing
   - Time zone differences are properly handled
   - Weekend/holiday effects are accounted for

### Modeling Assumptions
1. **Change Point Model Appropriateness**
   - Oil price dynamics exhibit discrete regime shifts
   - Bayesian framework captures uncertainty adequately
   - Prior distributions are reasonable and not overly influential

2. **Market Behavior**
   - Market participants respond rationally to new information
   - Price changes reflect all available information (semi-strong efficiency)
   - Historical patterns provide insight into future behavior

3. **Event Impact Structure**
   - Events cause identifiable structural changes in price dynamics
   - Impact magnitude is measurable and consistent
   - Effects are not completely masked by other factors

### Economic Assumptions
1. **Supply-Demand Dynamics**
   - Oil markets primarily driven by supply and demand fundamentals
   - Geopolitical events affect these fundamentals in predictable ways
   - Market adjustments follow economic theory

2. **Global Integration**
   - Oil markets are globally integrated and efficient
   - Regional events have global market implications
   - Arbitrage opportunities are quickly eliminated

## Major Limitations

### Methodological Limitations

#### 1. **Change Point Detection Constraints**
- **Discrete vs. Continuous Changes**: Models assume abrupt changes, missing gradual transitions
- **Parameter Stability**: Assumes parameters remain constant between change points
- **Detection Sensitivity**: May miss small but meaningful changes or detect spurious ones

#### 2. **Bayesian Model Limitations**
- **Prior Dependence**: Results can be sensitive to prior distribution choices
- **Computational Complexity**: MCMC sampling may not fully explore parameter space
- **Model Specification**: Wrong model structure can lead to misleading results

#### 3. **Time Series Analysis Challenges**
- **Non-Stationarity**: Oil prices exhibit complex non-stationary behavior
- **Volatility Clustering**: Standard models may not capture volatility dynamics adequately
- **Structural Breaks**: Multiple breaks can complicate analysis and interpretation

### Data Limitations

#### 1. **Historical Data Quality**
- **Early Period Reliability**: 1987-1990s data may be less accurate than recent data
- **Reporting Standards**: Data collection methods have changed over time
- **Missing Data**: Potential gaps in historical records

#### 2. **Event Data Challenges**
- **Subjectivity**: Event importance and impact assessment involve judgment
- **Incomplete Coverage**: Some events may be missed or underreported
- **Timing Ambiguity**: Exact impact timing may be unclear

#### 3. **Temporal Resolution**
- **Daily Data Limitations**: May miss intraday volatility and price movements
- **Weekend Effects**: Weekend events may not be reflected until Monday
- **Holiday Effects**: Market closures can delay price discovery

### Interpretation Limitations

#### 1. **Attribution Challenges**
- **Multiple Causes**: Price changes often result from multiple simultaneous factors
- **Confounding Variables**: Difficult to isolate individual event impacts
- **Interaction Effects**: Events may interact in complex, non-linear ways

#### 2. **Generalization Issues**
- **Historical Specificity**: Past relationships may not hold in future
- **Regime Changes**: Market structure evolves over time
- **Context Dependence**: Event impacts depend on specific market conditions

#### 3. **Prediction Limitations**
- **Model Uncertainty**: Statistical models have inherent prediction uncertainty
- **Black Swan Events**: Unprecedented events may not follow historical patterns
- **Market Evolution**: Future market dynamics may differ from historical behavior

## Mitigation Strategies

### Methodological Approaches
1. **Robustness Testing**: Use multiple model specifications and prior choices
2. **Cross-Validation**: Validate findings on different time periods
3. **Sensitivity Analysis**: Test assumptions and parameter choices
4. **Ensemble Methods**: Combine multiple approaches for more reliable results

### Data Quality Improvements
1. **Data Validation**: Cross-check price data with multiple sources
2. **Event Verification**: Validate event dates and descriptions with historical records
3. **Quality Metrics**: Assess and report data quality indicators
4. **Missing Data Handling**: Implement appropriate methods for gaps

### Interpretation Safeguards
1. **Confidence Intervals**: Report uncertainty in all estimates
2. **Alternative Explanations**: Consider and discuss competing hypotheses
3. **Expert Review**: Consult domain experts for validation
4. **Transparency**: Clearly document all assumptions and limitations

## Communication of Limitations

### To Stakeholders
1. **Executive Summary**: Clear, non-technical explanation of key limitations
2. **Technical Appendix**: Detailed documentation for technical audiences
3. **Uncertainty Quantification**: Explicit reporting of confidence levels
4. **Caveat Language**: Appropriate caution in conclusions and recommendations

### In Deliverables
1. **Dashboard Warnings**: Clear indicators of uncertainty in visualizations
2. **Report Disclaimers**: Explicit statements about limitations
3. **Methodology Documentation**: Complete technical documentation
4. **Validation Reports**: Results of robustness and sensitivity testing

---

**Document Version**: 1.0  
**Date**: February 2026  
**Author**: Data Science Team, Birhan Energies  
**Review Status**: Draft - Pending Technical Review
