
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
			content = reviews['Content']
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
					sentence = content.strip().split(' ')
					ner_tags = ['O'] * (len(sentence))
					sentence_clear = []
					ner_tags_clear = []
					# solve the '  ' multi space
					special_token = "$()*+.[]?\\^}{|!'#%&,-/:;_~@<=>`\"’“”‘…"
					special_token_re = r"[\$\(\)\*\+\.\[\]\?\\\^\{\}\|!'#%&,-/:;_~@<=>`\"’‘“”…]{1,1}"
					for x in range(len(sentence)):
						in_word = False
						if sentence[x] != '':
							punctuation_list = re.finditer(special_token_re, sentence[x])
							punctuation_list_start = []
							punctuation_list_len = []
							for m in punctuation_list:
								punctuation_list_start.append(m.start())
								punctuation_list_len.append(len(m.group()))

							if len(punctuation_list_start) != 0:
								# the start is word
								if punctuation_list_start[0] != 0:
									sentence_clear.append(sentence[x][0:punctuation_list_start[0]])
									ner_tags_clear.append(ner_tags[x])
								for (i, m) in enumerate(punctuation_list_start):
									# print(len(punctuation_list_start))
									# print(len(punctuation_list_len))
									# print(str(m) + ' - ' + str(m+punctuation_list_len[i]))
									sentence_clear.append(sentence[x][m:m + punctuation_list_len[i]])
									ner_tags_clear.append(ner_tags[x])

									if i != len(punctuation_list_start) - 1:
										if m + punctuation_list_len[i] != punctuation_list_start[i + 1]:
											sentence_clear.append(
												sentence[x][m + punctuation_list_len[i]:punctuation_list_start[i + 1]])
											ner_tags_clear.append(ner_tags[x])

									else:
										if m + punctuation_list_len[i] < len(sentence[x]):
											sentence_clear.append(sentence[x][m + punctuation_list_len[i]:])
											ner_tags_clear.append(ner_tags[x])


							else:  # has no punctuation
								sentence_clear.append(sentence[x])
								ner_tags_clear.append(ner_tags[x])

					assert '' not in sentence_clear
					assert len(sentence_clear) == len(ner_tags_clear)
					print("sentence_clear len", len(sentence_clear))
					print("ner_tags_clear len", len(ner_tags_clear))
					if len(ner_tags) > 1:
						fout.write(reviewId + '\t' + str(sentiment_value) + '\t' + aspect_sentiment + '\t' + ' '.join(sentence_clear) + '\t' + ' '.join(ner_tags_clear) + '\n')

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