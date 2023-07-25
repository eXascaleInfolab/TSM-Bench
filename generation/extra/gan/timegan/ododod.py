# 3. Metrics


# # plot the data
    # for i in range(len(generated_data[0])):
    #     plt.figure()
    #     plt.subplot(211)
    #     df_ori.iloc[:, i].plot()
    #     plt.subplot(212)
    #     plt.suptitle(dataset_name + " : Real vs. Generated Data", fontsize=14)
    #     df_gen.iloc[:, i].plot()
    #     plt.savefig('results/'+dataset_name+'/'+dataset_name+ str(i)+'.png')


        # plt.savefig('results/'+dataset_name+'/'+dataset_name+'_ori' + str(i)+'.png')
        # # plt.show()
        # plt.close()
        #
        # plt.figure()
        # df_gen.iloc[:, i].plot()
        # plt.savefig('results/' + dataset_name + '/' + dataset_name + '_gen' + str(i) + '.png')
        # # plt.show()
        # plt.close()



# ori_data_ordered = np.array(ori_data_ordered)
# generated_data_ordered = np.array(generated_data_ordered)
#
# print(ori_data_ordered[0, :, 0])
# print()
# print(generated_data_ordered[1, :, 0])
# print(ori_data[0][-1][0] == ori_data[1][0][0])


# print(len(ori_data[0]))
# print(len(ori_data[0][0]))


# for i in range(len(ori_data)):
#     for j in range(len(ori_data[0][0])):
#         plt.plot(ori_data[i][:][j])
#         plt.plot(generated_data[i][:][j])
#         plt.show()

# visualization(ori_data, generated_data, 'pca')
# visualization(ori_data, generated_data, 'tsne')

# pickle.dump(ori_data, f)
# pickle.dump(generated_data, f)
# pickle.dump(metrics, f)
# print(testout1)
# print(testout2)


# data = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
# idx = np.random.permutation(len(data))
# # print('idx = ', idx)
# new_data = []
# for i in range(len(data)):
#     new_data.append(data[idx[i]])
#
# print(new_data)
#
# ori_data = []
# for i in range(len(data)):
#     ori_data.append(new_data[idx.tolist().index(i)])
# print(ori_data)


# with open('result.pickle', 'wb') as f:
#     pickle.dump(['[[vs[sv'], f)
#     pickle.dump(['[[vs[sv'], f)
#     pickle.dump(['[[vs[sv'], f)


## Performance metrics
# Output initialization
metric_results = dict()

# 1. Discriminative Score
# discriminative_score = list()
# print('discriminative_score')
# for _ in range(10):
#     temp_disc = discriminative_score_metrics(ori_data, generated_data)
#     discriminative_score.append(temp_disc)
#     print(temp_disc)
#
# metric_results['discriminative'] = np.mean(discriminative_score)

# # 2. Predictive score
# predictive_score = list()
# print('predictive_score')
# for tt in range(10):
#     temp_pred = predictive_score_metrics(ori_data, generated_data)
#     predictive_score.append(temp_pred)
#     print(temp_pred)
#
# metric_results['predictive'] = np.mean(predictive_score)
#
# # 3. Visualization (PCA and tSNE)
# visualization(ori_data, generated_data, 'pca')
# # visualization(ori_data, generated_data, 'tsne')
#
# ## Print discriminative and predictive scores
# print(metric_results)
#


# visualization(ori_data_ordered, generated_data_ordered, 'tsne')
# visualization(ori_data_ordered, generated_data_ordered, 'pca')
