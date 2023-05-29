package cn.edu.fudan.cs.dstree.util;

import java.io.IOException;
import java.util.Arrays;

/**
 * Created by IntelliJ IDEA.
 * User: zetasq
 * Date: 1/31/11
 * Time: 9:26 PM
 * To change this template use File | Settings | File Templates.
 */
public class DistUtil {
    public static double euclideanDist(double[] ts_1, double[] ts_2) {
        double sum = 0;
        for (int i = 0; i < ts_1.length; i++) {
            final double dp = ts_1[i] - ts_2[i];
            sum += dp * dp;
        }
        return Math.sqrt(sum);
    }

    public static double minDist(String fileName, double[] queryTs) throws IOException {
        //open index file;
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(fileName);
        timeSeriesReader.open();
        double ShortestDist = Double.POSITIVE_INFINITY;
        double tempDist;
        int rowNo = 0;
        int resultLineNo = -1;
        while (timeSeriesReader.hasNext()) {
            double tempTimeseries[] = timeSeriesReader.next();
            tempDist = DistUtil.euclideanDist(queryTs, tempTimeseries);
            if (tempDist < ShortestDist) {
                ShortestDist = tempDist;
                resultLineNo = rowNo;
            }
            rowNo++;
        }
        timeSeriesReader.close();
        System.out.println("resultLineNo = " + resultLineNo);
        return ShortestDist;
    }

    public static double minDistBinary(String fileName, double[] queryTs) throws IOException {
        //open index file;
        double[][] tss = TimeSeriesFileUtil.readSeriesFromBinaryFileAtOnce(fileName, queryTs.length);
        return minDist(tss, queryTs);
    }

    public static double[] minDist(String fileName, double[][] multiTs) throws IOException {
        //open index file;
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(fileName);
        timeSeriesReader.open();
        double[] shortestDists = new double[multiTs.length];
        Arrays.fill(shortestDists, Double.POSITIVE_INFINITY);
        double tempDist;
        int rowNo = 0;
        int resultLineNo = -1;
        while (timeSeriesReader.hasNext()) {
            double tempTimeseries[] = timeSeriesReader.next();
            for (int i = 0; i < shortestDists.length; i++) {
                tempDist = DistUtil.euclideanDist(multiTs[i], tempTimeseries);
                if (tempDist < shortestDists[i]) {
                    shortestDists[i] = tempDist;
                    resultLineNo = rowNo;
                }
            }
            rowNo++;
        }
        timeSeriesReader.close();
        System.out.println("resultLineNo = " + resultLineNo);
        return shortestDists;
    }

    public static double minDist(double[][] tss, double[] queryTs) throws IOException {
        double ShortestDist = Double.POSITIVE_INFINITY;
        double tempDist;
//        int resultLineNo = -1;
        for (int i = 0; i < tss.length; i++) {
            tempDist = DistUtil.euclideanDist(queryTs, tss[i]);
            if (tempDist < ShortestDist) {
                ShortestDist = tempDist;
//                resultLineNo = i;
            }
        }
//        System.out.println("resultLineNo = " + resultLineNo);
        return ShortestDist;
    }


    public static int minDistIndex(double[][] tsArray, double[] queryTs) {
        int ret = -1;
        double ShortestDist = Double.POSITIVE_INFINITY;
        double tempDist;
        for (int i = 0; i < tsArray.length; i++) {
            tempDist = DistUtil.euclideanDist(queryTs, tsArray[i]);
            if (tempDist < ShortestDist) {
                ShortestDist = tempDist;
                ret = i;
            }
        }
        return ret;
    }
}
