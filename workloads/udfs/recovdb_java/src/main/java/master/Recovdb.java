package master;

import org.apache.commons.math3.linear.*;
import java.util.ArrayList;

public class Recovdb {
	public static void main(String[] args) {
		System.out.println("\n\n\n***********************************************************************\n");
		Array2DRowRealMatrix input = new Array2DRowRealMatrix(
			new double[][]{ {1, 2, 3}, {4, Double.NaN, Double.NaN}, {7, 8, 9}, {10, 11, 12}}
		);
		Array2DRowRealMatrix z = new Array2DRowRealMatrix(
			new double[][]{ {1, 1, 1}, {1, 1, 1}, {1, -1, 1}, {1, -1, 1}}
		);
		System.out.println(input.toString());
		System.out.println(recovery(input, 2, 0, 0).toString());


		System.out.println("\n***********************************************************************\n\n\n");
	}


	public static RealMatrix recovery(RealMatrix matrix, int trunc_col, double perc, int col_drop) {
		int n = matrix.getRowDimension();
		int m = matrix.getColumnDimension();
		RealMatrix x_tilde = matrix.copy();
		
		for (int perc_col = 0; perc_col < col_drop; ++perc_col) {
			for (int i = (int) ((perc_col * perc * n) - (perc_col * 0.05 * n));
				i < (int) (((perc_col + 1) * perc * n) - (perc_col * 0.05 * n));
				++i) {
				if (i < 0 || i >= n) continue;
				x_tilde.setEntry(i, perc_col, Double.NaN);
			}
		}

		int[] missing_rows = get_missing_rows(x_tilde);
		int[] missing_cols = get_missing_rows(x_tilde.transpose());
		for (int i = 0; i < m; ++i)
			x_tilde = linear_interpolated_base_series_values(x_tilde, i);

		
		CentroidDecompositionResult cd_r = CD(x_tilde, m - trunc_col);
		RealMatrix result = zcd_recovery(x_tilde, trunc_col, missing_rows, missing_cols, cd_r.z);
		return result;
	} 

	public static RealMatrix linear_interpolated_base_series_values(RealMatrix matrix, int column) {
		int n = matrix.getRowDimension();
		int m = matrix.getColumnDimension();

		int mb_start = -1;
		double prev_value = Double.NaN;
		double step = 0;
		for (int i = 0; i < n; ++i) {
			if (Double.isNaN(matrix.getEntry(i, column))) {				
				if (mb_start == -1) {
					mb_start = i;
					int mb_end = mb_start + 1;
					while ( (mb_end < n) && Double.isNaN(matrix.getEntry(mb_end, column)))
						mb_end++;
					double next_value = Double.NaN;
					if (mb_end < n)
						next_value = matrix.getEntry(mb_end, column);
					if (mb_start == 0)
						prev_value = next_value;
					step = (next_value - prev_value) / (mb_end - mb_start + 1);
				}
				matrix.setEntry(i, column, prev_value + step * (i - mb_start + 1));
			} else {
				prev_value = matrix.getEntry(i, column);
				mb_start = -1;
			}
		}
		return matrix;
	}
	public static RealMatrix zcd_recovery(RealMatrix x, int trunc_col, int[] missing_rows, 
						int[] missing_cols, RealMatrix z) {
		int n = x.getRowDimension();
		int m = x.getColumnDimension();

		RealMatrix previous_recovered = new Array2DRowRealMatrix(n, m);
		int iteration = 1;
		while ( previous_recovered.getSubMatrix(missing_rows, missing_cols)
						.subtract( x.getSubMatrix(missing_rows, missing_cols) )
						.getFrobeniusNorm() / missing_rows.length > 1.0 &&
			iteration < 200) {
			
			iteration++;
			previous_recovered = x.copy();
			CentroidDecompositionResult r = ZCD(x, z, m - trunc_col);
			RealMatrix x_new = r.L.multiply(r.R.transpose());
			setSubMatrix(x, missing_rows, missing_cols, x_new.getSubMatrix(missing_rows, missing_cols));
		}
		return x;
	}

	public static CentroidDecompositionResult ZCD(RealMatrix matrix, RealMatrix z, int k) {
		int n = matrix.getRowDimension();
		int m = matrix.getColumnDimension();

		CentroidDecompositionResult result = new CentroidDecompositionResult();
		result.L = new Array2DRowRealMatrix(n, m);
		result.R = new Array2DRowRealMatrix(m, m);
		result.z = z;

		for (int i = 0; i < k; ++i) {
			double norm = matrix.transpose().multiply( result.z.getColumnMatrix(i) ).getFrobeniusNorm();
			result.R.setColumnMatrix(i,
                                matrix.transpose().multiply( result.z.getColumnMatrix(i) ).scalarMultiply(1.0 / norm) );
			result.L.setColumnMatrix(i,
                                matrix.multiply( result.R.getColumnMatrix(i) ) );
			matrix = matrix.subtract(
                                result.L.getColumnMatrix(i).multiply( result.R.getColumnMatrix(i).transpose() ) );
		}
		return result;
	}

	public static CentroidDecompositionResult CD(RealMatrix matrix, int k) {
		int n = matrix.getRowDimension();
		int m = matrix.getColumnDimension();

		CentroidDecompositionResult result = new CentroidDecompositionResult();
		result.L = new Array2DRowRealMatrix(n, m);
		result.R = new Array2DRowRealMatrix(m, m);
		result.z = new Array2DRowRealMatrix(n, m);

		for (int i = 0; i < k; ++i) {
			result.z.setColumnMatrix(i, SSV_init(matrix) );

			double norm = matrix.transpose().multiply( result.z.getColumnMatrix(i) ).getFrobeniusNorm();
			if (norm <= 0.0)
				break;
			
			result.R.setColumnMatrix(i, 
				matrix.transpose().multiply( result.z.getColumnMatrix(i) ).scalarMultiply(1.0 / norm) );
			result.L.setColumnMatrix(i,
				matrix.multiply( result.R.getColumnMatrix(i) ) );
			matrix = matrix.subtract( 
				result.L.getColumnMatrix(i).multiply( result.R.getColumnMatrix(i).transpose() ) );
		}
		return result;
	}

