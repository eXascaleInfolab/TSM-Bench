package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.Serializable;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-7
 * Time: 下午7:26
 * To change this template use File | Settings | File Templates.
 */
public interface ISeriesSegmentSketcher extends Serializable {
    SeriesSegmentSketch doSketch(double[] series, int fromIdx, int toIdx);
}
