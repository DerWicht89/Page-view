import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def clean_data():
    # Filter out days when page views were in top 2.5% or bottom 2.5%
    df_filtered = df[(df['value'] >= df['value'].quantile(0.025)) & 
                     (df['value'] <= df['value'].quantile(0.975))]
    return df_filtered

def draw_line_plot():
    # Copy data to avoid modifying original
    df_line = df.copy()
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Plot the data
    ax.plot(df.index, df['value'], color='red')
    
    # Set title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Return the figure
    return fig

def draw_bar_plot():
    # Copy data to avoid modifying original
    df_bar = df.copy()
    
    # Extract year and month from date index
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # Calculate average page views grouped by year and month
    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Draw bar plot
    df_bar_grouped.plot(kind='bar', ax=ax)
    
    # Set labels
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # Set legend with month names
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(title='months of the year.', labels=month_names)
    
    # Return the figure
    return fig

def draw_box_plot():
    # Copy data to avoid modifying original
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    # Prepare data for box plots
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Create figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise box plot
    # Define month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    plt.setp(axes[1].get_xticklabels(), rotation=30)
    
    # Adjust layout
    plt.tight_layout()
    
    # Return the figure
    fig.savefig('box_plot.png')
    return fig

# Load data
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = clean_data()

# Draw line plot
line_plot = draw_line_plot()
line_plot.savefig('line_plot.png')

# Draw bar plot
bar_plot = draw_bar_plot()
bar_plot.savefig('bar_plot.png')

# Draw box plots
box_plots = draw_box_plot()
box_plots.savefig('box_plots.png')

plt.show()
