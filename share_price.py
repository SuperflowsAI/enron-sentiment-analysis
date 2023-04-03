import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import imageio
import os

# Read historical stock price data
stock_data = pd.read_csv('data/enron_stockprice/ENRON_stock_prices.csv')
stock_data['Date'] = pd.to_datetime(stock_data['date'])
stock_data = stock_data.set_index('Date')

# Define the date range of the Enron email dataset
start_date = '1998-05-01'
end_date = '2001-12-31'

# Filter the stock data to the date range
filtered_stock_data = stock_data.loc[start_date:end_date]

# Plot the rolling plot and save the frames
frames = []
output_directory = 'plots/enron_stockprice/frames'
os.makedirs(output_directory, exist_ok=True)

for idx, row in filtered_stock_data.iterrows():
    fig, ax = plt.subplots()
    ax.plot(filtered_stock_data.loc[:idx, 'close'], label='Close Price')

    # Add fill color under the rolling stock price
    ax.fill_between(filtered_stock_data.loc[:idx].index, 0, filtered_stock_data.loc[:idx, 'close'], alpha=0.3,
                    label='Close Price Fill')

    # Format plot
    ax.set_title(f'Enron Share Price - {idx.date()}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_ylim(0,95)

    ax.set_yticks([0, 40, 80])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)

    ax.tick_params(axis=u'both', which=u'both', length=0)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xticks(rotation=45)

    frame_path = os.path.join(output_directory, f'{idx.date()}.png')
    plt.savefig(frame_path)
    plt.close(fig)
    frames.append(imageio.imread(frame_path))

# Save the frames as a GIF
imageio.mimsave('plots/enron_stockprice/enron_rolling_plot.gif', frames, fps=5)
