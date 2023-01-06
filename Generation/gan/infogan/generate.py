# -*- coding: utf-8 -*-
import json
import numpy as np
import pandas as pd
import sugartensor as tf
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from tqdm import tqdm

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# import tensorflow as tf



class Generator():

    def __init__(self, model_path, batch_size, num_cont):

        #
        # hyper parameters
        #

        self.model_path = model_path
        with open("./parameters.json", "r") as f:
            para_dict = json.load(f)
            self.window = para_dict["window"]  # window size
            self.batch_size = batch_size  # batch size
            # self.batch_size = para_dict["batch_size_generation"]  # batch size
            # self.num_category = para_dict["num_category"]  # category variable number
            # self.num_cont = para_dict["num_cont"]  # continuous variable number
            self.num_cont = num_cont
            self.num_dim = num_cont  # total latent dimension ( category + continuous + noise )
            # self.num_dim = num_cont + self.num_category  # total latent dimension ( category + continuous + noise )
            # self.num_dim = para_dict["num_dim"]  # total latent dimension ( category + continuous + noise )
            # model_path = para_dict["model_path"]  # model path
            self.fake_generated_data = None
            self.window = para_dict["window"]
            # self.classified_generated_data = None

    def plot_generation(self, data, fig_name='sample.png'):
        import math
        nbplots = min(10, int(math.sqrt(self.batch_size)))
        # plot result
        _, ax = plt.subplots(nbplots, nbplots, sharex=True, sharey=True)
        for i in range(nbplots):
            for j in range(nbplots):
                ax[i][j].plot(data[i * nbplots + j, :, 0], linewidth=1)
                # ax[i][j].plot(imgs[i * nbplots + j, :, 1])
                # ax[i][j].set_axis_off()
        plt.savefig(self.model_path + '/' + fig_name, dpi=1500)
        tf.sg_info('Sample image saved to ' + self.model_path + '%s' % fig_name)
        plt.close()


    def progressBar(self, current, total, barLength = 20):
        percent = float(current) * 100 / total
        arrow   = '-' * int(percent/100 * barLength - 1) + '>'
        spaces  = ' ' * (barLength - len(arrow))

        print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

    #
    # save generated data
    #
    def save_generated(self, gen_data, fname='results.csv'):

        # print fake_generated_data.shape
        for i in tqdm(range(self.num_cont)):
            dataframe = pd.DataFrame()
            for j in range(len(self.fake_generated_data)):
                # print('range j')
                dataframe[str(j)] = pd.Series(gen_data[j, :, 0, i])
                # dataframe[str(i) + ',1'] = pd.Series(gen_data[i, :, 0, 1])
                # print(i, j)
            dataframe.to_csv(fname + str(i) + '.csv', index=False)

            # tf.sg_info('Sample image saved to ' + '%s' % fname + str(i) + '.csv')
        # print(dataframe)

    # def generate(self, queue_fake, queue_classified):
    def generate(self, queue_fake):
        #
        # tf.reset_default_graph()
        # tf.Graph().as_default()

        # set log level to debug
        tf.sg_verbosity(10)

        #
        # inputs
        #

        ## target_number
        # target_num = tf.placeholder(dtype=tf.sg_intx, shape=self.batch_size)
        # target continuous variable # 1
        target_cval_1 = tf.placeholder(dtype=tf.sg_floatx, shape=self.batch_size)

        # category variables
        # z = (tf.ones(self.batch_size, dtype=tf.sg_intx) * target_num).sg_one_hot(depth=self.num_category)

        # continuous variables
        # z = z.sg_concat(target=[target_cval_1.sg_expand_dims(), target_cval_2.sg_expand_dims()])
        # z = [target_cval_1.sg_expand_dims()]

        # random seed = categorical variable + continuous variable + random uniform
        z = tf.random_uniform((self.batch_size, self.num_cont))
        # z = z.sg_concat(target=tf.random_uniform((self.batch_size, self.num_dim - 2 - self.num_category)))

        #
        # create generator
        #

        # generator network

        with tf.sg_context(name='generator', size=(4, 1), stride=(2, 1), act='relu', bn=True):
            gen = (z.sg_dense(dim=1024)
                   .sg_dense(dim=int(self.window * 16))
                   .sg_reshape(shape=(-1, int(self.window / 8), 1, 128))
                   .sg_upconv(dim=64)
                   .sg_upconv(dim=32)
                   .sg_upconv(dim=self.num_cont, act='sigmoid', bn=False))

            # .sg_dense(dim=int(self.window / 8 * 1 * 128))
            # .sg_reshape(shape=(-1, int(self.window / 8), 1, 128))
        #
        # run generator
        #
        def run_generator(x1):
            with tf.Session() as sess:
                tf.sg_init(sess)
                # restore parameters
                saver = tf.train.Saver()

                # print(self.model_path)
                saver.restore(sess, tf.train.latest_checkpoint(self.model_path))

                # run generator
                gen_data = sess.run(gen, {target_cval_1: x1})
                tf.sg_info('The data was successfully generated')

                # # plot result
                # _, ax = plt.subplots(10, 10, sharex=True, sharey=True)
                # for i in range(10):
                #     for j in range(10):
                #         ax[i][j].plot(imgs[i * 10 + j, :, 0])
                #         ax[i][j].plot(imgs[i * 10 + j, :, 1])
                #         ax[i][j].set_axis_off()
                # plt.savefig('model/train/' + fig_name, dpi=600)
                # tf.sg_info('Sample image saved to "model/train/%s"' % fig_name)
                # plt.close()
                return gen_data

        #
        # draw sample by categorical division
        #

        self.fake_generated_data = run_generator(np.random.uniform(0, 1, self.batch_size))
        # plot_generation(fake_generated_data, fig_name='fake.png')
        # save_generated(fake_generated_data, model_path+ 'fake.csv')

        # # classified image
        # self.classified_generated_data = run_generator(np.arange(self.num_category).repeat(self.num_category),
        #                                           np.random.uniform(0, 1, self.batch_size), np.random.uniform(0, 1, self.batch_size))

        queue_fake.put(self.fake_generated_data)
        # queue_classified.put(self.classified_generated_data)

        # print self.classified_generated_data

        # plot_generation(classified_generated_data)
        # save_generated(classified_generated_data, model_path+ 'classified.csv')

        # print (classified_generated_data)

        #
        # import pickle
        #
        # with open("model/train/results.dat", "wb") as f:
        #     pickle.dump(fake_generated_data, f)
        #     pickle.dump(classified_generated_data, f)
        #

        # draw sample by continuous division
        #
        #
        # for i in range(10):
        #     run_generator(np.ones(self.batch_size) * i,
        #                   np.linspace(0, 1, self.num_category).repeat(self.num_category),
        #                   np.expand_dims(np.linspace(0, 1, self.num_category), axis=1).repeat(self.num_category, axis=1).T.flatten(),
        #                   fig_name='sample%d.png' % i)

    # def export(self, fake, classified):
    def export(self, fake):
        #
        # plot generated data
        #

        # self.classified_generated_data = classified
        self.fake_generated_data = fake

        with open("./parameters.json", "r") as f:
            para_dict = json.load(f)
            window = para_dict["window"]  # window size
            # batch_size = para_dict["batch_size_generation"]  # batch size
            # num_category = para_dict["num_category"]  # category variable number
            # num_cont = para_dict["num_cont"]  # continuous variable number
            # num_dim = para_dict["num_dim"]  # total latent dimension ( category + continuous + noise )
            num_dim = self.num_cont  # total latent dimension ( category + continuous + noise )

            # model_path = para_dict["model_path"]  # model path
        # self.plot_generation(fake, fig_name='fake.png')
        self.save_generated(fake, self.model_path + 'fake')

        # self.plot_generation(classified, fig_name='classified.png')
        # self.save_generated(classified, self.model_path + 'classified.csv')

    def main(self):
        self.generate()
        self.export()


if __name__ == "__main__":
    g = Generator('model/trainT/')
    g.main()
