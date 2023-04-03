import yaml

with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if __name__ == '__main__':
    if config['download_dataset']:
        import utils.download_enron_dataset

    if config['build_analysis']:
        import utils.build_emotion_score_df

    if config['make_sentiment_plots']:
        import utils.sentiment_through_time

    if config['make_share_plots']:
        import utils.share_price

