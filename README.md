# Enron Sentiment Analysis

This code is written by the team at Superflows. Check it out if you spend too long in your emails inbox.

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
## Code

The structure of the code is:
```
enron-sentiment-analysis/
├── README.md           # overview of the project
├── main.py
├── requirements.txt    # software requirements and dependencies
├── config.yml          # settings for running the code
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
│       └──ENRON_stock_prices.csv
├── utils/
│   ├── build_emotion_score_df.py
│   ├── download_enron_dataset.py
│   ├── share_price.py
│   ├── sentiment_through_time.py
│   └── loadsave_emails.py
├── plots/
│   ├── sentiment
│       └── Images for sentiment gif
│   └── enron_stockprice
│       ├──frames/
│           └──Frames of stock price gif
│       └──enron_rolling_plot.gif
```

To run the code, you will need:
- Enron dataset. You can get this by setting the flag in config to True
- NRC Emotion Lexicon. You should find this in the repo under data/sentiment
- Stock price. You should find this in the repo under data/enron_stockprice/ENRON_stock_prices.csv

To run the analysis from scratch, set the variables in the config file:
- download_dataset
- build_analysis
- make_sentiment_plots
- make_share_plots

By default, ```build_analysis``` is ```False```, and ```make_plots``` is ```True```.

If you'd like to build the analysis from scratch, set ```build_analysis``` to True. 

----
## Installation 

This code uses several packages. You'll need to have installed:
- Pandas
- Matplotlib
- imageio

To install the relevant packages, run ```pip install -r requirements.txt```

To run the analysis, you should run the main.py file. 

