import matplotlib.pyplot as plt
import pandas as pd
import imageio
from math import pi
from config import *

### Set path to save out plots
plots_filepath = config.plot_savepath

def get_yearmonth(date):
    '''
    Returns the year and month of a given date in 'YYYY-MM' format.

    This function takes a datetime object as input and extracts the year and month
    from it. It then formats the extracted year and month as a string in the
    'YYYY-MM' format.

    Parameters:
    ----------
    date : datetime.datetime
        The input date for which the year and month are to be extracted and formatted.

    Returns:
    -------
    yearmonth : str
        The year and month of the given date in 'YYYY-MM' format.

    Example:
    --------
    >>> from datetime import datetime
    >>> date = datetime(2021, 9, 1)
    >>> get_yearmonth(date)
    '2021-09'
    '''

    year = date.year
    month = date.month

    if len(str(month)) < 2:

        month = '0' + str(month)

    yearmonth = str(year) + '-' + str(month)

    return yearmonth

def generate_intermediate_frames(values1, values2, num_frames):
    """
    Generates a list of intermediate frames by interpolating between two sets of values.

    This function takes in two sets of values and calculates a specified number of intermediate
    frames by linearly interpolating between the values. The resulting intermediate frames
    are returned as a list.

    Parameters:
    ----------
    values1 : list of float
        The starting values to interpolate from.
    values2 : list of float
        The ending values to interpolate to.
    num_frames : int
        The number of intermediate frames to generate between the two sets of values.

    Returns:
    -------
    intermediate_frames : list of list of float
        A list of lists, where each inner list contains the interpolated values for each
        intermediate frame.

    Example:
    --------
    >>> values1 = [0, 0, 0]
    >>> values2 = [1, 1, 1]
    >>> num_frames = 3
    >>> generate_intermediate_frames(values1, values2, num_frames)
    [[0.25, 0.25, 0.25], [0.5, 0.5, 0.5], [0.75, 0.75, 0.75]]
    """


    intermediate_frames = []
    for t in range(1, num_frames + 1):
        weight = t / (num_frames + 1)
        intermediate_values = [(1 - weight) * v1 + weight * v2 for v1, v2 in zip(values1, values2)]
        intermediate_frames.append(intermediate_values)
    return intermediate_frames

def draw_radar_plot(categories, values, max_value, date_str, filename):
    """
    Creates and saves a radar plot based on the given input parameters.

        Parameters:
    -----------
    categories : list
        A list of categories (labels) for the radar plot.
    values : list
        A list of values corresponding to each category.
    max_value : float
        The maximum value to scale the plot. This is not used in the function but kept for future use.
    date_str : str
        The date string to be used as the title of the plot.
    filename : str
        The file name to save the plot as.

    Returns:
    --------
    None

    This function creates a radar plot with the given categories and values, and saves the plot
    to a file with the specified name. The plot will have a title with the date string, no y-axis
    tick labels, and no x-axis tick labels. The plot will be filled with blue color at 10%
    opacity. The function does not return any value.
    """

    print('PLOTTING: ', date_str)

    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    plt.xticks(angles[:-1], categories, color='black', size=10)
    plt.ylim(0, max_value)
    plt.title(date_str, size=20, y=1.1)

    ax.set_rlabel_position(0)
    ax.axes.yaxis.set_ticklabels([])
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])

    #ax.set_facecolor('lightgray')
    ax.set_facecolor((0.95, 0.95, 0.95))
    ax.spines['polar'].set_visible(False)

    # save the plot
    fig.savefig(filename)
    plt.close(fig)

def apply_exponential(values, factor):
    return [v ** factor for v in values]


if not config.build_analysis:
    try:
        emails_df
    except:
        email_df_path = ("./data/sentiment/email_sentiment_df.pkl")
        emails_df = pd.read_pickle(email_df_path)

if config.build_analysis:
    from utils.build_emotion_score_df import *



exponential_factor = 2
num_intermediate_frames = 5

categories = ['joy','anticipation', 'surprise', 'anger', 'disgust', 'fear', 'sadness', 'trust']

for emotion in categories:
    column_name = 'len_norm_' + emotion
    emails_df[column_name] = emails_df.apply(get_length_normalised_emotion,
                                             args=(emotion,),
                                             axis=1)

monthly_df = emails_df.groupby(emails_df['year_month'])

excluded_dates = ['1979-12', '1986-04', '1986-05', '2002-09',
                  '1997-11', '1997-01', '1997-03', '1997-04',
                  '1997-05', '1997-06', '1997-07', '1997-08',
                  '1997-09', '1997-10', '1998-01', '1998-05',
                  '1998-09', '1998-11', '1998-10', '1998-12',
                  '1999-01', '2004-02', '2002-12', '2002-02',
                  '2002-10', '2004-02', '2005-12', '2007-02',
                  '2012-11', '2020-12','2024-05', '2043-12',
                  '2044-01']

img_files = []

### Compute baselines for each emotion
emotion_baselines = {}

for category in categories:
    emotion_baseline = emails_df.loc[:, category].mean()
    emotion_baselines[category] = emotion_baseline

### Compute emotion value for each month, normalised to baseline
max_value = 0
monthly_emotions = {}

for idx, row in monthly_df:

    if idx in excluded_dates:
        print('Skipping: ', idx)
        continue

    row = row[row['email_length'] > 10][row['email_length'] < 500]

    values = [row[emotion].mean() / emotion_baselines[emotion] for emotion in categories]

    net_positive = row['positive'].mean() - row['negative'].mean()

    norm_values = [float(i)/sum(values) for i in values]

    if max(norm_values) == 1:
        continue

    monthly_emotions[idx] = norm_values

    if max(norm_values) > max_value:
        max_value = max(norm_values)

### Create radar plot of emotions
previous_idx = None
previous_values = None

for idx in monthly_emotions:

    img_filename = f'radar_plot_midemails_{idx}.png'
    img_filepath = plots_filepath + img_filename

    exp_values = apply_exponential(monthly_emotions[idx], exponential_factor)

    if previous_values is not None:
        intermediate_frames = generate_intermediate_frames(previous_values, exp_values, num_intermediate_frames)
        for i, intermediate_values in enumerate(intermediate_frames):
            intermediate_filename = f'radar_plot_midemails_{previous_idx}_to_{idx}_{i+1}.png'
            intermediate_filepath = plots_filepath + intermediate_filename
            img_files.append(intermediate_filepath)
            draw_radar_plot(categories, intermediate_values, max_value ** 2, str(previous_idx) + " to " + str(idx), intermediate_filepath)

    draw_radar_plot(categories, exp_values, max_value ** 2, str(idx), img_filepath)
    img_files.append(img_filepath)
    previous_idx = idx
    previous_values = exp_values

### Save out as a gif
with imageio.get_writer(plots_filepath + 'sentiment_radar_midemails_plot.gif', mode='I', duration=0.2) as writer:
    for img_file in img_files:
        image = imageio.imread(img_file)
        writer.append_data(image)

