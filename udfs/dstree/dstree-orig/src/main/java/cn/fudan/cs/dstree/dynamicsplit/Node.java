package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.CalcUtil;
import de.ruedigermoeller.serialization.FSTObjectInput;
import de.ruedigermoeller.serialization.FSTObjectOutput;

import java.io.*;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-4-27
 * Time: 下午9:07
 * To change this template use File | Settings | File Templates.
 */
public class Node implements Serializable {

    transient INodeSegmentSplitPolicy[] nodeSegmentSplitPolicies;

    public void setNodeSegmentSplitPolicies(INodeSegmentSplitPolicy[] nodeSegmentSplitPolicies) {
        this.nodeSegmentSplitPolicies = nodeSegmentSplitPolicies;
    }

    transient IRange range;

    public void setRange(IRange range) {
        this.range = range;
    }

    public Node(Node parent) {
        this(parent.indexPath, parent.threshold);

        this.nodeSegmentSplitPolicies = parent.nodeSegmentSplitPolicies;
        this.range = parent.range;
        this.nodeSegmentSketchUpdater = parent.nodeSegmentSketchUpdater;
        this.seriesSegmentSketcher = parent.seriesSegmentSketcher;
        this.parent = parent;

        level = parent.level + 1;
    }

    public Node(String indexPath, int threshold) {
        this.indexPath = indexPath;
        this.threshold = threshold;
    }

    public boolean isRoot() {
        return parent == null;
    }

    Node parent;

    //start from 0
    int level = 0;

    boolean isLeft;

    String indexPath;

    public int getSegmentSize() {
        return nodePoints.length;
    }

    public short getSegmentStart(short [] points, int idx) {
        if (idx == 0)
            return 0;
        else
            return points[idx - 1];
    }

    public short getSegmentEnd(short [] points, int idx) {
        return points[idx];
    }

    public int getSegmentLength(int i) {
        if (i == 0)
            return nodePoints[i];
        else
            return nodePoints[i] - nodePoints[i - 1];
    }

    public int getSegmentLength(short [] points, int i) {
        if (i == 0)
            return points[i];
        else
            return points[i] - points[i - 1];
    }

    transient int threshold;
    int size = 0;

    Node left;
    Node right;

    public int getSize() {
        return size;
    }

    public boolean isTerminal() {
        return (left == null && right == null);
    }

    public void append(double[] timeSeries) throws IOException {
        FileBufferManager fileBufferManager = FileBufferManager.getInstance();
        FileBuffer fileBuffer = fileBufferManager.getFileBuffer(getFileName());
        fileBuffer.append(timeSeries);
    }


