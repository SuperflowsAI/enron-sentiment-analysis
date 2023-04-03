# Enron Sentiment Analysis

The Enron dataset is an extensive corpus of over 500,000 internal emails at the company, spanning the period it's collapse. 

This code uses the NRC Emotion Lexicon to analyse the emotional shifts within the company over this period. The steps in processing are: 

1. Preprocessing
2. Sentiment Scoring
3. Aggregation
4. Normalisation
5. Plotting

To provide context, the share price is also plotted. This was aligned manually to the month being shown in radar plots after production. 

We wrote up a blog of the story and processing. You can find it here: https://www.superflows.ai/blog/enron-sentiment

----
The structure of the code is:
```
enron-sentiment-analysis/
├── README.md           # overview of the project
├── requirements.txt    # software requirements and dependencies
├── share_price.py
├── sentiment_through_time.py
├── data/               # data files used in the project
│   ├──  enron_dataset/
│       ├──maildir/
│           └──Folders by user with email data
│       └──enron_dataset.json
│   ├──  sentiment/
│       ├──NRC-Emotion-Lexicon/
│           ├──Paper1_NRC_Emotion_Lexicon.pdf
│           ├──Paper2_NRC_Emotion_Lexicon.pdf
│           ├──README.txt
│           └──NRC-Emotion-Lexicon-Wordlevel-v0.92.txt
│       └──email_sentiment_df.pkl
│   └──  enron_stockprice/
├── utils/
│   ├── build_emotion_score.py
│   └── loadsave_emails.py
├── plots/
│   └──  enron_stockprice
│       ├──frames/
│           └──Frames of stock price gif
│       └──enron_rolling_plot.gif
```

To run the code, you will need:
- DATASETS

To run the analysis from scratch, set the variables in the config file:
- build_analysis
- make_plots

We've created a pandas dataframe with the completed analysis, saved as a .pickle file. You can simply load this file
and run the rest of the code. 

By default, build_analysis is False, and make_plots is True.

If you do not have 'build_analysis' set to True, the pickle file will be loaded by default

If you'd like to build the analysis from scratch, set '''build_analysis''' to True. 

----
Installation 

This code uses several packages. You'll need to have installed:
- Pandas
- Matplotlib
- imageio

To run the analysis, you should run the main.py file. 

