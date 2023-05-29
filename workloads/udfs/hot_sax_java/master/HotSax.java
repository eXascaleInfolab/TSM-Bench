package master;

import java.util.*;
import java.lang.*;

public class HotSax {
	public static void main(String[] args) {
		ArrayList<Double> series = new ArrayList<Double>(Arrays.asList(0., 0., 0., 0., 0., -0.270340178359072, -0.367828308500142,
            0.666980581124872, 1.87088147328446, 2.14548907684624,
            -0.480859313143032, -0.72911654245842, -0.490308602315934,
            -0.66152028906509, -0.221049033806403, 0.367003418871239,
            0.631073992586373, 0.0487728723414486, 0.762655178750436,
            0.78574757843331, 0.338239686422963, 0.784206454089066,
            -2.14265084073625, 2.11325193044223, 0.186018356196443,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.519132472499234,
            -2.604783141655, -0.244519550114012, -1.6570790528784,
            3.34184602886343, 2.10361226260999, 1.9796808733979,
            -0.822247322003058, 1.06850578033292, -0.678811824405992,
            0.804225748913681, 0.57363964388698, 0.437113583759113,
            0.437208643628268, 0.989892093383503, 1.76545983424176,
            0.119483882364649, -0.222311941138971, -0.74669456611669,
            -0.0663660879732063, 0., 0., 0., 0., 0.));
		print(series);

		Map<String, List<Integer>> sax = sax_via_window(series, 6, 3, 3, 0.01);
		for (Map.Entry<String, List<Integer>> entry : sax.entrySet()) {
			System.out.print(entry.getKey() + " ---> ");
			print(entry.getValue());
		}

		List<Discord> best = find_discords_hotsax(series, 6, 3, 3, 3, 0.01);
		print(best);
	}

	public static List<Discord> find_discords_hotsax(List<Double> series, int win_size, int num_discords, int a_size, int paa_size, double znorm_threshold) {
		List<Discord> discords = new ArrayList<Discord>();
		Set<Integer> global_registry = new HashSet<Integer>();
		while (discords.size() < num_discords) {
			Discord best_discord = find_best_discord_hotsax(series, win_size, a_size, paa_size, znorm_threshold, global_registry);
			if (best_discord.position == -1) {
				break;
			}
			discords.add(best_discord);
			int mark_start = best_discord.position - win_size;
			if (mark_start < 0) {
				mark_start = 0;
			}
			int mark_end = best_discord.position + win_size;
			for (int i = mark_start; i < mark_end; ++i) {
				global_registry.add(i);
			}
		}
		return discords;
	} 

	public static Discord find_best_discord_hotsax(List<Double> series, int win_size, int a_size, int paa_size, double znorm_threshold, Set<Integer> globalRegistry) {
		Map<String, List<Integer>> sax_none = sax_via_window(series, win_size, a_size, paa_size, znorm_threshold);
		List<String> magic_array = new ArrayList<String>(sax_none.keySet());
		Collections.sort(magic_array, new Comparator<String>() {
			public int compare(String a, String b) {
				// Need to sort by length of list. Return difference between sizes.
				// If length of a is smaller, then compare returns negative number
				// If length of a is larger, then compare returns positive number
				// If length of a is equal to b, then compare return 0.
				// This is exactly what compare needs to return.
				return (sax_none.get(a).size() - sax_none.get(b).size());
			}
		});

		int bestSoFarPosition = -1;
		double bestSoFarDistance = 0.0;
		
		for (String curr_word : magic_array) {
			List<Integer> occurrences = sax_none.get(curr_word);
			for (Integer curr_pos : occurrences) {
				if (globalRegistry.contains(curr_pos)) {
					continue;
				}
				int mark_start = curr_pos - win_size;
				int mark_end = curr_pos + win_size;
				Set<Integer> visit_set = new HashSet<Integer>();
				for (int i = mark_start; i < mark_end; ++i) visit_set.add(i);
				
				List<Double> cur_seq = znorm( series.subList(curr_pos, curr_pos + win_size), znorm_threshold);
				double nn_dist = Double.POSITIVE_INFINITY;
				boolean do_random_search = true;

				for (Integer next_pos : occurrences) {
					if (visit_set.contains(next_pos)) {
						continue;
					} else {
						visit_set.add(next_pos);
					}

					double dist = euclidean(cur_seq, znorm( series.subList(next_pos, next_pos + win_size), znorm_threshold) );
					if (dist < nn_dist) {
						nn_dist = dist;
					}
					if (dist < bestSoFarDistance) {
						do_random_search = false;
						break;
					}
				}

				if (do_random_search) {
					List<Integer> visit_array = new ArrayList<Integer>();
					for (int i = 0; i < series.size() - win_size; ++i) {
						if (!visit_set.contains(i)) {
							visit_array.add(i);
						}
					}
					Collections.shuffle(visit_array);
					for (int curr_idx = visit_array.size() - 1; curr_idx >= 0; --curr_idx) {
						int rand_pos = visit_array.get(curr_idx);
						double dist = euclidean( cur_seq, znorm( series.subList(rand_pos, rand_pos + win_size), znorm_threshold) );
						if (dist < nn_dist) {
							nn_dist = dist;
						}
						if (dist < bestSoFarDistance) {
							nn_dist = dist;
							break;
						}
					}
				}
				if (nn_dist > bestSoFarDistance && nn_dist < Double.POSITIVE_INFINITY) {
					bestSoFarDistance = nn_dist;
					bestSoFarPosition = curr_pos;
				}
			}
		}
		return new Discord(bestSoFarDistance, bestSoFarPosition);
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

	public static double euclidean(List<Double> a, List<Double> b) {
		double ans = 0.0;
		for (int i = 0; i < a.size(); ++i) {
			ans += (a.get(i) - b.get(i)) * (a.get(i) - b.get(i));
		}
		return Math.sqrt(ans);
	}

	public static List<Double> cuts_for_asize(int a_size) {
		switch(a_size) {
			case 2: return new ArrayList<Double>(Arrays.<Double>asList(Double.NEGATIVE_INFINITY, 0.0));
			case 3: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -0.4307273, 0.4307273 ));
			case 4: return new ArrayList<Double>(Arrays.asList(Double.NEGATIVE_INFINITY, -0.6744898, 0.0, 0.6744898));
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

	public static Map<String, List<Integer>> sax_via_window(List<Double> series, int win_size, int paa_size, int alphabet_size, double z_threshold) {
		List<Double> cuts = cuts_for_asize(alphabet_size);
		Map<String, List<Integer>> sax = new HashMap<String, List<Integer>>();

		for (int i = 0; i < series.size() - win_size; ++i) {
			List<Double> sub_section = series.subList(i, i + win_size);
			List<Double> zn = znorm(sub_section, z_threshold);
			List<Double> paa_rep = paa(zn, paa_size);
			String curr_word = ts_to_string(paa_rep, cuts);

			if (!sax.containsKey(curr_word)) {
				sax.put(curr_word, new ArrayList<Integer>());
			}
			sax.get(curr_word).add(i);
		}
		return sax;
	}

	private static <T> void print(List<T> l) {
		System.out.println(Arrays.toString(l.toArray()));
	}
}
