package master;

import org.apache.commons.math3.linear.*;

public class CentroidDecomposition {
	public static void main(String[] args) {
		System.out.println("\n\n\n***********************************************************************\n");
		Array2DRowRealMatrix input = new Array2DRowRealMatrix(
			new double[][]{ {1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}}
		);
		System.out.println(input.toString());

		CentroidDecompositionResult result = CD(input);
		System.out.println("L = " + result.L.toString());
		System.out.println("R = " + result.R.toString());
		System.out.println("z = " + result.z.toString());
		System.out.println("L * R = " +  result.L.multiply(result.R.transpose()).toString());

		System.out.println("\n***********************************************************************\n\n\n");
	}

	public static CentroidDecompositionResult CD(RealMatrix matrix) {
		int n = matrix.getRowDimension();
		int m = matrix.getColumnDimension();

		CentroidDecompositionResult result = new CentroidDecompositionResult();
		result.L = new Array2DRowRealMatrix(n, m);
		result.R = new Array2DRowRealMatrix(m, m);
		result.z = new Array2DRowRealMatrix(n, m);

		for (int i = 0; i < m; ++i) {
			if (n < 5000) {
				result.z.setColumnMatrix(i, SSV(matrix) );
			} else {
				result.z.setColumnMatrix(i, SSV_init(matrix) );
			}

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
}
