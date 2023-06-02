package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.CalcUtil;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-7
 * Time: 下午7:28
 * To change this template use File | Settings | File Templates.
 */
public class MeanStdevSeriesSegmentSketcher implements ISeriesSegmentSketcher {
    public SeriesSegmentSketch doSketch(double[] series, int fromIdx, int toIdx) {
        SeriesSegmentSketch seriesSegmentSketch = new SeriesSegmentSketch();
        seriesSegmentSketch.indicators = new float[2];            //todo

        seriesSegmentSketch.indicators[0] = (float) CalcUtil.avg(series, fromIdx, toIdx);
        seriesSegmentSketch.indicators[1] = (float) CalcUtil.deviation(series, fromIdx, toIdx);
        return seriesSegmentSketch;
    }
}