    public void insert(double[] timeSeries) throws IOException {
        //update statistics dynamically for leaf and branch
        updateStatistics(timeSeries);

        if (isTerminal()) {
            append(timeSeries);            //append to file first

            if (threshold == size) {   //do split
                String fileName = getFileName();

                splitPolicy = new SplitPolicy();
                splitPolicy.setSeriesSegmentSketcher(this.getSeriesSegmentSketcher());

                //init the vars used in loop
                double maxDiffValue = Double.MAX_VALUE * -1;
                double avg_children_range_value = 0;
                short horizontalSplitPoint = -1; //default not do horizontal split

                //we want to test every possible split policy for each segment
                for (int i = 0; i < nodePoints.length; i++) {
                    //for each segment
                    double nodeRangeValue = range.calc(nodeSegmentSketches[i], getSegmentLength(nodePoints, i));

                    //for every split policy
                    for (int j = 0; j < nodeSegmentSplitPolicies.length; j++) {
                        INodeSegmentSplitPolicy nodeSegmentSplitPolicy = nodeSegmentSplitPolicies[j];
                        NodeSegmentSketch[] childNodeSegmentSketches = nodeSegmentSplitPolicy.split(nodeSegmentSketches[i]);

                        double rangeValues[] = new double[childNodeSegmentSketches.length];
                        for (int k = 0; k < childNodeSegmentSketches.length; k++) {
                            NodeSegmentSketch childNodeSegmentSketch = childNodeSegmentSketches[k];
                            rangeValues[k] = range.calc(childNodeSegmentSketch, getSegmentLength(nodePoints, i));
                        }

                        avg_children_range_value = CalcUtil.avg(rangeValues);

                        double diffValue = nodeRangeValue - avg_children_range_value;
                        if (diffValue > maxDiffValue) {
                            maxDiffValue = diffValue;
                            splitPolicy.splitFrom = getSegmentStart(nodePoints, i);
                            splitPolicy.splitTo = getSegmentEnd(nodePoints, i);
                            splitPolicy.indicatorIdx = nodeSegmentSplitPolicy.getIndicatorSplitIdx();
                            splitPolicy.indicatorSplitValue = nodeSegmentSplitPolicy.getIndicatorSplitValue();
                            splitPolicy.setNodeSegmentSplitPolicy(nodeSegmentSplitPolicy);
                        }
                    }
                }

//                System.out.println("before maxDiffValue = " + maxDiffValue);

                //wy add trade off for horizontal split
                maxDiffValue = maxDiffValue * 2;

                //for every hsNodeSegmentSketches
                for (int i = 0; i < hsNodePoints.length; i++) {
                    //for each segment
                    double nodeRangeValue = range.calc(hsNodeSegmentSketches[i], getSegmentLength(hsNodePoints, i));

                    //for every split policy
                    for (int j = 0; j < nodeSegmentSplitPolicies.length; j++) {
                        INodeSegmentSplitPolicy hsNodeSegmentSplitPolicy = nodeSegmentSplitPolicies[j];
                        NodeSegmentSketch[] childNodeSegmentSketches = hsNodeSegmentSplitPolicy.split(hsNodeSegmentSketches[i]);

                        double rangeValues[] = new double[childNodeSegmentSketches.length];
                        for (int k = 0; k < childNodeSegmentSketches.length; k++) {
                            NodeSegmentSketch childNodeSegmentSketch = childNodeSegmentSketches[k];
                            rangeValues[k] = range.calc(childNodeSegmentSketch, getSegmentLength(hsNodePoints, i));
                        }

                        avg_children_range_value = CalcUtil.avg(rangeValues);

                        double diffValue = nodeRangeValue - avg_children_range_value;
                        if (diffValue > maxDiffValue) {
//                            System.out.println("diffValue = " + diffValue);
                            maxDiffValue = diffValue;
                            splitPolicy.splitFrom = getSegmentStart(hsNodePoints, i);
                            splitPolicy.splitTo = getSegmentEnd(hsNodePoints, i);
                            splitPolicy.indicatorIdx = hsNodeSegmentSplitPolicy.getIndicatorSplitIdx();
                            splitPolicy.indicatorSplitValue = hsNodeSegmentSplitPolicy.getIndicatorSplitValue();
                            splitPolicy.setNodeSegmentSplitPolicy(hsNodeSegmentSplitPolicy);

                            //get horizontalSplitPoint
                            horizontalSplitPoint = getHorizontalSplitPoint(nodePoints, splitPolicy.splitFrom, splitPolicy.splitTo);
                        }
                    }
                }

//                System.out.println("horizontalSplitPoint = " + horizontalSplitPoint);
//                System.out.println("splitPolicy.getVerticalSplitPolicy().getClass().getSimpleName() = " + splitPolicy.getNodeSegmentSplitPolicy().getClass().getSimpleName());

                short[] childNodePoint;
                if (horizontalSplitPoint < 0) //not hs
                {
                    childNodePoint = new short[nodePoints.length];
                    System.arraycopy(nodePoints, 0, childNodePoint, 0, nodePoints.length);
                } else {
                    childNodePoint = new short[nodePoints.length + 1];
                    System.arraycopy(nodePoints, 0, childNodePoint, 0, nodePoints.length);
                    childNodePoint[childNodePoint.length - 1] = horizontalSplitPoint;
                    Arrays.sort(childNodePoint);
                }

                //init children node
                left = new Node(this);
                left.initSegments(childNodePoint);
                left.isLeft = true;
                
		right = new Node(this);
                right.initSegments(childNodePoint);
                right.isLeft = false;

                //read the time series from file, all the time series in this file include the new insert one
                //using buffer
                FileBufferManager fileBufferManager = FileBufferManager.getInstance();
                FileBuffer fileBuffer = fileBufferManager.getFileBuffer(getFileName());
                List<double[]> list = fileBuffer.getAllTimeSeries();
                for (int i = 0; i < list.size(); i++) {
                    double[] ts = list.get(i);
                    if (splitPolicy.routeToLeft(ts)) {
                        left.insert(ts);
		    } else {
                        right.insert(ts);
	 	    }
                }

                fileBufferManager.DeleteFile(getFileName());
            }
        } else { //not terminal
            //find the children and insert recursively
            if (splitPolicy.routeToLeft(timeSeries))
                left.insert(timeSeries);
            else
                right.insert(timeSeries);
        }
    }

