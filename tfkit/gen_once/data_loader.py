import csv
import os
import pickle
from collections import defaultdict

import numpy as np
from torch.utils import data
from transformers import BertTokenizer


class loadOnceDataset(data.Dataset):
    def __init__(self, fpath, tokenizer, maxlen=510, cache=False):
        sample = []
        tokenizer = BertTokenizer.from_pretrained(tokenizer)
        cache_path = fpath + ".cache"
        if os.path.isfile(cache_path) and cache:
            with open(cache_path, "rb") as cf:
                sample = pickle.load(cf)
        else:
            for i in get_data_from_file(fpath):
                tasks, task, input, target = i
                feature = get_feature_from_data(tokenizer, maxlen, input, target)
                if len(feature['input']) <= 512:
                    sample.append(feature)
            if cache:
                with open(cache_path, 'wb') as cf:
                    pickle.dump(sample, cf)

        self.sample = sample

    def __len__(self):
        return len(self.sample)

    def __getitem__(self, idx):
        return self.sample[idx]


def get_data_from_file(fpath):
    tasks = defaultdict(list)
    task = 'default'
    tasks[task] = []
    with open(fpath, encoding='utf') as csvfile:
        for i in list(csv.reader(csvfile)):
            source_text = i[0]
            target_text = i[1]
            input = "[CLS] " + source_text + " [SEP]"
            target = target_text + " [SEP]"
            yield tasks, task, input, target


def get_feature_from_data(tokenizer, maxlen, input, target=None, ntarget=None):
    row_dict = dict()
    tokenized_input = tokenizer.tokenize(input)
    mask_id = [1] * len(tokenized_input)
    type_id = [0] * len(tokenized_input)

    row_dict['target'] = np.asarray([-1] * maxlen)
    row_dict['ntarget'] = np.asarray([-1] * maxlen)

    if target is not None:
        tokenized_target = tokenizer.tokenize(target)
        tokenized_target_id = [-1] * len(tokenized_input)
        tokenized_target_id.extend(tokenizer.convert_tokens_to_ids(tokenized_target))
        tokenized_target_id.extend([-1] * (maxlen - len(tokenized_target_id)))
        row_dict['target'] = np.asarray(tokenized_target_id)

    if ntarget is not None:
        tokenized_ntarget = tokenizer.tokenize(ntarget)
        tokenized_ntarget_id = [-1] * len(tokenized_input)
        tokenized_ntarget_id.extend(tokenizer.convert_tokens_to_ids(tokenized_ntarget))
        tokenized_ntarget_id.extend([-1] * (maxlen - len(tokenized_ntarget_id)))
        row_dict['ntarget'] = np.asarray(tokenized_ntarget_id)

    tokenized_input_id = tokenizer.convert_tokens_to_ids(tokenized_input)
    target_start = len(tokenized_input_id)
    tokenized_input_id.extend([tokenizer.mask_token_id] * (maxlen - len(tokenized_input_id)))
    mask_id.extend([0] * (maxlen - len(mask_id)))
    type_id.extend([1] * (maxlen - len(type_id)))

    row_dict['input'] = np.asarray(tokenized_input_id)
    row_dict['type'] = np.asarray(type_id)
    row_dict['mask'] = np.asarray(mask_id)
    row_dict['start'] = target_start
    # if debug:
    #     print("*** Example ***")
    #     print(f"input: {len(row_dict['input'])}, {row_dict['input']} ")
    #     print(f"type: {len(row_dict['type'])}, {row_dict['type']} ")
    #     print(f"mask: {len(row_dict['mask'])}, {row_dict['mask']} ")
    #     if target is not None:
    #         print(f"target: {len(row_dict['target'])}, {row_dict['target']} ")
    #     if ntarget is not None:
    #         print("POS", target_start, len(tokenized_ntarget))
    #         print("STR", tokenized_target, tokenized_ntarget)
    #         print("ANS", tokenized_target[target_start], tokenized_ntarget_id)
    #         print(f"ntarget: {len(tokenized_ntarget_id)}, {row_dict['ntarget']} ")
    return row_dict
