package master;

import java.util.Random;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class KMeans {
	public static void main(String[] args) {
		double[][] datapoints = {
			{-10, -10}, {-9, -9}, {-10, -9}, {-9, -10},
			{10, 10}, {9, 9}, {10, 9}, {9, 10}
		};

		double[][] clusters = kmeans(datapoints, 2, 10);
		for (int i = 0; i < clusters.length; ++i) {
			for (int j = 0; j < clusters[i].length; ++j) {
				System.out.print(clusters[i][j]);
				System.out.print(" ");
			}
			System.out.println();
		}
	}

	private static double distance(double[] datapoint, double[] cluster) {
		double result = 0;
		for (int i = 0; i < datapoint.length; ++i) {
			result = result + (datapoint[i] - cluster[i]) * (datapoint[i] - cluster[i]);
		}
		return result;
	}

	public static double[][] kmeans(double[][] datapoints, int clusterCount, int iterations) {
		int rows = datapoints.length;
		int columns = datapoints[0].length;

		double[][] clusters = new double[clusterCount][columns];
		Random random = new Random();


		List<List<Double>> cpy = new ArrayList<List<Double>>();		
		for (int i = 0; i < rows; ++i) {
			List<Double> currentList = new ArrayList<Double>();
			for (int j = 0; j < columns; ++j) {
				currentList.add(datapoints[i][j]);
			}
			cpy.add(currentList);
		}
		Collections.shuffle(cpy, random);
		for (int i = 0; i < clusterCount; ++i) {
			for (int j = 0; j < columns; ++j) {
				clusters[i][j] = cpy.get(i).get(j);
			}
		}

		for (int it = 0; it < iterations; ++it) {
			double[][] sumClusters = new double[clusterCount][columns];
			double[] countClusters = new double[clusterCount];

			for (int i = 0; i < rows; ++i) {
				int closestCluster = 0;
				double closestDistance = distance(datapoints[i], clusters[0]);
				for (int j = 1; j < clusterCount; ++j) {
					double clusterDistance = distance(datapoints[i], clusters[j]);
					if (clusterDistance < closestDistance) {
						closestDistance = clusterDistance;
						closestCluster = j;
					}
				}

				for (int j = 0; j < columns; ++j) {
					sumClusters[closestCluster][j] += datapoints[i][j];
				}
				countClusters[closestCluster]++;
			}
			for (int i = 0; i < clusterCount; ++i) {
				if (countClusters[i] == 0) {
					int newCluster = random.nextInt(rows);
					for (int j = 0; j < columns; ++j) {
						clusters[i][j] = datapoints[newCluster][j];
					}
				} else {
					for (int j = 0; j < columns; ++j) {
						clusters[i][j] = sumClusters[i][j] / countClusters[i];
					}
				}
			}

		}

		return clusters;
	}
}
