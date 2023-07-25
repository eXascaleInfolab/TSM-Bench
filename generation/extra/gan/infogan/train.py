# -*- coding: utf-8 -*-
import json


import numpy as np
import sugartensor as tf
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# import tensorflow as tf


def main(input_data_path, model_path, shift, num_cont, max_epo, tr_sampling_size):

    class TimeSeriesData(object):
        def __init__(self, batch_size=128, path='datasets/bafu.csv', window=120):
            # load data
            try:
                df = pd.read_csv(path, delimiter=',', header=None, nrows = tr_sampling_size)
                # x = np.genfromtxt(path, delimiter=',', dtype=np.float32)
                x = df.to_numpy()

                x = x[:tr_sampling_size]

            except:
                tf.sg_info("The file in the path %s couldn't be read", path)
                exit(-1)
            # x = x[1:]
            # print(x)

            scaler = MinMaxScaler(copy=False)

            # delete zero pad data
            n = x.shape[0] # // window * window
            # n = ((np.where(np.any(x, axis=1))[0][-1] + 1) // window) * window

            try :
                x[0][0] = x[0][0]
            except:
                x = x.reshape(-1, 1)

            # normalize data between 0 and 1
            scaler.fit(x)
            x = scaler.transform(x)

            X = np.asarray([x[i:i + window] for i in range(0, n - window + 1, shift)])
            # # X = np.asarray([x[i:i + window] for i in range(0, n - window + 1, max(1, int(window * (1 - winShift))))])

            # X = np.asarray([x[i:i + window] for i in range(n - window + 1)])

            # make to matrix
            # if (winShift):
            #     X = np.asarray([x[i:i + window] for i in range(n - window + 1)])
            # else:
            #     X = np.asarray([x[i:i + window] fo OK so yes are you OK let's so yeah I what I did is that I ran on multiple times series the first one which is the time shift the second one which is a normal sign and with out and 1/ third one which is a growing sign and the last three is the most somewhere OK and lastly the are you are you sorry there is and most somewhere…r i in range(0, n - window + 1, window)])

            # shuffle data
            # for i in X:
            #     plt.plot(i)
            #     plt.show()

            np.random.shuffle(X)
            X = np.expand_dims(X, axis=2)

            # save to member variable
            self.batch_size = batch_size
            self.X = tf.sg_data._data_to_tensor([X], batch_size, name='train')
            self.num_batch = X.shape[0] // batch_size

            self.X = tf.to_float(self.X)

    # set log level to debug
    tf.sg_verbosity(10)

    #
    # hyper parameters
    #
    with open("./parameters.json", "r") as f:
        para_dict = json.load(f)
        window = para_dict["window"]  # window size
        batch_size = para_dict["batch_size_train"]  # batch size
        # num_category = para_dict["num_category"]  # category variable number
        # tr_sampling_size = para_dict["tr_sampling_size"]
        # num_cont = para_dict["num_cont"]  # continuous variable number
        # num_dim = para_dict["num_dim"]  # total latent dimension ( category + continuous + noise )
        num_dim = num_cont
        # path = para_dict["input_data_path"]  # dataset path
        # max_ep = para_dict["max_ep"]  # max epochs
        max_ep = max_epo  # max epochs
        # winShift = para_dict["winShift"]

    # model_path = para_dict["model_path"]  # model path

    #
    # inputs
    #

    # input tensor ( with QueueRunner )
    data = TimeSeriesData(batch_size=batch_size, path=input_data_path, window=window)
    x = data.X

    # generator labels ( all ones )
    y = tf.ones(batch_size, dtype=tf.sg_floatx)

    # discriminator labels ( half 1s, half 0s )
    y_disc = tf.concat([y, y * 0], 0)

    #
    # create generator
    #

    # random class number
    # z_cat = tf.multinomial(tf.ones((batch_size, num_category), dtype=tf.sg_floatx) / num_category, 1).sg_squeeze()

    # random seed = random categorical variable + random uniform
    z = tf.random_uniform((batch_size, num_cont))
    # z = z_cat.sg_one_hot(depth=num_category).sg_concat(target=tf.random_uniform((batch_size, num_dim - num_category)))

    # random continuous variable
    z_cont = z

    # generator network
    with tf.sg_context(name='generator', size=(4, 1), stride=(2, 1), act='relu', bn=True):
        gen = (z.sg_dense(dim=1024)
               .sg_dense(dim=int(window * 16))
               .sg_reshape(shape=(-1, int(window / 8), 1, 128))
               .sg_upconv(dim=64)
               .sg_upconv(dim=32)
               .sg_upconv(dim=num_cont, act='sigmoid', bn=False))

        # .sg_dense(dim=int(window / 8 * 1 * 128))

    #
    # create discriminator & recognizer
    #
    # print (x)
    # print (gen)
    # create real + fake image input
    xx = tf.concat([x, gen], 0)

    with tf.sg_context(name='discriminator', size=(4, 1), stride=(2, 1), act='leaky_relu'):
        # shared part
        shared = (xx.sg_conv(dim=32)
                  .sg_conv(dim=64)
                  .sg_conv(dim=128)
                  .sg_flatten()
                  .sg_dense(dim=1024))
        # shared recognizer part
        recog_shared = shared[batch_size:, :].sg_dense(dim=128)
        # discriminator end
        disc = shared.sg_dense(dim=1, act='linear').sg_squeeze()
        # continuous recognizer end
        recog_cont = recog_shared.sg_dense(dim=num_cont, act='sigmoid')

    #
    # loss and train ops
    #

    loss_disc = tf.reduce_mean(disc.sg_bce(target=y_disc))  # discriminator loss
    loss_gen = tf.reduce_mean(disc.sg_reuse(input=gen).sg_bce(target=y))  # generator loss
    loss_recog = tf.reduce_mean(recog_cont.sg_mse(target=z_cont))  # recognizer loss

    train_disc = tf.sg_optim(loss_disc + loss_recog, lr=0.0001, category='discriminator')  # discriminator train ops
    train_gen = tf.sg_optim(loss_gen + loss_recog, lr=0.001, category='generator')  # generator train ops

    #
    # training
    #

    # def alternate training func
    @tf.sg_train_func
    def alt_train(sess, opt, save_dir=model_path):
        l_disc = sess.run([loss_disc, train_disc])[0]  # training discriminator
        l_gen = sess.run([loss_gen, train_gen])[0]  # training generator

        return np.mean(l_disc) + np.mean(l_gen)

    # do training
    alt_train(log_interval=10, max_ep=max_ep, ep_size=data.num_batch, early_stop=False, save_dir=model_path)



if __name__ == "__main__":
    main(input_data_path="outputR.csv", model_path='assetR/train/')
