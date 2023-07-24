"""Time-series Generative Adversarial Networks (TimeGAN) Codebase.

Reference: Jinsung Yoon, Daniel Jarrett, Mihaela van der Schaar, 
"Time-series Generative Adversarial Networks," 
Neural Information Processing Systems (NeurIPS), 2019.

Paper link: https://papers.nips.cc/paper/8789-time-series-generative-adversarial-networks

Last updated Date: April 24th 2020
Code author: Jinsung Yoon (jsyoon0823@gmail.com)

-----------------------------

main_timegan.py

(1) Import data
(2) Generate synthetic data
(3) Evaluate the performances in three ways
  - Visualization (t-SNE, PCA)
  - Discriminative score
  - Predictive score
"""

## Necessary packages
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# 1. TimeGAN model
from timegan import timegan
# 2. Data loading
from data_loading import real_data_loading
# 3. Metrics
from gan.timegan.metrics.discriminative_metrics import discriminative_score_metrics
from gan.timegan.metrics import predictive_score_metrics
from gan.timegan.metrics.visualization_metrics import visualization

import pandas as pd


def export_results(dataset_name = "load"):

    with open("result"+dataset_name+ ".pickle", "rb") as f:
        ori_data = pickle.load(f)
        generated_data = pickle.load(f)
        # print(generated_data.shape)
        metrics = pickle.load(f)
        idx = pickle.load(f)




        # reorder the data
        ori_data_ordered = []
        generated_data_ordered = []
        for i in range(len(ori_data)):
            ori_data_ordered.append(ori_data[idx.tolist().index(i)])
            generated_data_ordered.append(generated_data[idx.tolist().index(i)])




        # unsplit the data
        ori_data_ordered = np.array(ori_data_ordered)

        ori_recon = ori_data_ordered[0, :, :]
        ori_data = []

        for i in ori_recon:
            ori_data.append(list(i))

        for i in range(1, len(ori_data_ordered)):
            ori_data.append(list(ori_data_ordered[i, -1, :]))


        generated_data_ordered = np.array(generated_data_ordered)
        # print(generated_data_ordered.shape)

        print(generated_data_ordered.shape)

        generated_recon = generated_data_ordered[0, :, :]
        print(generated_recon.shape)

        generated_data = []

        for i in generated_recon:
            generated_data.append(list(i))

        for i in range(1, len(generated_data_ordered)):
            generated_data.append(list(generated_data_ordered[i, -1, :]))

        df_ori = pd.DataFrame.from_records(ori_data)
        df_gen = pd.DataFrame.from_records(generated_data)


        df_gen.to_csv("generated_data.csv")




def main(args):
    """Main function for timeGAN experiments.

    Args:
      - data_name: sine, stock, or energy
      - seq_len: sequence length
      - Network parameters (should be optimized for different datasets)
        - module: gru, lstm, or lstmLN
        - hidden_dim: hidden dimensions
        - num_layer: number of layers
        - iteration: number of training iterations
        - batch_size: the number of samples in each batch
      - metric_iteration: number of iterations for metric computation

    Returns:
      - ori_data: original data
      - generated_data: generated synthetic data
      - metric_results: discriminative and predictive scores
    """
    ## Data loading

    data_path = '/Users/abdel/PycharmProjects/tsgen/gan/timegan/data/stock_data.csv'
    ori_data, idx = real_data_loading(data_path, args.seq_len)

    print(data_path + ' dataset is ready.')

    ## Synthetic data generation by TimeGAN
    # Set newtork parameters
    parameters = dict()
    parameters['module'] = args.module
    parameters['hidden_dim'] = args.hidden_dim
    parameters['num_layer'] = args.num_layer
    parameters['iterations'] = args.iteration
    parameters['batch_size'] = args.batch_size

    generated_data = timegan(ori_data, parameters)

    print('Finish Synthetic Data Generation')

    ## Performance metrics
    # Output initialization
    metric_results = dict()

    # 1. Discriminative Score
    discriminative_score = list()
    for _ in range(args.metric_iteration):
        temp_disc = discriminative_score_metrics(ori_data, generated_data)
        discriminative_score.append(temp_disc)

    metric_results['discriminative'] = np.mean(discriminative_score)

    # 2. Predictive score
    predictive_score = list()
    for tt in range(args.metric_iteration):
        temp_pred = predictive_score_metrics(ori_data, generated_data)
        predictive_score.append(temp_pred)

    metric_results['predictive'] = np.mean(predictive_score)

    # 3. Visualization (PCA and tSNE)
    visualization(ori_data, generated_data, 'pca')
    visualization(ori_data, generated_data, 'tsne')

    ## Print discriminative and predictive scores
    print(metric_results)

    return ori_data, generated_data, metric_results, idx


def export_results(generated_data, idx, result_file_name):

        # reorder the data
        generated_data_ordered = []
        for i in range(len(generated_data)):
            generated_data_ordered.append(generated_data[idx.tolist().index(i)])

        # unsplit the data
        generated_data_ordered = np.array(generated_data_ordered)
        # print(generated_data_ordered.shape)

        generated_recon = generated_data_ordered[0, :, :]
        print(generated_recon.shape)

        generated_data = []

        for i in generated_recon:
            generated_data.append(list(i))

        for i in range(1, len(generated_data_ordered)):
            generated_data.append(list(generated_data_ordered[i, -1, :]))

        import pandas as pd
        df_gen = pd.DataFrame.from_records(generated_data)

        df_gen.to_csv(result_file_name)


if __name__ == '__main__':
    # Inputs for the main function
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--seq_len',
        help='sequence length',
        default=24,
        type=int)
    parser.add_argument(
        '--module',
        choices=['gru', 'lstm', 'lstmLN'],
        default='gru',
        type=str)
    parser.add_argument(
        '--hidden_dim',
        help='hidden state dimensions (should be optimized)',
        default=24,
        type=int)
    parser.add_argument(
        '--num_layer',
        help='number of layers (should be optimized)',
        default=3,
        type=int)
    parser.add_argument(
        '--iteration',
        help='Training iterations (should be optimized)',
        default=1,
        type=int)
    parser.add_argument(
        '--batch_size',
        help='the number of samples in mini-batch (should be optimized)',
        default=128,
        type=int)
    parser.add_argument(
        '--metric_iteration',
        help='iterations of the metric computation',
        default=10,
        type=int)

    args = parser.parse_args()

    # Calls main function
    ori_data, generated_data, metrics, idx = main(args)

    print(generated_data)


    export_results(generated_data, idx, "generated_data.csv")

    import pickle

    with open('result' + args.data_name + '.pickle', 'wb') as f:
        pickle.dump(ori_data, f)
        pickle.dump(generated_data, f)
        pickle.dump(metrics, f)
        pickle.dump(idx, f)


    export_results(args.data_name)