    short getHorizontalSplitPoint(short [] points, short from, short to) {
        if (Arrays.binarySearch(points, to) < 0) {
            return to;
        } else
            return from;
    }

    SplitPolicy splitPolicy;

    short [] nodePoints;
    transient short[] hsNodePoints;
    NodeSegmentSketch[] nodeSegmentSketches;
    transient NodeSegmentSketch[] hsNodeSegmentSketches; //for horizontal splitting

    transient ISeriesSegmentSketcher seriesSegmentSketcher; //= new MeanStdevSeriesSegmentSketcher();
    transient INodeSegmentSketchUpdater nodeSegmentSketchUpdater;// = new MeanStdevNodeSegmentSketchUpdater(seriesSegmentSketcher);

    public ISeriesSegmentSketcher getSeriesSegmentSketcher() {
        return seriesSegmentSketcher;
    }

    public void setSeriesSegmentSketcher(ISeriesSegmentSketcher seriesSegmentSketcher) {
        this.seriesSegmentSketcher = seriesSegmentSketcher;
    }

    public INodeSegmentSketchUpdater getNodeSegmentSketchUpdater() {
        return nodeSegmentSketchUpdater;
    }

    public void setNodeSegmentSketchUpdater(INodeSegmentSketchUpdater nodeSegmentSketchUpdater) {
        this.nodeSegmentSketchUpdater = nodeSegmentSketchUpdater;
    }

    private void updateStatistics(double[] timeSeries) {
        size++;
        //update nodeSegmentSketches
        for (int i = 0; i < nodePoints.length; i++) {
            NodeSegmentSketch nodeSegmentSketch = nodeSegmentSketches[i];
            nodeSegmentSketchUpdater.updateSketch(nodeSegmentSketch, timeSeries, getSegmentStart(nodePoints, i), getSegmentEnd(nodePoints, i));
        }

        //update hsNodeSegmentSketches
        for (int i = 0; i < hsNodePoints.length; i++) {
            NodeSegmentSketch hsNodeSegmentSketch = hsNodeSegmentSketches[i];
            nodeSegmentSketchUpdater.updateSketch(hsNodeSegmentSketch, timeSeries, getSegmentStart(hsNodePoints, i), getSegmentEnd(hsNodePoints, i));
        }
    }

    public double min(double[] values) {
        double ret = values[0];
        for (int i = 0; i < values.length; i++) {
            double value = values[i];
            if (value < ret)
                ret = value;
        }
        return ret;
    }

    public int minIdx(double[] values) {
        double ret = values[0];
        int retIdx = 0;
        for (int i = 0; i < values.length; i++) {
            double value = values[i];
            if (value < ret) {
                ret = value;
                retIdx = i;
            }
        }
        return retIdx;
    }

