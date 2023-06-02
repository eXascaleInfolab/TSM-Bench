package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 12-3-11
 * Time: 下午2:04
 * To change this template use File | Settings | File Templates.
 */
public class HistogramNode {
    public HistogramNode parent;
    public double lowBound;
    public double uppBound;
    public long count;
    public List<HistogramNode> children = new ArrayList<HistogramNode>();

    public HistogramNode(HistogramNode parent, double lowBound, double uppBound, long count) {
        this.parent = parent;
        this.lowBound = lowBound;
        this.uppBound = uppBound;
        this.count = count;
    }
}
