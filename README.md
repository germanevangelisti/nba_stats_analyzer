# NBA Stats Analyzer

Advanced NBA statistics analyzer and prediction system for the 2024-2025 season.

## Description

This project allows you to obtain, analyze, visualize, and predict NBA team statistics and game outcomes for the current season (2024-2025) using official NBA data. The system features a comprehensive statistical analysis model with weighted factors to provide accurate game predictions.

The project includes:
- Collection of basic and advanced statistics for all NBA teams
- Real-time game schedule data from the official NBA API
- Advanced prediction system with multi-factor analysis
- Interactive visualizations to analyze trends and patterns
- Team comparison tools with radar charts and statistical breakdowns
- Comprehensive game analysis with predictive models
- Interactive dashboard built with Dash and Plotly

## Key Features

### Advanced Game Prediction System
- Multi-factor analysis with 26 weighted statistics
- Predictions based on offensive efficiency, defensive metrics, rebounding, and victory factors
- Home court advantage integration (with dynamic adjustment based on team strength)
- Context-aware adjustments for playing style, shooting efficiency, and momentum
- Confidence level calculation for predictions

### Data Visualization
- Interactive radar charts for team comparisons
- Statistical correlation analysis
- Color-coded advantage indicators for all statistics
- Team-specific color schemes for all visualizations

### Game Calendar
- Real-time schedule data from the official NBA API
- Game predictions with probability percentages
- Comprehensive statistical breakdowns for each matchup
- Categorized analysis showing all factors influencing the prediction

### Team Analysis
- Detailed statistical profiles for all NBA teams
- Comparative analysis between any two teams
- Identification of strengths and weaknesses
- Performance trends across multiple statistical categories

## Requirements

- Python 3.9 or higher
- Required packages:
  - nba_api
  - pandas
  - matplotlib
  - seaborn
  - numpy
  - plotly
  - dash

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/nba_stats_analyzer.git
   cd nba_stats_analyzer
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Getting Team Statistics

To obtain basic statistics for all teams:

```
python main.py
```

This will generate a CSV file with basic statistics (`nba_team_stats_2024_25.csv`).

### Getting Advanced Team Metrics

To obtain advanced metrics for all teams:

```
python advanced_stats.py
```

This will generate CSV files with advanced metrics (`nba_team_advanced_metrics_2024_25.csv`) and a combined file with all statistics (`nba_team_complete_stats_2024_25.csv`).

### Generating Visualizations

To generate static visualizations of statistics:

```
python visualize_stats.py
```

This will create several visualizations in the `visualizations/` folder, including:
- Relationship between offensive and defensive ratings
- Top 10 teams by points per game
- Relationship between assists and wins
- Correlation heatmap between statistics
- Comparison of pace and offensive efficiency

### Interactive Dashboard

To run the interactive dashboard with dynamic visualizations and predictions:

```
python dashboard.py
```

The dashboard will be available at `http://127.0.0.1:8050/` and offers:
- Real-time updated charts
- Customized team analysis
- Visual comparison between teams
- Game predictions with comprehensive statistical breakdowns
- Interactive filters to customize analysis
- Exploration of correlations between metrics
- Game schedule with prediction probabilities

#### Dashboard Tabs

1. **Team Statistics**: View detailed statistics for any NBA team with radar charts
2. **Team Comparison**: Compare any two teams with side-by-side statistical analysis
3. **League Analysis**: Visualize league-wide trends and statistical correlations
4. **Schedule & Predictions**: View upcoming games with detailed matchup analysis and predictions

### Prediction System

The prediction system uses a sophisticated model that analyzes 26 different statistics across four main categories:

1. **Offense**:
   - Points per game
   - Offensive rating
   - Field goal percentage
   - Three-point percentage
   - Free throw percentage
   - Assists
   - Assist ratio
   - Field goals made
   - Three-pointers made

2. **Defense**:
   - Defensive rating
   - Steals
   - Blocks
   - Blocks received
   - Personal fouls