    public double max(double[] values) {
        double ret = values[0];
        for (int i = 0; i < values.length; i++) {
            double value = values[i];
            if (value > ret)
                ret = value;
        }
        return ret;
    }

    public int maxIdx(double[] values) {
        double ret = values[0];
        int retIdx = 0;
        for (int i = 0; i < values.length; i++) {
            double value = values[i];
            if (value > ret) {
                ret = value;
                retIdx = i;
            }
        }
        return retIdx;
    }

    public static int maxSegmentLength = 2;
    public static int maxValueLength = 10;

    public String getFileName() {
        String ret = indexPath;
        if (!indexPath.endsWith(File.separator))
            ret = ret + File.separator;
        ret = ret + formatInt(getSegmentSize(), maxSegmentLength);
        //04_(1,23,433,445,3334,3434) root
        //09_03(111,333,<0.334343434)_(1,23,433,445,3334,3434) children
        if (!this.isRoot()) {
            if (isLeft)
                ret = ret + "_L";
            else
                ret = ret + "_R";

            //add parent split policy
            ret = ret + "_" + parent.splitPolicy.indicatorIdx + "_";
            ret = ret + "_" + parent.splitPolicy.getNodeSegmentSplitPolicy().getClass().getSimpleName() + "_";

            ret = ret + "(" + parent.splitPolicy.splitFrom + "," + parent.splitPolicy.splitTo + "," + formatDouble(parent.splitPolicy.indicatorSplitValue, maxValueLength) + ")";
        }
        ret = ret + "_" + level;

        return ret;
    }

    public String formatInt(int value, int length) {
        String ret = String.valueOf(value);
        if (ret.length() > length) {
            throw new RuntimeException("exceed length:" + length);
        }
        while (ret.length() < length) {
            ret = "0" + ret;
        }
        return ret;
    }

    public String formatDouble(double value, int length) {
        String ret = String.valueOf(value);
        if (ret.length() > length) {
            ret = ret.substring(0, length - 1);
        }
        return ret;
    }

    public void initSegments(short[] segmentPoints) {
        this.nodePoints = new short[segmentPoints.length];
        System.arraycopy(segmentPoints, 0, this.nodePoints, 0, segmentPoints.length);

        this.hsNodePoints = CalcUtil.split(segmentPoints, (short) 1); //max length is 1

        //update nodeSegmentSketches and hsNodeSegmentSketches
        nodeSegmentSketches = new NodeSegmentSketch[nodePoints.length];
        for (int i = 0; i < nodeSegmentSketches.length; i++) {
            nodeSegmentSketches[i] = new NodeSegmentSketch();
        }

        hsNodeSegmentSketches = new NodeSegmentSketch[hsNodePoints.length];
        for (int i = 0; i < hsNodeSegmentSketches.length; i++) {
            hsNodeSegmentSketches[i] = new NodeSegmentSketch();
        }
    }

    public TreeInfo printTreeInfo() {
        //1.get total node
        //2.get terminal node(empty and not empty)
        //3.get average amount for none empty terminal node

        //using dept-first
        //init first level node
        TreeInfo tInfo = new TreeInfo();
        List<Node> list = new ArrayList<Node>();
        list.add(this);

        int totalCount = 0;
        int emptyNodeCount = 0;
        int noneEmptyNodeCount = 0;
        int tsCount = 0;
        int sumofLevel = 0;

        //stack
        while (list.size() > 0) {
            //pop
            Node node = list.remove(list.size() - 1);

            totalCount++;

            if (node.isTerminal()) {
                //for terminal node
                if (node.size > 0) {
                    noneEmptyNodeCount++;
                    tsCount += node.size;
                    sumofLevel += node.level;
                } else
                    emptyNodeCount++;
            } else {
                //for internal node
                //push their children if it is internal node
                list.add(node.left);
                list.add(node.right);
            }
        }
        double avgLevel = sumofLevel / (double) noneEmptyNodeCount;
        double avgPerNode = tsCount / (noneEmptyNodeCount == 0 ? 1 : noneEmptyNodeCount);

        tInfo.setTotalCount(totalCount);
        tInfo.setTsCount(tsCount);
        tInfo.setEmptyNodeCount(emptyNodeCount);
        tInfo.setNoneEmptyNodeCount(noneEmptyNodeCount);
        tInfo.setAvgPerNode(avgPerNode);
        tInfo.setAvgLevel(avgLevel);
        return tInfo;
    }

