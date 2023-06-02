package cn.edu.fudan.cs.dstree.dynamicsplit;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-10
 * Time: 上午10:30
 * To change this template use File | Settings | File Templates.
 */
public class StdevNodeSegmentSplitPolicy implements INodeSegmentSplitPolicy {
    public NodeSegmentSketch[] split(NodeSegmentSketch nodeSegmentSketch) {
        double max_stdev = nodeSegmentSketch.indicators[2];
        double min_stdev = nodeSegmentSketch.indicators[3];
        indicatorSplitValue = (float) ((max_stdev + min_stdev) / 2);  //the mean of stdeve value is split value       todo

        NodeSegmentSketch[] ret = new NodeSegmentSketch[2]; //split into 2 node
        ret[0] = new NodeSegmentSketch();
        ret[0].indicators = new float[nodeSegmentSketch.indicators.length];  //todo:
        ret[1] = new NodeSegmentSketch();
        ret[1].indicators = new float[nodeSegmentSketch.indicators.length];  //todo:

        for (int i = 0; i < ret.length; i++) {
            System.arraycopy(nodeSegmentSketch.indicators, 0, ret[i].indicators, 0, ret[i].indicators.length);
        }

        ret[0].indicators[2] = indicatorSplitValue;
        ret[1].indicators[3] = indicatorSplitValue;
        return ret;  //To change body of implemented methods use File | Settings | File Templates.
    }

    int indicatorSplitIdx = 1;
    float indicatorSplitValue;              //todo:

    public int getIndicatorSplitIdx() {
        return indicatorSplitIdx;
    }

    public float getIndicatorSplitValue() {           //todo:
        return indicatorSplitValue;
    }

    @Override
    public String toString() {
        return "(idx = " + indicatorSplitIdx + ", value = " + indicatorSplitValue + ")";
    }

}