3. **Rebounds and Possessions**:
   - Total rebounds
   - Offensive rebounds
   - Defensive rebounds
   - Offensive rebound percentage
   - Defensive rebound percentage
   - Turnovers
   - Turnover percentage
   - Pace

4. **Victory Factors**:
   - Win percentage
   - Net rating
   - Plus/minus

Additionally, the system accounts for contextual factors:
- Home court advantage (with adjustment for significant team strength differences)
- Momentum (based on recent performance)
- Playing style compatibility (high-pace teams vs. low-pace teams)
- Shooting efficiency advantages

Each statistic is assigned a specific weight based on its importance for predicting game outcomes.

## Project Structure

- `main.py` - Obtains basic team statistics
- `advanced_stats.py` - Obtains advanced team metrics
- `visualize_stats.py` - Generates static visualizations
- `dashboard.py` - Interactive web dashboard with Dash and Plotly
- `application.py` - Main entry point for AWS Elastic Beanstalk deployment
- `requirements.txt` - Project dependencies
- `visualizations/` - Folder with generated visualizations
- `cache/` - Cache folder for NBA API data
- `*.csv` - CSV files with collected data
- `.ebextensions/` - Configuration files for Elastic Beanstalk
- `Procfile` - Process file for web deployment

## Deployment on AWS Elastic Beanstalk

This project is configured for deployment on AWS Elastic Beanstalk, which provides an optimal environment for Python web applications.

### Prerequisites

1. Install the AWS CLI:
   ```
   pip install awscli
   aws configure  # Configure with your AWS credentials
   ```

2. Install the Elastic Beanstalk CLI:
   ```
   pip install awsebcli
   ```

### Deployment Steps

1. **Create an Elastic Beanstalk application** (first time only):
   ```
   eb init -p python-3.9 nba-stats-analyzer
   ```
   - Follow the prompts to select your region and set up SSH (if needed)

2. **Create an environment** (first time only):
   ```
   eb create nba-stats-analyzer-env
   ```

3. **Deploy updates** (for subsequent deployments):
   ```
   eb deploy
   ```

4. **View the deployed application**:
   ```
   eb open
   ```

5. **Monitor the application**:
   ```
   eb logs          # View logs
   eb status        # Check environment status
   eb health        # Check environment health
   ```

### Configuration Files

- `.elasticbeanstalk/config.yml`: Main EB CLI configuration
- `.ebextensions/`: Contains configuration files for your environment
  - `01_packages.config`: System packages to install
  - `02_python.config`: Python-specific settings
  - `03_files.config`: File and directory setup
- `Procfile`: Specifies the command to start your application
- `application.py`: Main entry point for the application

### Environment Variables

You can set environment variables in the AWS Elastic Beanstalk console:
1. Go to your environment in the EB Console
2. Click on "Configuration"
3. Scroll to "Software" and click "Edit"
4. Add environment variables in the "Environment properties" section:
   - `DEBUG`: False (for production)
   - `PORT`: 8000 (matching Procfile configuration)

## Project Structure

- `main.py` - Obtains basic team statistics
- `advanced_stats.py` - Obtains advanced team metrics
- `visualize_stats.py` - Generates static visualizations
- `dashboard.py` - Interactive web dashboard with Dash and Plotly
- `application.py` - Main entry point for AWS Elastic Beanstalk deployment
- `requirements.txt` - Project dependencies
- `visualizations/` - Folder with generated visualizations
- `cache/` - Cache folder for NBA API data
- `*.csv` - CSV files with collected data
- `.ebextensions/` - Configuration files for Elastic Beanstalk
- `Procfile` - Process file for web deployment

## Acknowledgments

- [NBA API](https://github.com/swar/nba_api) - Library providing access to official NBA data
- [Plotly](https://plotly.com/) and [Dash](https://dash.plotly.com/) - Tools for creating interactive visualizations
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) - Deployment and hosting platform

## License

This project is licensed under the MIT License - see the LICENSE file for details. 