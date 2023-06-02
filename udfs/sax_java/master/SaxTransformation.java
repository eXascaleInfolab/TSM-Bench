package master;

import java.util.*;
import java.lang.*;

public class SaxTransformation {
	public static void main(String[] args) {
		double[][] data = new double[][] {
			{1, 2, 3}, {2, 5, 10}, {3, 1, 11}
		};
		List<String> result = saxrepresentation(data);
		for (int i = 0; i < result.size(); ++i) 
			System.out.println(result.get(i));
	}

	public static List<String> saxrepresentation(double[][] data) {
		List<String> result = new ArrayList<String>();
		int rows = data.length;
		int columns = data[0].length;
		for (int j = 0; j < columns; ++j) {
			List<Double> timeSeries = new ArrayList<Double>();
			for (int i = 0; i < rows; ++i) {
				timeSeries.add(data[i][j]);
			}
			List<Double> norm = znorm(timeSeries, 0.01);
			List<Double> paa = paa(norm, 3);
			String a = ts_to_string(paa, cuts_for_asize(3));
			result.add(a);
		}
		return result;
	}

	public static List<Double> znorm(List<Double> series, double znorm_threshold) {
		double mean = 0.0;
		for (Double x : series)
			mean += x;
		mean /= series.size();
		
		double std = 0.0;
		for (Double x : series)
			std += (x - mean) * (x - mean);
		std = Math.sqrt(std / series.size());
		
		if (std < znorm_threshold) {
			return series;
		}

		List<Double> ans = new ArrayList<Double>();
		for (Double x : series) {
			ans.add( (x - mean) / std );
		}
		return ans;
	}

	public static List<Double> cuts_for_asize(int a_size) {
		switch(a_size) {
			case 2: return new ArrayList<Double>(Arrays.<Double>asList(Double.NEGATIVE_INFINITY, 0.0));
			case 3: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -0.4307273, 0.4307273 ));
			case 4: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -0.6744898, 0.0, 0.6744898));
			case 5: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -0.841621233572914, -0.2533471031358, 0.2533471031358, 0.841621233572914));
			case 6: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -0.967421566101701, -0.430727299295457, 0, 0.430727299295457, 0.967421566101701));
			case 7: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY,-1.06757052387814, -0.565948821932863, -0.180012369792705, 0.180012369792705, 0.565948821932863, 1.06757052387814));
			case 8: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -1.15034938037601, -0.674489750196082, -0.318639363964375, 0, 0.318639363964375, 0.674489750196082, 1.15034938037601));			
			case 9: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -1.22064034884735, -0.764709673786387, -0.430727299295457, -0.139710298881862, 0.139710298881862, 0.430727299295457, 0.764709673786387, 1.22064034884735));
			case 10: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -1.2815515655446, -0.841621233572914, -0.524400512708041, -0.2533471031358, 0, 0.2533471031358, 0.524400512708041, 0.841621233572914, 1.2815515655446));
			default: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY));
		}
	}

	public static List<Double> paa(List<Double> series, int paa_size) {
		if (series.size() == paa_size) {
			return new ArrayList<Double>(series);
		}

		ArrayList<Double> res = new ArrayList<Double>();
		for (int i = 0; i < paa_size; ++i)
			res.add(0.0);

		if (series.size() % paa_size == 0) {
			int inc = series.size() / paa_size;
			for (int i = 0; i < series.size(); ++i) {
				int idx = i / inc;
				res.set(idx, res.get(idx) + series.get(i));
			}
			for (int i = 0; i < paa_size; ++i)
				res.set(i, res.get(i) / inc);
		} else {
			for (int i = 0; i < series.size() * paa_size; ++i) {
				int idx = i / series.size();
				int pos = i / paa_size;
				res.set(idx, res.get(idx) + series.get(pos));
			}
			for (int i = 0; i < paa_size; ++i)
				res.set(i, res.get(i) / series.size());
		}
		return res;
	}

	public static char idx2letter(int idx) {
		return (char) ('a' + idx);
	}

	public static String ts_to_string(List<Double> series, List<Double> cuts) {
		StringBuilder res = new StringBuilder();
	
		for (int i = 0; i < series.size(); ++i) {
			double num = series.get(i);
			if (num >= 0.0) {
				int j = cuts.size() - 1;
				while (j > 0 && cuts.get(j) >= num) {
					--j;
				}
				res.append(idx2letter(j));
			} else {
				int j = 1;
				while (j < cuts.size() && cuts.get(j) <= num) {
					++j;
				}
				res.append(idx2letter(j - 1));
			}
		}
		return res.toString();
	}
}