    public void toXml(StringBuffer xml) {
	spaces(xml, level); xml.append("<node>").append("\n");
	spaces(xml, level + 1); xml.append("hsNodePoints: ").append(Arrays.toString(hsNodePoints)).append("\n");
	spaces(xml, level + 1); xml.append("hsNodeSegmentSketches: ").append(Arrays.toString(hsNodeSegmentSketches)).append("\n");
	spaces(xml, level + 1); xml.append("indexPath: ").append(indexPath).append("\n");
	spaces(xml, level + 1); xml.append("isLeft: ").append(isLeft).append("\n");
	spaces(xml, level + 1); xml.append("left: ");
	if (left != null) {
	    xml.append("\n");
            left.toXml(xml);
	} else {
		xml.append("null\n");
	}
	spaces(xml, level + 1); xml.append("level: ").append(level).append("\n");	
	spaces(xml, level + 1); xml.append("nodePoints: ").append(Arrays.toString(nodePoints)).append("\n");
	spaces(xml, level + 1); xml.append("nodeSegmentSketches: ").append(Arrays.toString(nodeSegmentSketches)).append("\n");
	spaces(xml, level + 1); xml.append("nodeSegmentSplitPolicies: ").append(Arrays.toString(nodeSegmentSplitPolicies)).append("\n");
	spaces(xml, level + 1); xml.append("right: ");
	if (right != null) {
		xml.append("\n");
		right.toXml(xml);
	} else {
		xml.append("null\n");
	}
	spaces(xml, level + 1); xml.append("size: ").append(size).append("\n");
	spaces(xml, level + 1); xml.append("splitPolicy: ").append(splitPolicy).append("\n");
	spaces(xml, level + 1); xml.append("threshold: ").append(threshold).append("\n");
	spaces(xml, level); xml.append("</node>").append("\n");
    }
    public void spaces(StringBuffer xml, int l) {
	for (int i = 0; i < l; ++i)
		xml.append(" ");
    }

    public Node approximateSearch(double[] queryTs) {
        System.out.println("this.getFileName() = " + this.getFileName());
        if (isTerminal())
            return this;
        else //internal node
        {
            if (splitPolicy.routeToLeft(queryTs))
                return left.approximateSearch(queryTs);
            else
                return right.approximateSearch(queryTs);
        }
    }

    public void saveToFile(String fileName) throws IOException {
//        FileOutputStream fos = new FileOutputStream(fileName);
//        ObjectOutputStream oos = new ObjectOutputStream(fos);
//        oos.writeObject(this);
//        fos.close();
        FSTObjectOutput out = new FSTObjectOutput(new FileOutputStream(fileName));
        out.writeObject(this);
        out.close(); // required !
    }

    public static Node loadFromFile(String fileName) throws IOException, ClassNotFoundException {
//        FileInputStream fis = new FileInputStream(fileName);
//        ObjectInputStream ios = new ObjectInputStream(fis);
//        return  (Node) ios.readObject();
        FSTObjectInput in = new FSTObjectInput(new FileInputStream(fileName));
        Node node = null;
        try {
            node = (Node) in.readObject(Node.class);
        } catch (Exception e) {
            throw new IOException(e.getMessage());
        }
        in.close();
        return node;
    }
}
