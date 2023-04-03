import yaml

with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if __name__ == '__main__':
    # If the "download_dataset" flag is set to True in the config file, import and execute the "download_enron_dataset" script.
    if config['download_dataset']:
        import utils.download_enron_dataset

    # If the "build_analysis" flag is set to True in the config file, import and execute the "build_emotion_score_df" script.
    if config['build_analysis']:
        import utils.build_emotion_score_df

    # If the "make_sentiment_plots" flag is set to True in the config file, import and execute the "sentiment_through_time" script.
    if config['make_sentiment_plots']:
        import utils.sentiment_through_time

    # If the "make_share_plots" flag is set to True in the config file, import and execute the "share_price" script.
    if config['make_share_plots']:
        import utils.share_price

