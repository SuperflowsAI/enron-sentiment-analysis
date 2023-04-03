import pandas as pd
from utils.loadsave_emails import *
import yaml

with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

nrc_lexicon_path = './data/sentiment/NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'


def preprocess_nrc_lexicon(file_path):
    nrc_data = pd.read_csv(file_path, names=["word", "emotion", "association"], sep='\t')
    nrc_data = nrc_data.pivot_table(index='word', columns='emotion', values='association').reset_index()
    emotion_dict = nrc_data.set_index('word').T.to_dict('list')
    return emotion_dict

def get_emotion_scores(text, emotion_dict):
    '''
    Gets the NRC Lexicon Emotion score for each email.

    It first tokenises the emails, then goes through each token and assigns the NRC Lexicon Emotion score. It
    then sums these scores and stores the result for each email in a dict.



    :param text:
    :param emotion_dict:
    :return:
    '''
    tokens = nltk.word_tokenize(text.lower())
    #emotion_count = Counter()

    emotions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for token in tokens:
        if token in emotion_dict:
            token_emotion = emotion_dict[token]
            emotions = [x + y for x, y in zip(emotions, token_emotion)]

    #### CHANGED HERE
    emotions = [e/len(tokens) for e in emotions]

    return emotions

def get_rolling_positve_negative_scores():
    email_df = email_df.sort_values('timestamp')
    email_df['pos_neg_diff'] = email_df['positive'] - email_df['negative']
    email_df = email_df.set_index('timestamp')
    email_df['rolling_30day_avg'] = email_df['pos_neg_diff'].rolling('30D').mean()

    plt.figure(figsize=(15, 8))
    plt.plot(email_df.index, email_df['rolling_30day_avg'])
    plt.xlabel('Date')
    plt.ylabel('Rolling 30-Day Average (Positive - Negative)')
    plt.title('Sentiment Analysis: Rolling 30-Day Average of Positive-Negative Score')
    plt.show()
    return net_score

def get_email_length(row):

    email = row['body']
    return len(email.split())

def get_length_normalised_emotion(row, emotion):
    """
    Calculate the length-normalized emotion value for a given row and emotion.

        Parameters:
    -----------
    row : pd.Series or dict
        A row containing emotion values and email length, typically from a pandas DataFrame.
    emotion : str
        The name of the emotion for which the length-normalized value is to be calculated.

    Returns:
    --------
    float
        The length-normalized emotion value.

    This function takes a row containing emotion values and email length, and calculates the
    length-normalized value for the specified emotion by dividing the raw emotion value by the
    email length. This helps to account for differences in email length when comparing emotion
    intensities across different emails.
    """

    return row[emotion] / row['email_length']

def processes_emails_dataframe(emails_df, emotion_dict):
    # Get emotion scores for each email, then unpack into dataframe

    emails_df['emotion_scores'] = emails_df['body'].progress_apply(lambda x: get_emotion_scores(x, emotion_dict))
    emails_df[['anger', 'anticipation', 'disgust', 'fear', 'joy',
            'negative', 'positive', 'sadness', 'surprise', 'trust']] = emails_df.emotion_scores.tolist()

    # Convert datetime to index
    emails_df['date_dt'] = pd.to_datetime(emails_df['date'])
    emails_df['date'] = pd.to_datetime(emails_df['date'], errors='coerce')
    emails_df['year_month'] = emails_df['date_dt'].apply(lambda x: get_yearmonth(x))

    # Get length of email
    emails_df['email_length'] = emails_df.apply(get_email_length, axis=1)

    # Drop rows with invalid datetime values
    emails_df = emails_df.dropna(subset=['date'])

    categories = ['joy', 'anticipation', 'surprise', 'anger', 'disgust', 'fear', 'sadness', 'trust']

    for emotion in categories:
        column_name = 'len_norm_' + emotion
        emails_df[column_name] = emails_df.apply(get_length_normalised_emotion,
                                                 args=(emotion,),
                                                 axis=1)

    # Remove timezone information
    emails_df['date'] = emails_df['date'].apply(lambda x: x.replace(tzinfo=None))

    # Sort by date
    emails_df = emails_df.sort_values('date')
    emails_df['pos_neg_diff'] = emails_df['positive'] - emails_df['negative']

    # Reset the index after resampling and calculating the rolling mean
    emails_df.reset_index(inplace=True)

    return emails_df



if config['build_analysis']:
    ### Load emails if not already loaded
    try: enron_dataset
    except:
        filepath = r"./data/enron_dataset/enron_dataset.json"
        enron_dataset = load_emails_from_json(filepath)

    ### Load emails_df processed data if not already loaded
    emails_df = pd.DataFrame.from_dict(enron_dataset)
    ### Load emotion processed data if not already loaded
    try:
        emotion_dict
    except:
        print('Loading NRC Lexicon Dictionary')
        preprocess_nrc_lexicon(nrc_lexicon_path)

    emails_df = processes_emails_dataframe(emails_df, emotion_dict)
    emails_df.to_pickle("./data/sentiment/email_sentiment_df.pkl")