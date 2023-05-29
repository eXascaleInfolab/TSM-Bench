package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.Serializable;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-10
 * Time: 上午10:28
 * To change this template use File | Settings | File Templates.
 */
public interface INodeSegmentSplitPolicy extends Serializable {
    NodeSegmentSketch[] split(NodeSegmentSketch nodeSegmentSketch);

    int getIndicatorSplitIdx();

    float getIndicatorSplitValue();      //todo:wy

}
