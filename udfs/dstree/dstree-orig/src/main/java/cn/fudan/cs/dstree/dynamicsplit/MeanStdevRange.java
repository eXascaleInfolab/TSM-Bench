package cn.edu.fudan.cs.dstree.dynamicsplit;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-5
 * Time: 下午8:11
 * To change this template use File | Settings | File Templates.
 */
public class MeanStdevRange implements IRange {
    public double calc(Sketch sketch, int len) {
        final double mean_width = sketch.indicators[0] - sketch.indicators[1];
        final double stdev_upper = sketch.indicators[2];
        final double stdev_lower = sketch.indicators[3];
        return len * (mean_width * mean_width + stdev_upper * stdev_upper);
    }
}
