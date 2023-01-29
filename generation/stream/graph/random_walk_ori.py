import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import time


class RandomWalkOri:
    # Calculates the distance between two series. Given series A, B returns the Euclidean distance between A and B
    def distance(self, a, b):
        return np.sqrt(np.sum((a - b) ** 2))

    # The probability is converted according to the sorted distances, which adds up to 1
    def distopro(self, a):
        a = len(a)
        if (a == 3):
            b = [0.2, 0.3, 0.5]
        elif (a == 4):
            b = [0.1, 0.2, 0.3, 0.4]
        else:
            b = np.random.dirichlet(np.ones(a),size=1)
        return np.array(b)

    # Input is the original data matrix, return is the relationship matrix relation_matrix, and probability matrix probability_matrix
    # Data is the matrix of series, the first dimension is the number of series, and the second dimension is each series
    # Window_size is the size of the window to calculate the distance, and k is the number of the nearest neighbors selected. Currently, 3,4,5 are supported
    def transformA(self, data, window_size, k):
        numOfSeq = data.shape[0]
        distance_matrix = np.ones([numOfSeq, numOfSeq], dtype=float)
        for i in tqdm(range(numOfSeq)):
            for j in range(numOfSeq):
                distance_matrix[i][j] = self.distance(data[i, data.shape[1] - window_size:], data[j, 0:window_size])
        relation_matrix = np.ones([numOfSeq, k], dtype=int)
        subdistance_matrix = np.ones([numOfSeq, k], dtype=float)
        probability_matrix = np.ones([numOfSeq, k], dtype=float)
        for i in tqdm(range(numOfSeq)):
            relation_matrix[i] = distance_matrix[i].argsort()[::-1][data.shape[0] - k:]
            # print(relation_matrix[i])
        for i in tqdm(range(numOfSeq)):
            for j in range(k):
                subdistance_matrix[i][j] = distance_matrix[i][relation_matrix[i][j]]

        for i in tqdm(range(numOfSeq)):
            print(i)
            probability_matrix[i] = self.distopro(subdistance_matrix[i])

        return distance_matrix, subdistance_matrix, relation_matrix, probability_matrix

    # print(transform(np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]), 2, 3))

    # Given the ID of the current series, the ID of the next series is generated randomly according to probability
    def next_step(self, relation_array, probability_array):
        value = random.random()
        print(value)
        threshold = [0]
        sum_value = 0
        for i in range(len(probability_array)):
            sum_value = sum_value + probability_array[i]
            threshold.append(sum_value)
        for i in range(len(threshold) - 1):
            if (value > threshold[i] and value <= threshold[i + 1]):
                return relation_array[i]

    # Given a relation matrix and a probability matrix, returns a series of length
    def random_walk(self, relation_matrix, probability_matrix, length, seq):
        # seq=[0]
        temp_id = 0
        for i in range(int(length - 1)):
            temp_id = self.next_step(relation_matrix[temp_id], probability_matrix[temp_id])
            seq.append(temp_id)
            # print(temp_id)
        return seq

    def sigmoid(self, x):
        s = 1 / (1 + np.exp(-x))
        return s

    # data是一个二维数组，每一维表示一个拼接的片段，size为拟合窗口的长度
    def contact(self, data, size):
        result = []
        result = np.array(result)
        colomns = data.shape[1]
        for i in range(data.shape[0]):
            if (i == 0):
                result = np.append(result, data[i][0:colomns - size])
            elif (i > 0 and i < data.shape[0] - 2):
                result = np.append(result, data[i][size:colomns - size])
            else:
                result = np.append(result, data[i][size:])
                break
            for j in range(size):
                temp = (1 - self.sigmoid(self, j)) * data[i][colomns - size + j] + self.sigmoid(self, j) * data[i + 1][
                    j]
                # print(1-sigmoid(j))
                result = np.append(result, temp)
            # print('i:',i,result)
        plt.figure(figsize=(60, 8))
        plt.plot(result, color='blue')
        plt.xlim(0, 26848)
        # plt.xticks([])
        # plt.yticks([])
        plt.savefig('./fake_04.pdf', dpi=600,
                    bbox_inches='tight')
        np.savetxt("./fake_04.txt", result, fmt='%f', delimiter=',')
        return len(result)

    def main_time(self, file):

        time_res = {}
        print('loading data: ')
        data = np.loadtxt(file, delimiter=',')  # generated data with Kalman filter

        file_object = open('/Users/abdel/PycharmProjects/tsgen/results/goldwind/goldwind9216/' + 'time_results.txt',
                           'a')
        file_object.write('nb_fragments' + ',' + 'time_res[nb_fragments]' + '\n')
        file_object.close()

        for nb_fragments in tqdm(range(100, data.shape[0], 100)):
            print("nb_fragments : ", nb_fragments)
            data_to_use = data[:nb_fragments]
            start_time = time.time()

            # for i in range(0):
            #     data = np.concatenate((data, data))

            print(data_to_use.shape)

            seq = [random.randint(0, data_to_use.shape[0])]  # starting series

            a, b, c, d = self.transform(self, data_to_use, 100, 4)

            print(self.random_walk(self, c, d, 100, seq))

            data_con = []
            for i in range(10):
                index = seq[i]
                data_con.append(data_to_use[index])

            data_con = np.array(data_con)
            # data=np.array([[1,2,3,4,5,6],[1,1,4,3,7,8]])
            print(self.contact(self, data_con, 100))
            c = []
            for i in range(10):
                index = seq[i]
                data0 = data_to_use[index].tolist()
                c += data0
            len(c)

            # np.savetxt("pin4_19.txt", c, fmt='%f', delimiter=',')

            time_res[nb_fragments] = float(time.time() - start_time)
            file_object = open('/Users/abdel/PycharmProjects/tsgen/results/goldwind/goldwind9216/' + 'time_results.txt',
                               'a')
            file_object.write(str(nb_fragments) + ',' + str(time_res[nb_fragments]) + '\n')
            file_object.close()

        return time_res
        # datas = pd.read_csv("14_data.csv", header=None)  # real data
        #
        # data4 = datas[4]
        # data4 = data4.tolist()
        #
        # a = data4[400 * 50:400 * 50 + 26848]
        #
        # len(a)
        #
        # plt.figure(figsize=(60, 8))
        # plt.plot(a, color='red')
        # plt.xlim(0, 26848)
        # plt.savefig('real_04.pdf', dpi=600,
        #             bbox_inches='tight')


    def main_n_m(self, data, nb_fragments, exportPath, gen_ts_length, update_percentage, winSize):
        # result_time_name = 'graph-time.txt'
        # file_object = open('graph_result_time.txt', 'a')
        # file_object = open('/Users/abdel/PycharmProjects/tsgen/results/goldwind/goldwind9216/' + 'time_results.txt', 'a')
        # file_object.write('nb_points' + ',' + 'time' + '\n')
        # file_object.close()

        start_time = time.time()
        stream = []

        prev_gen = 0
        # for i in range(0):
        #     data = np.concatenate((data, data))
        print(data.shape)
        seq = [40]  # starting series
        a, b, c, d = self.transformA(data, winSize, 100)
        # a, b, c, d = self.transform(self, data, 100, 4)
        # run_time = {}
        while (True):
            print('loading data: ')
            # while (len(stream) - prev_gen < nb_fragments * winSize * 0.9):
            seq = self.random_walk(c, d, nb_fragments * update_percentage, seq)

            # data_con = []
            # for i in range(10):
            #     index = seq[i]
            #     data_con.append(data[index])
            #
            # data_con = np.array(data_con)
            # # data=np.array([[1,2,3,4,5,6],[1,1,4,3,7,8]])
            # print(self.contact(data_con, 100))

            for i in range(int(nb_fragments * 0.9)):
                index = seq[i]
                data0 = data[index].tolist()
                stream += data0
            print(len(stream))
            # run_time[len(stream)] = time.time() - start_time
            # file_object = open(result_time_name, 'a')
            # file_object.write(str(len(stream)) + ',' + str(time.time() - start_time) + '\n')
            # file_object.close()
            if len(stream)/winSize > gen_ts_length:
                # file_object = open(result_time_name, 'a')
                # file_object.write(str(len(stream)) + ',' + str(time.time() - start_time) + '\n')
                # file_object.close()
                # run_time[len(stream)] = time.time() - start_time
                break
            else:
                # file_object = open(result_time_name, 'a')
                # file_object.write(str(len(stream)) + ',' + str(time.time() - start_time) + '\n')
                # file_object.close()
                # run_time[len(stream)] = time.time() - start_time
                prev_gen = len(stream)
                '''# call GAN'''
                # data = np.loadtxt(file, delimiter=',', encoding='utf-8-sig')  # generated data with Kalman filter
                # data = data.T
                # for i in range(0):
                #     data = np.concatenate((data, data))
                print(data.shape)
                seq = [40]  # starting series
                a, b, c, d = self.transformA(data, nb_fragments, 100)
                # a, b, c, d = self.transform(self, data, 100, 4)
                continue

        np.savetxt(exportPath + "graph-generation.txt", stream, fmt='%f', delimiter=',')

        return time.time() - start_time


    def main_with_update(self, data, nb_fragments, exportPath, gen_ts_length, update_percentage, winSize):
        # result_time_name = 'graph-time.txt'
        # file_object = open('graph_result_time.txt', 'a')
        # file_object = open('/Users/abdel/PycharmProjects/tsgen/results/goldwind/goldwind9216/' + 'time_results.txt', 'a')
        # file_object.write('nb_points' + ',' + 'time' + '\n')
        # file_object.close()

        start_time = time.time()
        stream = []

        prev_gen = 0
        # for i in range(0):
        #     data = np.concatenate((data, data))
        print(data.shape)
        seq = [40]  # starting series
        a, b, c, d = self.transformA(data, winSize, 10)
        # a, b, c, d = self.transform(self, data, 100, 4)
        # run_time = {}
        while (True):
            print('loading data: ')
            # while (len(stream) - prev_gen < nb_fragments * winSize * 0.9):
            seq = self.random_walk(c, d, nb_fragments * update_percentage, seq)

            # data_con = []
            # for i in range(10):
            #     index = seq[i]
            #     data_con.append(data[index])
            #
            # data_con = np.array(data_con)
            # # data=np.array([[1,2,3,4,5,6],[1,1,4,3,7,8]])
            # print(self.contact(data_con, 100))

            for i in range(int(nb_fragments * update_percentage)):
                index = seq[i]
                data0 = data[index].tolist()
                stream += data0
            print(len(stream))
            # run_time[len(stream)] = time.time() - start_time
            # file_object = open(result_time_name, 'a')
            # file_object.write(str(len(stream)) + ',' + str(time.time() - start_time) + '\n')
            # file_object.close()
            if len(stream)/winSize > gen_ts_length:
                # file_object = open(result_time_name, 'a')
                # file_object.write(str(len(stream)) + ',' + str(time.time() - start_time) + '\n')
                # file_object.close()
                # run_time[len(stream)] = time.time() - start_time
                break
            else:
                # file_object = open(result_time_name, 'a')
                # file_object.write(str(len(stream)) + ',' + str(time.time() - start_time) + '\n')
                # file_object.close()
                # run_time[len(stream)] = time.time() - start_time
                '''# call GAN'''
                time.sleep(5)
                # data = np.loadtxt(file, delimiter=',', encoding='utf-8-sig')  # generated data with Kalman filter
                # data = data.T
                # for i in range(0):
                #     data = np.concatenate((data, data))
                print(data.shape)
                seq = [40]  # starting series
                a, b, c, d = self.transformA(data, winSize, 100)
                # a, b, c, d = self.transform(self, data, 100, 4)
                continue

        np.savetxt(exportPath + "graph-generation.txt", stream, fmt='%f', delimiter=',')

        return time.time() - start_time

    def main_without_update(self, data, nb_fragments, exportPath, gen_ts_length, update_percentage, winSize):
        # result_time_name = 'graph-time.txt'
        # file_object = open('graph_result_time.txt', 'a')
        # file_object = open('/Users/abdel/PycharmProjects/tsgen/results/goldwind/goldwind9216/' + 'time_results.txt', 'a')
        # file_object.write('nb_points' + ',' + 'time' + '\n')
        # file_object.close()

        start_time = time.time()
        stream = []

        prev_gen = 0
        # for i in range(0):
        #     data = np.concatenate((data, data))
        print(data.shape)
        seq = [40]  # starting series
        a, b, c, d = self.transformA(data, winSize, 10)
        # a, b, c, d = self.transform(self, data, 100, 4)
        # run_time = {}
        print('loading data: ')
        # while (len(stream) - prev_gen < nb_fragments * winSize * 0.9):
        seq = self.random_walk(c, d, gen_ts_length, seq)
        print(seq)

        # data_con = []
        # for i in range(10):
        #     index = seq[i]
        #     data_con.append(data[index])
        #
        # data_con = np.array(data_con)
        # # data=np.array([[1,2,3,4,5,6],[1,1,4,3,7,8]])
        # print(self.contact(data_con, 100))
        for i in tqdm(range(gen_ts_length)):
            index = seq[i]
            data0 = data[index].tolist()
            stream += data0
        print(len(stream))

        np.savetxt(exportPath + "graph-generation.txt", stream, fmt='%f', delimiter=',')

        return time.time() - start_time

    # datas = pd.read_csv("14_data.csv", header=None)  # real data
    #
    # data4 = datas[4]
    # data4 = data4.tolist()
    #
    # a = data4[400 * 50:400 * 50 + 26848]
    #
    # len(a)
    #
    # plt.figure(figsize=(60, 8))
    # plt.plot(a, color='red')
    # plt.xlim(0, 26848)
    # plt.savefig('real_04.pdf', dpi=600,
    #             bbox_inches='tight')

#
# if __name__ == "__main__":
#     import time
#     start_time = time.time()
#     rw = RandomWalkOri
#     rw.main_time(rw, '/Users/abdel/PycharmProjects/tsgen/results/goldwind/goldwind9216/fake9216.csv')
#     # rw.main(rw, '/Users/abdel/PycharmProjects/tsgen/results/goldwind/goldwind12288/fake12288.csv')
#     print('time: ' + str(time.time() - start_time) + ' sec')
#
