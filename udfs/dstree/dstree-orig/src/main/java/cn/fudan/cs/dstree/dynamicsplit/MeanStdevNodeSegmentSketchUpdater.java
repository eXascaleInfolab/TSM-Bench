package cn.edu.fudan.cs.dstree.dynamicsplit;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-7
 * Time: 下午7:40
 * To change this template use File | Settings | File Templates.
 */
public class MeanStdevNodeSegmentSketchUpdater implements INodeSegmentSketchUpdater {
    ISeriesSegmentSketcher seriesSegmentSketcher;

    public NodeSegmentSketch updateSketch(NodeSegmentSketch nodeSegmentSketch, double[] series, int fromIdx, int toIdx) {
        SeriesSegmentSketch seriesSegmentSketch = seriesSegmentSketcher.doSketch(series, fromIdx, toIdx);

        if (nodeSegmentSketch.indicators == null) //not initial
        {
            nodeSegmentSketch.indicators = new float[4];                //float    todo
            nodeSegmentSketch.indicators[0] = Float.MAX_VALUE * -1; //for max mean
            nodeSegmentSketch.indicators[1] = Float.MAX_VALUE; //for min mean
            nodeSegmentSketch.indicators[2] = Float.MAX_VALUE * -1; //for max stdev
            nodeSegmentSketch.indicators[3] = Float.MAX_VALUE; //for min stdev
        }

        nodeSegmentSketch.indicators[0] = Math.max(nodeSegmentSketch.indicators[0], seriesSegmentSketch.indicators[0]);
        nodeSegmentSketch.indicators[1] = Math.min(nodeSegmentSketch.indicators[1], seriesSegmentSketch.indicators[0]);
        nodeSegmentSketch.indicators[2] = Math.max(nodeSegmentSketch.indicators[2], seriesSegmentSketch.indicators[1]);
        nodeSegmentSketch.indicators[3] = Math.min(nodeSegmentSketch.indicators[3], seriesSegmentSketch.indicators[1]);

        return nodeSegmentSketch;
    }

    public MeanStdevNodeSegmentSketchUpdater(ISeriesSegmentSketcher seriesSegmentSketcher) {
        this.seriesSegmentSketcher = seriesSegmentSketcher;
    }
}
