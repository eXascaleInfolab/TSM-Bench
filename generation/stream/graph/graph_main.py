import random
import matplotlib.image as mpimg
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import pandas as pd
import time
from tqdm import tqdm
from stream.graph.random_walk import RandomWalk


class Graph_conca:

    # def graph_augment(self, res, seq_length, sim_thresh, head_tail_length, argmax, walk_length):
    #
    #     # build nodes
    #     G = nx.DiGraph()
    #     for i in range(len(res)):
    #         G.add_node(i, seq=res[i])
    #         print(G.nodes[i]['seq'])
    #         plt.axis('off')
    #         plt.plot(res[i], color='black')
    #         plt.savefig('node_fig'+str(i)+'.png')
    #         img=mpimg.imread('node_fig'+str(i)+'.png')
    #         G.add_node(i, img=img)
    #         plt.clf()
    #         os.remove('node_fig'+str(i)+'.png')
    #
    #     # iterate over the nodes
    #     for u, u_att in G.nodes(data=True):
    #         list_neighbors = {}
    #         list_all = {}
    #         sum_sim = 0
    #         # find the edges weights
    #         for v, v_att in G.nodes(data=True):
    #             if u != v:
    #                 sim_u_v = self._sim(u_att['seq'][-head_tail_length:], v_att['seq'][:head_tail_length], head_tail_length)
    #                 list_all[v] = sim_u_v
    #                 if sim_u_v > sim_thresh:
    #                     list_neighbors[v] = sim_u_v
    #
    #         # if no neighbors found
    #         if not bool(list_neighbors):
    #             max_value_keys = [key for key in list_all.keys() if
    #                               list_all[key] in sorted(list_all.values(), reverse=True)[:argmax]]
    #             for i in max_value_keys:
    #                 list_neighbors[i] = list_all[i]
    #
    #         # build the weighted edges
    #         for v in list_neighbors:
    #             G.add_edge(u, v, weight=(list_neighbors[v] - sim_thresh) / (sum_sim - sim_thresh))
    #
    #     self.plot_graph(G)
    #
    #     from random_walk import RandomWalk
    #
    #     random_walk = RandomWalk(G, walk_length=walk_length, num_walks=1, p=1, q=1, weight_key= 'weight', workers=1)
    #
    #     walklist = random_walk.walks
    #
    #     # for w in walklist:
    #     #     print(w)
    #
    #     w = walklist[0]
    #     generated_sequence = list(G.nodes[w[0]]['seq'])
    #     for i in range(1, len(w)):
    #         generated_sequence.extend(G.nodes[w[i]]['seq'])
    #         a_t = generated_sequence[int(-seq_length - head_tail_length/2 ) : - seq_length]
    #         b_t = generated_sequence[- seq_length : int(-seq_length + head_tail_length/2 )]
    #         generated_sequence[int(-seq_length - head_tail_length/2 ) : -seq_length] = fit(a_t, b_t)
    #         del generated_sequence[-seq_length: int( -seq_length + head_tail_length/2)]
    #         # print(G.nodes[w[i]]['seq'])
    #
    #     return generated_sequence

    def graph_main(self, nb_ts, gen_path, export_path, window_size, tr_sampling_size, sim_thresh, argmax, head_tail_length,
                   gen_ts_length, nb_fragments):

        export_path += 'graph/'

        graphs = []
        tr_sampling_size = max(window_size, tr_sampling_size)
        gen_ts_length = max(1, gen_ts_length)
        gen_ts_length = tr_sampling_size * gen_ts_length
        walk_length = int(gen_ts_length / window_size) + 1

        start_Graph = time.time()

        # building graphs
        print('creating graphs (nodes + edges)...')
        for ts_index in tqdm(range(nb_ts)):
            res = pd.read_csv(gen_path + 'fake' + str(ts_index) + '.csv')
            res = res.T.values.tolist()[:nb_fragments]
            graphs.append(self.graph_create(res, head_tail_length, sim_thresh, argmax))

        print('done\n generating data with random walk')

        for i in range(len(graphs)):
            gen = self.graph_generate(graphs[i], window_size, walk_length, head_tail_length)
            np.savetxt(export_path + "fake_long" + str(i) + ".csv", np.array(gen), delimiter=",")

        # file_object = open(export_path+'time_results.txt', 'a')
        # file_object.write("\n--- Graph Time: %s seconds ---" % (time.time() - start_Graph))
        # file_object.close()
        Graph_time = time.time() - start_Graph
        print("--- Graph Time: %s seconds ---" % (Graph_time))
        # generated_data = self.graph_augment(res, seq_length, sim_thresh, head_tail_length, argmax)
        # print(len(generated_data))

        # generating data with random walk
        return Graph_time

    def graph_generate(self, G, seq_length, walk_length, head_tail_length):

        random_walk = RandomWalk(G, walk_length=walk_length, num_walks=1, p=1, q=1, weight_key='weight', workers=1)

        walklist = random_walk.walks

        w = walklist[0]
        generated_sequence = list(G.nodes[w[0]]['seq'])
        for i in range(1, len(w)):
            generated_sequence.extend(G.nodes[w[i]]['seq'])
            a_t = generated_sequence[int(-seq_length - head_tail_length / 2): - seq_length]
            b_t = generated_sequence[- seq_length: int(-seq_length + head_tail_length / 2)]
            generated_sequence[int(-seq_length - head_tail_length / 2): -seq_length] = self._fit(a_t, b_t)
            del generated_sequence[-seq_length: int(-seq_length + head_tail_length / 2)]
            # print(G.nodes[w[i]]['seq'])
        return generated_sequence

    def graph_create(self, res, head_tail_length, sim_thresh, argmax):
        # build nodes
        G = nx.DiGraph()
        for i in range(len(res)):
            G.add_node(i, seq=res[i])
            # print(G.nodes[i]['seq'])

            # plt.axis('off')
            # plt.plot(res[i], color='black')
            # plt.savefig('node_fig'+str(i)+'.png')
            # img=mpimg.imread('node_fig'+str(i)+'.png')
            # G.add_node(i, img=img)
            # G.add_node(i)
            # plt.clf()
            # os.remove('node_fig'+str(i)+'.png')

        # iterate over the nodes
        for u, u_att in tqdm(G.nodes(data=True)):
            list_neighbors = {}
            list_all = {}
            sum_sim = 0
            # find the edges weights
            for v, v_att in G.nodes(data=True):
                if u != v:
                    sim_u_v = self._sim(u_att['seq'][-head_tail_length:], v_att['seq'][:head_tail_length],
                                        head_tail_length)
                    list_all[v] = sim_u_v
                    if sim_u_v > sim_thresh:
                        list_neighbors[v] = sim_u_v

            # if no neighbors found
            if not bool(list_neighbors):
                max_value_keys = [key for key in list_all.keys() if
                                  list_all[key] in sorted(list_all.values(), reverse=True)[:argmax]]
                for i in max_value_keys:
                    list_neighbors[i] = list_all[i]

            # build the weighted edges
            for v in list_neighbors:
                G.add_edge(u, v, weight=(list_neighbors[v] - sim_thresh) / (sum_sim - sim_thresh))

        # self.plot_graph(G)

        return G

    # def _main(self):
    #     res = []
    #     seq_length = 8
    #     sim_thresh = 1 / 2
    #     walk_length = 10
    #     head_tail_length = 4
    #     argmax = 2
    #     for i in range(10):
    #         res.append([random.randint(0, 22) for j in range(seq_length)])
    #     # print(res)
    #
    #     generated_data =self.graph_augment(res, seq_length, sim_thresh, head_tail_length, argmax)
    #     print(len(generated_data))

    def _sim(self, a, b, head_tail_length):
        sum = 0
        for i in range(head_tail_length):
            sum += (np.linalg.norm(a[i] - b[i]))
        return 1 / sum

    def _fit(self, a, b):
        c = []
        for i in range(len(a)):
            sigma_i = 1 / (1 + math.exp(-i))
            c.append((1 - sigma_i) * a[i] + sigma_i * b[i])
        return c

    def _plot_graph(self, G):
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(G)

        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
        plt.savefig('graph.png')

    def plot_with_image(self, G):
        pos = nx.circular_layout(G)

        fig = plt.figure(figsize=(15, 15))
        ax = plt.subplot(111)
        ax.set_aspect('equal')
        nx.draw_networkx_edges(G, pos, ax=ax)

        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)

        trans = ax.transData.transform
        trans2 = fig.transFigure.inverted().transform

        piesize = 0.05  # this is the image size
        p2 = piesize / 2.0
        for n in G:
            xx, yy = trans(pos[n])  # figure coordinates
            xa, ya = trans2((xx, yy))  # axes coordinates
            a = plt.axes([xa - p2, ya - p2, piesize, piesize])
            a.set_aspect('equal')
            a.imshow(G.nodes[n]['img'])
            a.axis('off')
        ax.axis('off')
        plt.show()
