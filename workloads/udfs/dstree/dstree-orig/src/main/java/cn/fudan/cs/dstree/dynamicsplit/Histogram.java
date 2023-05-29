package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.NorminvUtil;
import org.apache.commons.math.MathException;
import org.apache.commons.math.distribution.NormalDistribution;
import org.apache.commons.math.distribution.NormalDistributionImpl;

import java.util.Arrays;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 12-3-11
 * Time: 下午2:08
 * To change this template use File | Settings | File Templates.
 */
public class Histogram {
    private double min;
    private double max;
    private int size;
    private double step;
    private double starts[];
    private long[] counts;

    public int getSize() {
        return size;
    }

    public double[] getStarts() {
        return starts;
    }

    public Histogram(HistogramNode root, double min, double max, double step) {
        this(root, min, max, (int) Math.round(Math.ceil((root.uppBound - root.lowBound) / step)));
    }

    public Histogram(HistogramNode root, double min, double max, int histSize) {
        this.min = min;
        this.max = max;
        this.size = histSize;
        this.step = (max - min) / histSize;
        //init the bins
        this.starts = new double[this.size];
        for (int i = 0; i < starts.length; i++) {
            starts[i] = this.min + i * step;
        }
        this.counts = new long[this.size];
        Arrays.fill(this.counts, 0);

        //visit the left node recursively and build the histogram
        calcHistogram(root);
    }

    private void calcHistogram(HistogramNode histogramNode) {
        if (histogramNode.children.size() > 0) {       //internal node
            for (int i = 0; i < histogramNode.children.size(); i++) {
                HistogramNode child = histogramNode.children.get(i);
                calcHistogram(child);
            }
        } else //leaf node
        {
            double low = histogramNode.lowBound;
            double upp = histogramNode.uppBound;
            long cnt = histogramNode.count;

            int startPos = (int) (Math.floor((low - starts[0]) / step));
            int endPos = (int) (Math.floor((upp - starts[0]) / step));
            if (endPos >= starts.length) {
                endPos = starts.length - 1;
            }
            double width = upp - low;

            long countAllocated = 0;
            for (int i = startPos; i <= endPos; i++) {
                //from the start[0]
                double intersect_width = calcIntersectWidth(starts[0], starts[i] + step, low, upp);

                long countSoFar = cnt;   //using count so far to avoid the accumulative error
                if (width > 0) {         //intersected
                    double ratio = intersect_width / width;
                    countSoFar = Math.round(cnt * calcProbabilityCount(ratio));
                }
                counts[i] += countSoFar - countAllocated;
                countAllocated = countSoFar;
            }
        }
    }

    private static final double CDF_LOW = NorminvUtil.getInvCDF(0.0000001, true);
    private static final double CDF_UPP = NorminvUtil.getInvCDF(1 - 0.0000001, true);
    private static final NormalDistribution distribution = new NormalDistributionImpl(0, 1);    //adjust mean and std or you can use uniform distribution instead

    /**
     * @param x
     * @return
     */
    private static double calcProbabilityCount(double x) {
        double width = CDF_UPP - CDF_LOW;
        double new_x = CDF_LOW + x * width;
        try {
            return distribution.cumulativeProbability(new_x);
        } catch (MathException e) {
            throw new RuntimeException(e);
        }
    }

    private double calcIntersectWidth(double start, double end, double low, double upp) {
        return Math.min(end, upp) - Math.max(start, low);
    }

    public void printInfo() {
        //print the middle value
        for (int i = 0; i < starts.length; i++) {
            System.out.println("start = " + (starts[i] + step / 2) + "  count = " + counts[i]);
        }
    }

    public double getMin() {
        return min;
    }

    public double getMax() {
        return max;
    }

    public double getStep() {
        return step;
    }

    public long[] getCounts() {
        return counts;
    }
}
