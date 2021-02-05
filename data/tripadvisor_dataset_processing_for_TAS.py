
import os
import re
import argparse
import json
from change_TO_to_BIO import TXT_file, TSV_file, change_TO_to_BIO

def get_aspect_sentiment_compose_set(path, file_name, output_path, output_file):
	aspect_set = []
	sentiment_set = ['positive', 'negative', 'neutral']
	with open(os.path.join(path, file_name)) as json_file, open(os.path.join(output_path, TSV_file(output_file)), 'w', encoding='utf-8') as fout:
		fout.write('\t'.join(['sentence_id', 'yes_no', 'aspect_sentiment', 'sentence', 'ner_tags']))
		fout.write('\n')
		data = json.load(json_file)
		for reviews in data['Reviews']:
			sentance = reviews['Content']
			reviewId = reviews['ReviewID']
			aspects = reviews['Ratings']
			for aspect, rating in aspects.items():
				print(aspect, rating)
				rating = float(rating)
				for i in range(len(sentiment_set)):
					sentiment = sentiment_set[i]
					aspect_sentiment = aspect + ' ' + sentiment
					sentiment_value = 0
					if i == 0 and rating > 3:
						sentiment_value = 1
					elif i == 1 and rating < 3:
						sentiment_value = 1
					elif i == 2 and rating == 3:
						sentiment_value = 1
					sentence_arr = sentance.strip().split(' ')
					ner_tags = ['O'] * (len(sentence_arr) + 10)
					if len(ner_tags) > 1:
						fout.write(reviewId + '\t' + str(sentiment_value) + '\t' + aspect_sentiment + '\t' + sentance + '\t' + ' '.join(ner_tags) + '\n')

	compose_set = []
	return compose_set

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--dataset',
						type=str,
						choices=["semeval2015", "semeval2016"],
						help='dataset, as a folder name, you can choose from semeval2015 and semeval2016')
	args = parser.parse_args()

	path = args.dataset + '/three_joint'
	output_path = path + '/BIO'
	test_file = 'trip_advisor.json'
	test_output = 'test_TAS23'

	# get set of aspect-sentiment
	compose_set = get_aspect_sentiment_compose_set(args.dataset, test_file, output_path, test_output)

	# for input_file, output_file in zip([train_file, test_file], [train_output, test_output]):
	# 	# get preprocessed data, TO labeling schema
	# 	create_dataset_file(args.dataset, output_path, input_file, output_file, compose_set)
	# 	# get preprocessed data, BIO labeling schema
	# 	change_TO_to_BIO(path, output_file)