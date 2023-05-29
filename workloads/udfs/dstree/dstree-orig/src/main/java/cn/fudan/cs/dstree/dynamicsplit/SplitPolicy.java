package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.Serializable;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-7
 * Time: 下午7:03
 * To change this template use File | Settings | File Templates.
 */
public class SplitPolicy implements Serializable {
    short splitFrom;
    short splitTo;
    INodeSegmentSplitPolicy nodeSegmentSplitPolicy;

    public INodeSegmentSplitPolicy getNodeSegmentSplitPolicy() {
        return nodeSegmentSplitPolicy;
    }

    public void setNodeSegmentSplitPolicy(INodeSegmentSplitPolicy nodeSegmentSplitPolicy) {
        this.nodeSegmentSplitPolicy = nodeSegmentSplitPolicy;
    }

    int indicatorIdx;
    double indicatorSplitValue;

    ISeriesSegmentSketcher seriesSegmentSketcher;

    public ISeriesSegmentSketcher getSeriesSegmentSketcher() {
        return seriesSegmentSketcher;
    }

    public void setSeriesSegmentSketcher(ISeriesSegmentSketcher seriesSegmentSketcher) {
        this.seriesSegmentSketcher = seriesSegmentSketcher;
    }

    boolean routeToLeft(double[] series) {
        SeriesSegmentSketch seriesSegmentSketch = seriesSegmentSketcher.doSketch(series, splitFrom, splitTo);
        return (seriesSegmentSketch.indicators[indicatorIdx] < indicatorSplitValue);
    }

    @Override
    public String toString() {
       return "{ indicatorIdx = " + indicatorIdx + ", indicatorSplitValue = " + indicatorSplitValue + ", nodeSegmentSplitPolicy = " + nodeSegmentSplitPolicy + ", splitFrom = " + splitFrom + ", splitTo = " + splitTo + "}";
    }
}