	public static RealMatrix SSV(RealMatrix x) {
		int n = x.getRowDimension();
		int m = x.getColumnDimension();

		int pos = -1;
		RealMatrix z = ones(n, 1);
		RealMatrix v = x.multiply( ones(1, n).multiply(x).transpose() ).subtract(
				pointwiseMultiplication(x, x).multiply( ones(m, 1) )
			);
		boolean var_bool = true;
		while (var_bool || (pos != -1)) {
			var_bool = false;
			if (pos != -1) {
				z.setEntry(pos, 0, z.getEntry(pos, 0) * -1);
				v = v.add( x.multiply( x.getRowMatrix(pos).transpose() )
						.scalarMultiply(2.0 * z.getEntry(pos, 0)) );
				v.setRowMatrix(
					pos,
					v.getRowMatrix(pos)
						.subtract(x.getRowMatrix(pos)
								.multiply(x.getRowMatrix(pos).transpose())
								.scalarMultiply( 2.0 * z.getEntry(pos, 0))));
			}
			RealMatrix val = pointwiseMultiplication(z, v);
			
			int argmin = 0;
			for (int i = 0; i < n; ++i)
				if (val.getEntry(i, 0) < val.getEntry(argmin, 0)) {
					argmin = i;
				}
			if (val.getEntry(argmin, 0) < 0) {
				pos = argmin;
			} else {
				pos = -1;
			}
		}
				
		
		return z;
	}

        public static RealMatrix SSV_init(RealMatrix x) {
                int n = x.getRowDimension();
                int m = x.getColumnDimension();

                int pos = -1;
                RealMatrix z = LSV(x);
                RealMatrix v = x.multiply( ones(1, n).multiply(x).transpose() ).subtract(
                                pointwiseMultiplication(x, x).multiply( ones(m, 1) )
                        );
                boolean var_bool = true;
                while (var_bool || (pos != -1)) {
                        var_bool = false;
                        if (pos != -1) {
                                z.setEntry(pos, 0, z.getEntry(pos, 0) * -1);
                                v = v.add( x.multiply( x.getRowMatrix(pos).transpose() )
                                                .scalarMultiply(2.0 * z.getEntry(pos, 0)) );
                                v.setRowMatrix(
                                        pos,
                                        v.getRowMatrix(pos)
                                                .subtract(x.getRowMatrix(pos)
                                                                .multiply(x.getRowMatrix(pos).transpose())
                                                                .scalarMultiply( 2.0 * z.getEntry(pos, 0))));
                        }
                        RealMatrix val = pointwiseMultiplication(z, v);

                        int argmin = 0;
                        for (int i = 0; i < n; ++i)
                                if (val.getEntry(i, 0) < val.getEntry(argmin, 0)) {
                                        argmin = i;
                                }
                        if (val.getEntry(argmin, 0) < 0) {
                                pos = argmin;
                        } else {
                                pos = -1;
                        }
                }


                return z;
        }

	public static RealMatrix LSV(RealMatrix x) {
		int n = x.getRowDimension();
		int m = x.getColumnDimension();

		RealMatrix D = x.getRowMatrix(0);
		RealMatrix z = ones(n, 1);

		for (int i = 1; i < n; ++i) {
			double change_plus = D.add( x.getRowMatrix(i) ).getFrobeniusNorm();
			change_plus = change_plus * change_plus;
			double change_minus = D.subtract( x.getRowMatrix(i) ).getFrobeniusNorm();
			change_minus = change_minus * change_minus;
			if (change_plus < change_minus)
				z.setEntry(i, 0, -1.0);
			D = D.add( x.getRowMatrix(i).scalarMultiply( z.getEntry(i, 0) ) );
		}

		return z;
	}

	// Returns a matrix full of 1.
	private static RealMatrix ones(int n, int m) {
		return new Array2DRowRealMatrix(n, m).scalarAdd(1.0); 
	}

	// Multiplies point-wise the two matrix a, b.
	private static RealMatrix pointwiseMultiplication(RealMatrix a, RealMatrix b) {
		int n = a.getRowDimension();
		int m = a.getColumnDimension();
		RealMatrix result = new Array2DRowRealMatrix(n, m);
		for (int i = 0; i < n; ++i)
			for (int j = 0; j < m; ++j) 
				result.setEntry(i, j, a.getEntry(i, j) * b.getEntry(i, j));
		return result;
	}

	private static void setSubMatrix(RealMatrix dest, int[] rows, int[] cols, RealMatrix source) {
		for (int i = 0; i < rows.length; ++i)
			for (int j = 0; j < cols.length; ++j)
				dest.setEntry(rows[i], cols[j], source.getEntry(i, j));
	}

	private static int[] get_missing_rows(RealMatrix x) {
		int n = x.getRowDimension();
		int m = x.getColumnDimension();

		ArrayList<Integer> missing_rows_list = new ArrayList<Integer>();
		for (int i = 0; i < n; ++i) {
			for (int j = 0; j < m; ++j) 
				if (Double.isNaN(x.getEntry(i, j))) {
					missing_rows_list.add(i);
					break;
				}
		}
		int[] missing_rows_array = new int[missing_rows_list.size()];
		for (int i = 0; i < missing_rows_list.size(); ++i) {
			missing_rows_array[i] = missing_rows_list.get(i);
		}
		return missing_rows_array;
	}
}
