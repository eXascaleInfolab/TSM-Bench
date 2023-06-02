package master;

import java.lang.Math;

public class ZScore {
	public static float[][] zScore(float[][] datapoints){
		int columns = datapoints[0].length;
		int rows = datapoints.length;
		float[][] result = new float[rows][columns];
		for (int j = 0; j < columns; j++) {
			float avg = (float) 0.0;
			for (int i = 0; i < rows; i++) {
				avg = avg + datapoints[i][j];
			}
			avg = avg / rows;
			float stdev = (float) 0.0;
			for (int i = 0; i < rows; i++) {
				stdev = stdev + (datapoints[i][j] - avg) * (datapoints[i][j] - avg);
			}
			stdev = (float) Math.sqrt(stdev / rows);
			for (int i = 0; i < rows; i++) {
				result[i][j] = (datapoints[i][j] - avg) / stdev;
			}
		}
		return result;
	}
    
};
