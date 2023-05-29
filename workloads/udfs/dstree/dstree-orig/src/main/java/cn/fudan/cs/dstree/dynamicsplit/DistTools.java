package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.CalcUtil;
import cn.edu.fudan.cs.dstree.util.DistUtil;

import java.io.IOException;

public class DistTools {
    /**
     * using avg and std
     * @param node
     * @param queryTs
     * @return
     * @throws IOException
     */
    public static double minDist(Node node, double[] queryTs) throws IOException {
        double sum = 0;
        short[] points = node.nodePoints;
        double[] avg = CalcUtil.avgBySegments(queryTs, points);
        double[] stdDev = CalcUtil.devBySegments(queryTs, points);

        for (int i = 0; i < avg.length; i++) {
            //use mean and standardDeviation to estimate the distance
            double tempDist = 0;
            //stdDev out the range of min std and max std
            if ((stdDev[i] - node.nodeSegmentSketches[i].indicators[2]) * (stdDev[i] - node.nodeSegmentSketches[i].indicators[3]) > 0) {
                tempDist += Math.pow(Math.min(Math.abs(stdDev[i] - node.nodeSegmentSketches[i].indicators[2]), Math.abs(stdDev[i] - node.nodeSegmentSketches[i].indicators[3])), 2);
            }

            //avg out the range of min mean and max mean
            if ((avg[i] - node.nodeSegmentSketches[i].indicators[0]) * (avg[i] - node.nodeSegmentSketches[i].indicators[1]) > 0) {
                tempDist += Math.pow(Math.min(Math.abs(avg[i] - node.nodeSegmentSketches[i].indicators[0]), Math.abs(avg[i] - node.nodeSegmentSketches[i].indicators[1])), 2);
            }
            sum += tempDist * node.getSegmentLength(i);
        }
        sum = Math.sqrt(sum);
        return sum;
    }

    /**
     * use only avg
     * @param node
     * @param queryTs
     * @return
     * @throws IOException
     */
    public static double minDistByAvg(Node node, double[] queryTs) throws IOException {
        double sum = 0;
        short[] points = node.nodePoints;
        double[] avg = CalcUtil.avgBySegments(queryTs, points);
        for (int i = 0; i < avg.length; i++) {
            double tempDist = 0;
            if ((avg[i] - node.nodeSegmentSketches[i].indicators[0]) * (avg[i] - node.nodeSegmentSketches[i].indicators[1]) > 0) {
                tempDist += Math.pow(Math.min(Math.abs(avg[i] - node.nodeSegmentSketches[i].indicators[0]), Math.abs(avg[i] - node.nodeSegmentSketches[i].indicators[1])), 2);
            }
            sum += tempDist * node.getSegmentLength(i);
        }
        sum = Math.sqrt(sum);
        return sum;
    }

    public static double maxDist(Node node, double[] queryTs) {
        double sum = 0;
        short[] points = node.nodePoints;
        double[] avg = CalcUtil.avgBySegments(queryTs, points);
        double[] stdDev = CalcUtil.devBySegments(queryTs, points);

        for (int i = 0; i < avg.length; i++) {
            double tempDist = 0;
            //using max std
            tempDist += Math.pow(stdDev[i] + node.nodeSegmentSketches[i].indicators[2], 2);
            //max of (avg to min mean and max mean)
            tempDist += Math.pow(Math.max(Math.abs(avg[i] - node.nodeSegmentSketches[i].indicators[0]), Math.abs(avg[i] - node.nodeSegmentSketches[i].indicators[1])), 2);
            sum += tempDist * node.getSegmentLength(i);
        }
        sum = Math.sqrt(sum);
        return sum;
    }

    public static double lowerBoundBy2Timeseries(double[] ts1, double[] ts2) {
        double avg1 = CalcUtil.avg(ts1);
        double stdDev1 = CalcUtil.deviation(ts1);
        double avg2 = CalcUtil.avg(ts2);
        double stdDev2 = CalcUtil.deviation(ts2);
        double lowerBound = Math.sqrt(ts1.length * (Math.pow(stdDev1 - stdDev2, 2) + Math.pow(avg1 - avg2, 2)));
        return lowerBound;
    }

    public static double upperBoundBy2Timeseries(double[] ts1, double[] ts2) {
        double avg1 = CalcUtil.avg(ts1);
        double stdDev1 = CalcUtil.deviation(ts1);
        double avg2 = CalcUtil.avg(ts2);
        double stdDev2 = CalcUtil.deviation(ts2);
        double upperBound = Math.sqrt(ts1.length * (Math.pow(stdDev1 + stdDev2, 2) + Math.pow(avg1 - avg2, 2)));
        return upperBound;
    }
}
