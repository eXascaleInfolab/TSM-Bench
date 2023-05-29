package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.Serializable;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-7
 * Time: 下午7:38
 * To change this template use File | Settings | File Templates.
 */
public interface INodeSegmentSketchUpdater extends Serializable {
    NodeSegmentSketch updateSketch(NodeSegmentSketch nodeSegmentSketch, double[] series, int fromIdx, int toIdx);
}
