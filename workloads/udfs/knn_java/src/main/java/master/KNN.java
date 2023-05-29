package master;

import java.util.*;
import java.lang.*;

public class KNN {
	public static void main(String[] args) {
		List<List<Double>> l_data = Arrays.asList(
			Arrays.asList(1.0, 1.0),
			Arrays.asList(2.0, 2.0),
			Arrays.asList(3.0, 3.0),
			Arrays.asList(4.0, 4.0),
			Arrays.asList(-1.0, -1.0),
			Arrays.asList(-2.0, -2.0),
			Arrays.asList(-3.0, -3.0),
			Arrays.asList(-4.0, -4.0)
		);
		List<Integer> l_labels = Arrays.asList(1,1,1,1,2,2,2,2);
		List<List<Double>> u_data = Arrays.asList(
			Arrays.asList(0.0, 0.0),
			Arrays.asList(10.0, 10.0),
			Arrays.asList(-10.0, -10.0),
			Arrays.asList(-1.0, 2.0),
			Arrays.asList(0.0, 1.0)
		);
		List<Integer> u_labels = knn(l_data, l_labels, u_data, 3);
		System.out.println(Arrays.toString(u_labels.toArray()));
	}

	public static List<Integer> knn(List<List<Double>> label_matrix, List<Integer> labels, List<List<Double>> unlabel_matrix, int k) {
		int n_unlabel = unlabel_matrix.size();
		List<Integer> result = new ArrayList<Integer>();
		for(int i = 0; i < n_unlabel; i++){
			result.add(knn_single(label_matrix, labels, unlabel_matrix.get(i), k));
		}		
		return result;
	}

	public static Integer knn_single(List<List<Double>> label_matrix, List<Integer> labels, List<Double> datapoint, int k) {
		//getting the number of labeled data
		int n_label = label_matrix.size();
		PriorityQueue<KNNItem> a = new PriorityQueue<KNNItem>( (x, y) -> {
			if (x.distance > y.distance) return -1;
			if (x.distance < y.distance) return 1;
			return 0;
		});
		for(int i = 0; i < n_label; i++){
			a.add(new KNNItem(distance(label_matrix.get(i), datapoint), labels.get(i)));
			while(a.size() > k)
				a.poll();
		}
		HashMap<Integer, Integer> count = new HashMap<Integer, Integer>();
		Integer mostFrequentLabel = null;
		while(a.size() > 0){
			int label = a.poll().label;
			if(count.containsKey(label))
				count.put(label, count.get(label) + 1);
			else
				count.put(label, 1);
			if(mostFrequentLabel == null || count.get(label) > count.get(mostFrequentLabel) )
				mostFrequentLabel = label;
		}
		return mostFrequentLabel;
	}

	public static Double distance(List<Double> a, List<Double> b){
		double ans = 0.0;
                for (int i = 0; i < a.size(); ++i) {
	                ans += (a.get(i) - b.get(i)) * (a.get(i) - b.get(i));
                }
                return Math.sqrt(ans);
	}
}
